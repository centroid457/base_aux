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


# =====================================================================================================================
class SessionManager:
    def __init__(self):
        self.sessions: dict[str, CmdSession_OsTerminalAio] = {}
        # Ключ: session_id, значение: список очередей для каждого WebSocket
        self._output_queues: dict[str, list[asyncio.Queue]] = {}
        # Флаг: был ли уже применён патч к методам истории
        self._patched: set[str] = set()

    async def create_session(self, session_id: Optional[str] = None) -> str:
        if session_id is None:
            session_id = str(uuid.uuid4())
        session = CmdSession_OsTerminalAio(id=session_id)
        self.sessions[session_id] = session
        self._output_queues[session_id] = []
        return session_id

    async def get_session(self, session_id: str) -> Optional[CmdSession_OsTerminalAio]:
        return self.sessions.get(session_id)

    async def register_queue(self, session_id: str, queue: asyncio.Queue) -> None:
        """Добавляет очередь для рассылки вывода."""
        if session_id not in self._output_queues:
            self._output_queues[session_id] = []
        self._output_queues[session_id].append(queue)

    async def unregister_queue(self, session_id: str, queue: asyncio.Queue) -> None:
        """Удаляет очередь и, если она последняя, восстанавливает оригинальные методы."""
        queues = self._output_queues.get(session_id)
        if queues and queue in queues:
            queues.remove(queue)
        # Если больше нет клиентов – восстанавливаем оригинальные методы истории
        if session_id in self.sessions and not queues:
            session = self.sessions[session_id]
            if hasattr(session, '_original_append_stdout'):
                session.history.append_stdout = session._original_append_stdout
                session.history.append_stderr = session._original_append_stderr
                del session._original_append_stdout
                del session._original_append_stderr
            self._patched.discard(session_id)
            # Можно также удалить пустой список, но оставим для аккуратности
            self._output_queues[session_id] = []

    async def broadcast(self, session_id: str, msg: tuple[str, str]) -> None:
        """Разослать сообщение (тип, строка) во все очереди сессии."""
        queues = self._output_queues.get(session_id, [])
        for q in queues:
            await q.put(msg)

    async def close_session(self, session_id: str) -> None:
        """Принудительно завершает сессию, очищает очереди."""
        session = self.sessions.pop(session_id, None)
        if not session:
            return

        # Удаляем все очереди и восстанавливаем оригиналы
        self._output_queues.pop(session_id, None)
        if hasattr(session, '_original_append_stdout'):
            session.history.append_stdout = session._original_append_stdout
            session.history.append_stderr = session._original_append_stderr
            del session._original_append_stdout
            del session._original_append_stderr
        self._patched.discard(session_id)

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

    async def get_all_session_ids(self) -> list[str]:
        return list(self.sessions.keys())

    # connections --------
    async def register_connection(self, session_id: str, websocket: WebSocket):
        """Регистрирует WebSocket для сессии, закрывая предыдущее соединение."""
        if session_id in self.active_connections:
            old_ws = self.active_connections[session_id]
            try:
                await old_ws.close(code=1000, reason="New connection")
            except:
                pass
        self.active_connections[session_id] = websocket

    def unregister_connection(self, session_id: str):
        self.active_connections.pop(session_id, None)


session_manager = SessionManager()


# =====================================================================================================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Web Terminal — Multi Session</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: monospace;
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            margin: 0;
        }
        #app-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #444;
        }
        h1 {
            margin: 0;
            font-size: 24px;
            color: #fff;
        }
        #add-session-btn {
            background: #0e639c;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
        #add-session-btn:hover { background: #1177bb; }
        #sessions-container {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .session-window {
            background: #2d2d2d;
            border: 1px solid #444;
            border-radius: 6px;
            position: relative;
            display: flex;
            flex-direction: column;
        }
        .session-header {
            background: #3c3c3c;
            padding: 8px 12px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #555;
        }
        .session-title {
            font-weight: bold;
            color: #9cdcfe;
            font-size: 14px;
        }
        .close-btn {
            background: transparent;
            border: none;
            color: #f48771;
            font-size: 18px;
            cursor: pointer;
            padding: 0 6px;
            border-radius: 4px;
        }
        .close-btn:hover {
            background: #f48771;
            color: #1e1e1e;
        }
        .output {
            background: #1e1e1e;
            padding: 12px;
            height: 300px;
            overflow-y: scroll;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: monospace;
            border-bottom: 1px solid #444;
        }
        .stdout { color: #b5cea8; }
        .stderr { color: #f48771; }
        .stdin  { color: #dcdcaa; }
        .system { color: #569cd6; font-style: italic; }
        .input-area {
            display: flex;
            padding: 10px;
            background: #2d2d2d;
        }
        .session-input {
            flex: 1;
            padding: 8px;
            font-size: 14px;
            background: #3c3c3c;
            color: #fff;
            border: 1px solid #555;
            border-radius: 4px;
            font-family: monospace;
        }
        .session-input:focus {
            outline: none;
            border-color: #0e639c;
        }
        .reconnect-btn {
            background: #0e639c;
            color: white;
            border: none;
            padding: 4px 10px;
            margin-left: 8px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
        }
        .reconnect-btn:hover { background: #1177bb; }
        .status {
            margin-left: 10px;
            font-size: 12px;
            color: #888;
        }
    </style>
</head>
<body>
    <div id="app-header">
        <h1>🔌 Web Terminal — Multi Session</h1>
        <button id="add-session-btn">➕ Новая сессия</button>
    </div>
    <div id="sessions-container"></div>

    <script>
        // --------------------------------------------------------------
        // Глобальный менеджер сессий
        // --------------------------------------------------------------
        const sessionManager = {
            sessions: new Map(),
            container: document.getElementById('sessions-container'),
            addSessionBtn: document.getElementById('add-session-btn'),

            async init() {
                const serverIds = await this.fetchServerSessions();
                let storedIds = this.loadStoredIds();
                storedIds = storedIds.filter(id => serverIds.includes(id));
                this.saveStoredIds(storedIds);

                for (const id of storedIds) {
                    this.createSessionWindow(id, false);
                }

                if (this.sessions.size === 0) {
                    await this.createNewSession();
                }

                this.addSessionBtn.addEventListener('click', () => this.createNewSession());
            },

            async fetchServerSessions() {
                try {
                    const resp = await fetch('/sessions');
                    const data = await resp.json();
                    return data.sessions || [];
                } catch {
                    return [];
                }
            },

            loadStoredIds() {
                const stored = localStorage.getItem('terminal_session_ids');
                return stored ? JSON.parse(stored) : [];
            },

            saveStoredIds(ids) {
                localStorage.setItem('terminal_session_ids', JSON.stringify(ids));
            },

            async createNewSession() {
                const resp = await fetch('/sessions', { method: 'POST' });
                const data = await resp.json();
                const sessionId = data.session_id;
                const stored = this.loadStoredIds();
                stored.push(sessionId);
                this.saveStoredIds(stored);
                this.createSessionWindow(sessionId, true);
                return sessionId;
            },

            createSessionWindow(sessionId, isNew) {
                if (this.sessions.has(sessionId)) return;
                const sessionUI = new SessionUI(sessionId, this.container, isNew);
                this.sessions.set(sessionId, sessionUI);
                sessionUI.init();
            },

            async closeSession(sessionId) {
                await fetch(`/sessions/${sessionId}`, { method: 'DELETE' });
                const stored = this.loadStoredIds();
                const updated = stored.filter(id => id !== sessionId);
                this.saveStoredIds(updated);
                
                const sessionUI = this.sessions.get(sessionId);
                if (sessionUI) {
                    sessionUI.destroy();
                    this.sessions.delete(sessionId);
                }

                if (this.sessions.size === 0) {
                    await this.createNewSession();
                }
            }
        };

        // --------------------------------------------------------------
        // Класс одного окна сессии
        // --------------------------------------------------------------
        class SessionUI {
            constructor(sessionId, container, isNew) {
                this.sessionId = sessionId;
                this.container = container;
                this.isNew = isNew;
                this.socket = null;
                this.element = null;
                this.outputElement = null;
                this.inputElement = null;
                this.statusElement = null;
            }

            init() {
                this.render();
                this.connectWebSocket();
            }

            render() {
                const windowDiv = document.createElement('div');
                windowDiv.className = 'session-window';
                windowDiv.dataset.sessionId = this.sessionId;

                // Header
                const header = document.createElement('div');
                header.className = 'session-header';
                const title = document.createElement('span');
                title.className = 'session-title';
                title.textContent = `📟 Сессия: ${this.sessionId.slice(0,8)}...`;
                const closeBtn = document.createElement('button');
                closeBtn.className = 'close-btn';
                closeBtn.innerHTML = '&times;';
                closeBtn.onclick = () => sessionManager.closeSession(this.sessionId);
                header.appendChild(title);
                header.appendChild(closeBtn);

                // Output
                const output = document.createElement('div');
                output.className = 'output';
                this.outputElement = output;

                // Input area
                const inputArea = document.createElement('div');
                inputArea.className = 'input-area';
                const input = document.createElement('input');
                input.type = 'text';
                input.className = 'session-input';
                input.placeholder = 'Введите команду и нажмите Enter';
                this.inputElement = input;

                const reconnectBtn = document.createElement('button');
                reconnectBtn.className = 'reconnect-btn';
                reconnectBtn.textContent = '🔄';
                reconnectBtn.title = 'Переподключиться';
                reconnectBtn.onclick = () => this.sendReconnect();

                const statusSpan = document.createElement('span');
                statusSpan.className = 'status';
                statusSpan.textContent = '⚡ соединяемся...';
                this.statusElement = statusSpan;

                inputArea.appendChild(input);
                inputArea.appendChild(reconnectBtn);
                inputArea.appendChild(statusSpan);

                windowDiv.appendChild(header);
                windowDiv.appendChild(output);
                windowDiv.appendChild(inputArea);
                this.container.appendChild(windowDiv);
                this.element = windowDiv;

                input.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' && this.socket?.readyState === WebSocket.OPEN) {
                        const cmd = e.target.value.trim();
                        if (cmd) {
                            this.socket.send(cmd);
                            e.target.value = '';
                        }
                    }
                });
            }

            connectWebSocket() {
                if (this.socket) this.socket.close();
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/ws/${this.sessionId}`;
                this.socket = new WebSocket(wsUrl);

                this.socket.onopen = () => {
                    this.statusElement.textContent = '✅ онлайн';
                    if (!this.isNew) this.loadHistory();
                };
                this.socket.onmessage = (e) => {
                    const msg = JSON.parse(e.data);
                    this.addOutputLine(msg.type, msg.line);
                };
                this.socket.onclose = () => {
                    this.statusElement.textContent = '❌ отключено';
                };
                this.socket.onerror = () => {
                    this.statusElement.textContent = '⚠️ ошибка';
                };
            }

            sendReconnect() {
                if (this.socket?.readyState === WebSocket.OPEN) {
                    this.socket.send('/reconnect');
                }
            }

            async loadHistory() {
                try {
                    const resp = await fetch(`/sessions/${this.sessionId}/history`);
                    const history = await resp.json();
                    this.addOutputLine('system', '=== ЗАГРУЖЕНА ИСТОРИЯ СЕССИИ ===');
                    history.forEach(cmd => {
                        if (cmd.input) this.addOutputLine('stdin', `→ ${cmd.input}`);
                        cmd.stdout?.forEach(l => this.addOutputLine('stdout', l));
                        cmd.stderr?.forEach(l => this.addOutputLine('stderr', l));
                    });
                    this.addOutputLine('system', '=== КОНЕЦ ИСТОРИИ ===');
                } catch (err) {
                    this.addOutputLine('stderr', `Ошибка загрузки истории: ${err.message}`);
                }
            }

            addOutputLine(type, text) {
                const line = document.createElement('div');
                line.className = type;
                line.textContent = text;
                this.outputElement.appendChild(line);
                this.outputElement.scrollTop = this.outputElement.scrollHeight;
            }

            destroy() {
                this.socket?.close();
                this.element?.remove();
            }
        }

        // --------------------------------------------------------------
        // Запуск
        // --------------------------------------------------------------
        window.onload = () => sessionManager.init();
        window.onbeforeunload = () => {
            sessionManager.sessions.forEach(s => s.socket?.close());
        };
    </script>
</body>
</html>
"""


# =====================================================================================================================
app = FastAPI(title="Web Terminal")


@app.get("/", response_class=HTMLResponse)
async def get_html():
    return HTML_TEMPLATE


@app.post("/sessions")
async def create_session():
    session_id = await session_manager.create_session()
    return {"session_id": session_id}


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    await session_manager.close_session(session_id)
    # await session_manager.reconnect_session(session_id)
    return {"status": "closed"}


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


@app.get("/sessions")
async def list_sessions():
    ids = await session_manager.get_all_session_ids()
    return {"sessions": ids}


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    session = await session_manager.get_session(session_id)
    if not session:
        await websocket.close(code=1008, reason="Invalid session")
        return

    # Подключаем процесс, если ещё не подключён
    if not session._conn:
        await session.connect()

    # --- 1. Создаём очередь для этого клиента ---
    output_queue = asyncio.Queue()
    await session_manager.register_queue(session_id, output_queue)

    # --- 2. Патчим методы истории (только один раз!) ---
    if session_id not in session_manager._patched:
        # Сохраняем оригиналы как атрибуты экземпляра сессии
        session._original_append_stdout = session.history.append_stdout
        session._original_append_stderr = session.history.append_stderr

        def patched_append_stdout(data):
            # Сначала вызываем оригинал (сохраняем в истории)
            session._original_append_stdout(data)
            # Рассылаем всем подключённым клиентам
            asyncio.create_task(session_manager.broadcast(session_id, ("stdout", data)))

        def patched_append_stderr(data):
            session._original_append_stderr(data)
            asyncio.create_task(session_manager.broadcast(session_id, ("stderr", data)))

        session.history.append_stdout = patched_append_stdout
        session.history.append_stderr = patched_append_stderr
        session_manager._patched.add(session_id)

    # --- 3. Задача отправки из очереди этого клиента в его WebSocket ---
    async def send_output():
        try:
            while True:
                out_type, line = await output_queue.get()
                try:
                    await websocket.send_json({"type": out_type, "line": line})
                except (WebSocketDisconnect, RuntimeError):
                    break
        except asyncio.CancelledError:
            pass

    send_task = asyncio.create_task(send_output())

    # --- 4. Принимаем команды от клиента ---
    try:
        await websocket.accept()  # <-- перенесём accept сюда, после регистрации
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
        # Отписываем клиента
        await session_manager.unregister_queue(session_id, output_queue)


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


# =====================================================================================================================
