from base_aux.cmds.m4_terminal1_os2_aio import *

# ------------------------------------------------------------
# 1. УСТАНОВКА ПОЛИТИКИ ЦИКЛА ДЛЯ WINDOWS (самое начало!)
# ------------------------------------------------------------
import sys
import os

if os.name == "nt":
    import asyncio
    # Принудительно устанавливаем политику Proactor (необходима для подпроцессов)
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    # Для отладки – печатаем, какая политика используется
    print(f"[DEBUG] Windows: установлена политика {asyncio.get_event_loop_policy()!r}", file=sys.stderr)

# ------------------------------------------------------------
# 2. ИМПОРТЫ (все остальные)
# ------------------------------------------------------------
import asyncio
import time
import uuid
from typing import *
from datetime import datetime
from dataclasses import dataclass, field

# Эти модули должны быть доступны в вашем окружении
from base_aux.base_enums.m2_enum1_adj import EnumAdj_Buffer, EnumAdj_FinishedStatus
from base_aux.base_values.m3_exceptions import *

# ------------------------------------------------------------
# 3. ИСХОДНЫЕ КЛАССЫ (ПОЛНОСТЬЮ БЕЗ ИЗМЕНЕНИЙ)
#    Вставьте сюда всё содержимое из условия.
#    Я приведу только сигнатуры, чтобы сохранить краткость.
#    В реальном файле должно быть полное тело классов.
# ------------------------------------------------------------
# ... (полное содержание классов CmdResult, CmdHistory, Base_CmdSession, CmdSession_OsTerminalAio)
# Убедитесь, что они в точности скопированы из условия.

# ------------------------------------------------------------
# 4. WEB‑ИНТЕГРАЦИЯ (FASTAPI + XTERM.JS)
# ------------------------------------------------------------
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

class WebTerminalSession(CmdSession_OsTerminalAio):
    """
    Наследник, отправляющий вывод через WebSocket.
    Исходные методы НЕ ПЕРЕОПРЕДЕЛЕНЫ, кроме _reading_stdout/_stderr.
    """
    def __init__(self, *, output_callback: Callable[[str, str], Awaitable[None]], **kwargs):
        super().__init__(**kwargs)
        self._output_callback = output_callback

    async def _reading_stdout(self):
        while not self._stop_reading and self._conn:
            try:
                line = await self._conn.stdout.readline()
                if not line:
                    break
                line = line.decode(self._encoding).rstrip()
                if line:
                    self.history.append_stdout(line)
                    await self._output_callback("stdout", line + "\r\n")
                self.history.set_retcode(self._conn.returncode)
            except asyncio.CancelledError:
                break
            except Exception as exc:
                msg = f"stdout reader error: {exc!r}"
                self.history.append_stderr(msg)
                await self._output_callback("stderr", msg + "\r\n")
                break

    async def _reading_stderr(self):
        while not self._stop_reading and self._conn:
            try:
                line = await self._conn.stderr.readline()
                if not line:
                    break
                line = line.decode(self._encoding).rstrip()
                if line:
                    self.history.append_stderr(line)
                    await self._output_callback("stderr", line + "\r\n")
                self.history.set_retcode(self._conn.returncode)
            except asyncio.CancelledError:
                break
            except Exception as exc:
                msg = f"stderr reader error: {exc!r}"
                self.history.append_stderr(msg)
                await self._output_callback("stderr", msg + "\r\n")
                break

app = FastAPI(title="Web Terminal UI")

# ------------------------------------------------------------
# 5. HTML ШАБЛОН (xterm.js)
# ------------------------------------------------------------
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Web Terminal (Windows)</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/xterm@5.3.0/css/xterm.css" />
    <style>
        body { margin: 0; padding: 20px; background: #1e1e1e; color: #fff; font-family: monospace; }
        #terminal-container { height: 80vh; width: 100%; }
        .status { padding: 8px; background: #333; margin-bottom: 10px; border-radius: 4px; color: #0f0; }
        button { background: #007acc; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
        button:hover { background: #005a9e; }
    </style>
</head>
<body>
    <h2>🔌 Web Terminal (Windows + FastAPI)</h2>
    <div class="status" id="status">⏳ Подключение...</div>
    <div id="terminal-container"></div>
    <div style="margin-top: 20px;">
        <button onclick="clearTerminal()">Очистить</button>
        <button onclick="reconnect()">Переподключить</button>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/xterm@5.3.0/lib/xterm.js"></script>
    <script>
        let term, socket;
        let reconnectAttempt = 0, maxAttempts = 5;
        let currentLine = '';

        function initTerminal() {
            term = new Terminal({
                cursorBlink: true,
                theme: { background: '#1e1e1e', foreground: '#f0f0f0' },
                fontSize: 14,
                fontFamily: 'Menlo, Consolas, monospace',
                rows: 25, cols: 100
            });
            term.open(document.getElementById('terminal-container'));
            term.writeln('\\x1b[32m=== Добро пожаловать в Web Terminal ===\\x1b[0m');
            term.writeln('Введите команду и нажмите Enter...\\r\\n');

            term.onData(data => {
                if (!socket || socket.readyState !== WebSocket.OPEN) return;

                if (data === '\\r') { // Enter
                    socket.send(JSON.stringify({ type: 'command', data: currentLine }));
                    currentLine = '';
                } else if (data === '\\x7f' || data === '\\b') { // Backspace
                    if (currentLine.length > 0) {
                        currentLine = currentLine.slice(0, -1);
                        term.write('\\b \\b');
                    }
                } else {
                    currentLine += data;
                    term.write(data);
                }
            });
        }

        function connectWebSocket() {
            const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            socket = new WebSocket(wsProtocol + '//' + window.location.host + '/ws');

            socket.onopen = () => {
                document.getElementById('status').innerHTML = '✅ Подключено к терминалу';
                document.getElementById('status').style.color = '#0f0';
                reconnectAttempt = 0;
            };

            socket.onmessage = (event) => {
                const msg = JSON.parse(event.data);
                if (msg.type === 'output') {
                    term.write(msg.data);
                } else if (msg.type === 'status') {
                    console.log('Status:', msg.data);
                }
            };

            socket.onclose = () => {
                if (reconnectAttempt < maxAttempts) {
                    reconnectAttempt++;
                    document.getElementById('status').innerHTML = `❌ Соединение потеряно. Попытка ${reconnectAttempt}/${maxAttempts}...`;
                    document.getElementById('status').style.color = '#f00';
                    setTimeout(connectWebSocket, 3000);
                } else {
                    document.getElementById('status').innerHTML = '❌ Не удалось подключиться. Обновите страницу.';
                }
            };
        }

        function clearTerminal() { term.clear(); }
        function reconnect() { if (socket) socket.close(); connectWebSocket(); }

        window.onload = () => { initTerminal(); connectWebSocket(); };
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML_TEMPLATE

@app.websocket("/ws")
async def websocket_terminal(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"type": "status", "data": "WebSocket открыт, запуск терминала..."})

    async def send_output(stream: str, line: str):
        await websocket.send_json({"type": "output", "data": line})

    session = WebTerminalSession(output_callback=send_output)
    try:
        if not await session.connect():
            await websocket.send_json({"type": "status", "data": "ОШИБКА: не удалось запустить терминал (NotImplementedError?)"})
            await websocket.close()
            return

        await websocket.send_json({"type": "status", "data": "Терминал готов"})

        async for message in websocket.iter_json():
            if message.get("type") == "command":
                cmd = message.get("data", "").strip()
                if cmd:
                    await session.send_command(cmd)
                else:
                    await websocket.send_json({"type": "output", "data": "\r\n"})
    except WebSocketDisconnect:
        pass
    finally:
        await session.disconnect()

# ------------------------------------------------------------
# 6. ЗАПУСК (reload=False – строго!)
# ------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(
        "__main__:app",
        host="0.0.0.0",
        port=8000,
        reload=False,          # <--- ОТКЛЮЧАЕМ RELOAD
        log_level="info"
    )