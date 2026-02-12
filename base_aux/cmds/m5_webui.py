import asyncio
import os
from typing import Optional
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from base_aux.cmds.m4_terminal1_os2_aio import *


# ==================== Менеджер сессий ====================
class SessionManager:
    def __init__(self):
        self.sessions: dict[str, CmdSession_OsTerminalAio] = {}

    async def create_session(self, session_id: Optional[str] = None) -> str:
        if session_id is None:
            session_id = str(uuid.uuid4())
        session = CmdSession_OsTerminalAio(id=session_id)
        self.sessions[session_id] = session
        return session_id

    async def get_session(self, session_id: str) -> Optional[CmdSession_OsTerminalAio]:
        return self.sessions.get(session_id)

    # async def reconnect_session(self, session_id: str) -> None:
    #     session = self.sessions.get(session_id)
    #     await session.reconnect()

    async def close_session(self, session_id: str) -> None:
        """Принудительно завершает сессию без отправки exit."""
        session = self.sessions.pop(session_id, None)
        if not session:
            return

        # Останавливаем фоновые задачи чтения
        session._stop_reading = True
        for task in session._reader_tasks:
            task.cancel()
        await asyncio.gather(*session._reader_tasks, return_exceptions=True)
        session._reader_tasks.clear()

        # Завершаем процесс
        if session._conn:
            try:
                session._conn.terminate()
                await asyncio.wait_for(session._conn.wait(), timeout=1.0)
            except asyncio.TimeoutError:
                session._conn.kill()
                await session._conn.wait()
            session._conn = None

    async def session_exists(self, session_id: str) -> bool:
        return session_id in self.sessions


session_manager = SessionManager()


# ==================== FastAPI приложение ====================
app = FastAPI(title="Web Terminal")

# HTML страница будет встроена прямо в код для простоты
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Web Terminal</title>
    <style>
        body { font-family: monospace; background: #1e1e1e; color: #d4d4d4; padding: 20px; }
        #output { 
            background: #2d2d2d; 
            padding: 15px; 
            border-radius: 5px; 
            height: 400px; 
            overflow-y: scroll;
            white-space: pre-wrap;
            word-wrap: break-word;
            border: 1px solid #444;
        }
        .stdout { color: #b5cea8; }
        .stderr { color: #f48771; }
        .stdin  { color: #dcdcaa; }
        .system { color: #569cd6; font-style: italic; }
        #input { 
            width: 100%; 
            padding: 10px; 
            font-size: 16px; 
            background: #3c3c3c; 
            color: #fff; 
            border: 1px solid #555; 
            margin-top: 10px;
            border-radius: 3px;
        }
        #status { margin-top: 10px; color: #888; }
        a { color: #569cd6; }
        .header { display: flex; justify-content: space-between; align-items: center; }
        button { background: #0e639c; color: white; border: none; padding: 6px 12px; border-radius: 3px; cursor: pointer; }
        button:hover { background: #1177bb; }
    </style>
</head>
<body>
    <div class="header">
        <h2>🔌 Web Terminal</h2>
        <div>
            <span id="status">⚡ Подключение...</span>
            <button onclick="reconnect()">Переподключиться</button>
        </div>
    </div>
    <div id="output"></div>
    <input type="text" id="input" placeholder="Введите команду и нажмите Enter" autofocus>

    <script>
        let socket = null;
        let sessionId = null;
        let isNewSession = true; // по умолчанию – новая сессия
    
        async function initSession() {
            const storedId = localStorage.getItem('terminal_session_id');
            if (storedId) {
                const resp = await fetch(`/sessions/${storedId}`);
                if (resp.ok) {
                    sessionId = storedId;
                    isNewSession = false; // сессия восстановлена
                    document.getElementById('status').innerHTML = `✅ Сессия восстановлена: ${sessionId}`;
                    connectWebSocket();
                    return;
                }
                localStorage.removeItem('terminal_session_id');
            }
    
            const resp = await fetch('/sessions', { method: 'POST' });
            const data = await resp.json();
            sessionId = data.session_id;
            isNewSession = true; // новая сессия
            localStorage.setItem('terminal_session_id', sessionId);
            document.getElementById('status').innerHTML = `✅ Сессия создана: ${sessionId}`;
            connectWebSocket();
        }
    
        function addOutputLine(type, text) {
            const output = document.getElementById('output');
            const line = document.createElement('div');
            line.className = type; // stdout, stderr, stdin, system
            line.textContent = text;
            output.appendChild(line);
            output.scrollTop = output.scrollHeight;
        }
    
        async function loadHistory() {
            if (!sessionId) return;
            try {
                const resp = await fetch(`/sessions/${sessionId}/history`);
                const history = await resp.json();
                addOutputLine('system', '=== ЗАГРУЖЕНА ИСТОРИЯ СЕССИИ ===');
                history.forEach(cmd => {
                    if (cmd.input) {
                        addOutputLine('stdin', `→ ${cmd.input}`);
                    }
                    if (cmd.stdout && Array.isArray(cmd.stdout)) {
                        cmd.stdout.forEach(line => addOutputLine('stdout', line));
                    }
                    if (cmd.stderr && Array.isArray(cmd.stderr)) {
                        cmd.stderr.forEach(line => addOutputLine('stderr', line));
                    }
                });
                addOutputLine('system', '=== КОНЕЦ ИСТОРИИ ===');
            } catch (err) {
                addOutputLine('stderr', `Ошибка загрузки истории: ${err.message}`);
            }
        }
    
        function connectWebSocket() {
            if (socket) socket.close();
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            socket = new WebSocket(`${protocol}//${window.location.host}/ws/${sessionId}`);
    
            socket.onopen = () => {
                document.getElementById('status').innerHTML = `✅ Сессия: ${sessionId} (WebSocket открыт)`;
                // Автоматически загружаем историю, если сессия не новая
                if (!isNewSession) {
                    loadHistory();
                }
            };
    
            socket.onmessage = (event) => {
                const msg = JSON.parse(event.data);
                addOutputLine(msg.type, msg.line);
            };
    
            socket.onclose = () => {
                document.getElementById('status').innerHTML = `❌ Сессия: ${sessionId} (отключено)`;
            };
    
            socket.onerror = (err) => {
                console.error('WebSocket error', err);
            };
        }
    
        function reconnect() {
            if (sessionId && socket && socket.readyState === WebSocket.OPEN) {
                socket.send('/reconnect');
            } else {
                console.warn('WebSocket не открыт, переподключение невозможно');
            }
        }
    
        document.getElementById('input').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && socket && socket.readyState === WebSocket.OPEN) {
                const cmd = e.target.value;
                if (cmd.trim() === '') return;
                socket.send(cmd);
                e.target.value = '';
            }
        });
    
        window.onload = initSession;
        window.onbeforeunload = () => {
            if (socket) socket.close();
        };
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_html():
    return HTML_TEMPLATE

@app.post("/sessions")
async def create_session():
    session_id = await session_manager.create_session()
    return {"session_id": session_id}

# @app.post("/sessions/{session_id}")
# async def reconnect_session(session_id: str):
#     await session_manager.reconnect_session(session_id)
#     return {"status": "closed"}

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    await session_manager.close_session(session_id)
    # await session_manager.reconnect_session(session_id)
    return {"status": "closed"}

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    session = await session_manager.get_session(session_id)
    if not session:
        await websocket.close(code=1008, reason="Invalid session")
        return

    # Подключаемся к терминалу, если ещё не подключены
    if not session._conn:
        await session.connect()

    # Создаём очередь для перехвата вывода
    output_queue = asyncio.Queue()

    # Сохраняем оригинальные методы
    original_append_stdout = session.history.append_stdout
    original_append_stderr = session.history.append_stderr

    # Патчим методы для отправки строк в очередь
    def patched_append_stdout(data):
        original_append_stdout(data)
        # Создаём задачу, чтобы не блокировать чтение
        asyncio.create_task(output_queue.put(("stdout", data)))

    def patched_append_stderr(data):
        original_append_stderr(data)
        asyncio.create_task(output_queue.put(("stderr", data)))

    session.history.append_stdout = patched_append_stdout
    session.history.append_stderr = patched_append_stderr

    # Задача для отправки данных из очереди в WebSocket
    async def send_output():
        try:
            while True:
                out_type, line = await output_queue.get()
                try:
                    await websocket.send_json({"type": out_type, "line": line})
                except (WebSocketDisconnect, RuntimeError):
                    # Сокет закрыт – прекращаем отправку
                    break
        except asyncio.CancelledError:
            pass

    send_task = asyncio.create_task(send_output())

    try:
        while True:
            cmd = await websocket.receive_text()
            if cmd == '/reconnect':
                await session.reconnect()
                await websocket.send_json({"type": "system", "line": "🔄 Сессия переподключена"})
            else:
                await session.send_command(cmd)
    except WebSocketDisconnect:
        pass
    finally:
        send_task.cancel()
        await send_task
        # Восстанавливаем оригинальные методы
        session.history.append_stdout = original_append_stdout
        session.history.append_stderr = original_append_stderr
        # ❌ НЕ закрываем сессию автоматически
        # await session_manager.close_session(session_id)


@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    exists = await session_manager.session_exists(session_id)
    if exists:
        return {"session_id": session_id, "active": True}
    raise HTTPException(status_code=404, detail="Session not found")


@app.get("/sessions/{session_id}/history")
async def get_session_history(session_id: str):
    session = await session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    history_data = []
    for result in session.history:
        history_data.append({
            "input": result.INPUT,
            "stdout": result.STDOUT,
            "stderr": result.STDERR,
            "timestamp": result.timestamp.isoformat() if result.timestamp else None,
            "duration": result.duration,
            "finished_status": result.finished_status.value if result.finished_status else None,
            "retcode": result.retcode
        })
    return history_data

# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


# =====================================================================================================================
