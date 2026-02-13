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
class ObjectManager:
    """
    GOAL
    ----
    controlling object collection
    """
    ITEM_CLASS: type[CmdSession_OsTerminalAio] = CmdSession_OsTerminalAio
    items: dict[str, CmdSession_OsTerminalAio]
    _last_index: int = 0

    def __init__(self):
        self.items = {}
        # Ключ: id, значение: список очередей для каждого WebSocket
        self._output_queues: dict[str, list[asyncio.Queue]] = {}
        # Флаг: был ли уже применён патч к методам истории
        self._patched: set[str] = set()

    async def create_item(self, id: Optional[str] = None) -> str:
        if id is None:
            self._last_index += 1
            id = f"[{self._last_index}]{self.ITEM_CLASS.get_name()}"
        new_item = self.ITEM_CLASS(id=id)
        self.items[id] = new_item
        self._output_queues[id] = []
        return id

    async def get_item(self, id: str) -> Optional[CmdSession_OsTerminalAio]:
        return self.items.get(id)

    async def register_queue(self, id: str, queue: asyncio.Queue) -> None:
        """Добавляет очередь для рассылки вывода."""
        if id not in self._output_queues:
            self._output_queues[id] = []
        self._output_queues[id].append(queue)

    async def unregister_queue(self, id: str, queue: asyncio.Queue) -> None:
        """Удаляет очередь и, если она последняя, восстанавливает оригинальные методы."""
        queues = self._output_queues.get(id)
        if queues and queue in queues:
            queues.remove(queue)
        # Если больше нет клиентов – восстанавливаем оригинальные методы истории
        if id in self.items and not queues:
            object_item = self.items[id]
            if hasattr(object_item, '_original_append_stdout'):
                object_item.history.append_stdout = object_item._original_append_stdout
                object_item.history.append_stderr = object_item._original_append_stderr
                del object_item._original_append_stdout
                del object_item._original_append_stderr
            self._patched.discard(id)
            # Можно также удалить пустой список, но оставим для аккуратности
            self._output_queues[id] = []

    async def broadcast(self, id: str, msg: tuple[str, str]) -> None:
        """Разослать сообщение (тип, строка) во все очереди сессии."""
        queues = self._output_queues.get(id, [])
        for q in queues:
            await q.put(msg)

    async def close_item(self, id: str) -> None:
        """Принудительно закрывает обьект очищает очереди."""
        item = self.items.pop(id, None)
        if not item:
            return

        # Удаляем все очереди и восстанавливаем оригиналы
        self._output_queues.pop(id, None)
        if hasattr(item, '_original_append_stdout'):
            item.history.append_stdout = item._original_append_stdout
            item.history.append_stderr = item._original_append_stderr
            del item._original_append_stdout
            del item._original_append_stderr
        self._patched.discard(id)

        # Останавливаем фоновые задачи чтения
        item._stop_reading = True
        for task in item._reader_tasks:
            task.cancel()
        await asyncio.gather(*item._reader_tasks, return_exceptions=True)
        item._reader_tasks.clear()

        # Завершаем процесс
        if item._conn:
            try:
                item._conn.terminate()
                await asyncio.wait_for(item._conn.wait(), timeout=1.0)
            except asyncio.TimeoutError:
                item._conn.kill()
                await item._conn.wait()
            item._conn = None

    async def item_exists(self, id: str) -> bool:
        return id in self.items

    async def get_all_item_ids(self) -> list[str]:
        return list(self.items)


object_manager = ObjectManager()


# =====================================================================================================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Web Terminal</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: monospace;
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            margin: 0;
        }
        #div_app_header__id {
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
        #btn_add_item__id {
            background: #0e639c;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
        #btn_add_item__id:hover { background: #1177bb; }
        
        #div_items_container__id {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .div_itembox__style {
            background: #2d2d2d;
            border: 1px solid #444;
            border-radius: 6px;
            position: relative;
            display: flex;
            flex-direction: column;
        }
        
        .div_termheader__style {
            background: #3c3c3c;
            padding: 8px 12px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #555;
        }
        .span_itemid__style {
            font-weight: bold;
            color: #9cdcfe;
            font-size: 14px;
        }
        
        .btn_reconnect__style {
            background: #0e639c;
            color: white;
            border: none;
            padding: 4px 10px;
            margin-left: 8px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
        }
        .btn_reconnect__style:hover { background: #1177bb; }
        
        .btn_close__style {
            background: transparent;
            border: none;
            color: #f48771;
            font-size: 18px;
            cursor: pointer;
            padding: 0 6px;
            border-radius: 4px;
        }
        .btn_close__style:hover {
            background: #f48771;
            color: #1e1e1e;
        }
        
        .div_output__style {
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
        .div_input__style {
            display: flex;
            padding: 10px;
            background: #2d2d2d;
        }
        .input_item__style{
            flex: 1;
            padding: 8px;
            font-size: 14px;
            background: #3c3c3c;
            color: #fff;
            border: 1px solid #555;
            border-radius: 4px;
            font-family: monospace;
        }
        .input_item__style:focus {
            outline: none;
            border-color: #0e639c;
        }
        .span_status__style {
            margin-left: 10px;
            font-size: 12px;
            color: #888;
        }
    </style>
</head>
<body>
    <div id="div_app_header__id">
        <h1>🔌 Web Terminal</h1>
        <button id="btn_add_item__id">➕ Новый объект</button>
    </div>
    <div id="div_items_container__id"></div>

    <script>
        // --------------------------------------------------------------
        // Глобальный менеджер сессий
        // --------------------------------------------------------------
        const itemsManager = {
            items: new Map(),
            container: document.getElementById('div_items_container__id'),
            addItemBtn: document.getElementById('btn_add_item__id'),

            async init() {
                const serverIds = await this.fetchServerItems();
                let storedIds = this.loadStoredIds();
                storedIds = storedIds.filter(id => serverIds.includes(id));
                this.saveStoredIds(storedIds);

                for (const id of storedIds) {
                    this.addItemBlock(id, false);
                }

                if (this.items.size === 0) {
                    await this.createNewItem();
                }

                this.addItemBtn.addEventListener('click', () => this.createNewItem());
            },

            async fetchServerItems() {
                try {
                    const resp = await fetch('/items');
                    const data = await resp.json();
                    return data.items || [];
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

            async createNewItem() {
                const resp = await fetch('/items', { method: 'POST' });
                const data = await resp.json();
                const itemId = data.id;
                const stored = this.loadStoredIds();
                stored.push(itemId);
                this.saveStoredIds(stored);
                this.addItemBlock(itemId, true);
                return itemId;
            },

            addItemBlock(itemId, isNew) {
                if (this.items.has(itemId)) return;
                const itemUI = new ItemUI(itemId, this.container, isNew);
                this.items.set(itemId, itemUI);
                itemUI.init();
            },

            async closeItem(itemId) {
                await fetch(`/items/${itemId}`, { method: 'DELETE' });
                const stored = this.loadStoredIds();
                const updated = stored.filter(id => id !== itemId);
                this.saveStoredIds(updated);
                
                const itemUI = this.items.get(itemId);
                if (itemUI) {
                    itemUI.destroy();
                    this.items.delete(itemId);
                }

                if (this.items.size === 0) {
                    await this.createNewItem();
                }
            }
        };

        // --------------------------------------------------------------
        // Класс одного item
        // --------------------------------------------------------------
        class ItemUI {
            constructor(itemId, container, isNew) {
                this.itemId = itemId;
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
                const div_itembox = document.createElement('div');
                div_itembox.className = 'div_itembox__style';
                div_itembox.dataset.itemId = this.itemId;

                // Header
                const div_itemheader = document.createElement('div');
                div_itemheader.className = 'div_termheader__style';
                
                const span_itemid = document.createElement('span');
                span_itemid.className = 'span_itemid__style';
                span_itemid.textContent = `📟 ${this.itemId}`;
                
                const btn_reconnect = document.createElement('button');
                btn_reconnect.className = 'btn_reconnect__style';
                btn_reconnect.textContent = '🔄';
                btn_reconnect.title = 'Переподключиться';
                btn_reconnect.onclick = () => this.sendReconnect();
                
                const btn_close = document.createElement('button');
                btn_close.className = 'btn_close__style';
                btn_close.title = 'Закрыть';
                btn_close.innerHTML = '&times;';
                btn_close.onclick = () => itemsManager.closeItem(this.itemId);
                
                div_itemheader.appendChild(span_itemid);
                div_itemheader.appendChild(btn_reconnect);
                div_itemheader.appendChild(btn_close);

                // Output
                const div_output = document.createElement('div');
                div_output.className = 'div_output__style';
                this.outputElement = div_output;

                // Input area
                const div_input = document.createElement('div');
                div_input.className = 'div_input__style';
                
                const input_item = document.createElement('input');
                input_item.type = 'text';
                input_item.className = 'input_item__style';
                input_item.placeholder = 'Введите команду и нажмите Enter';
                this.inputElement = input_item;

                const span_status = document.createElement('span');
                span_status.className = 'span_status__style';
                span_status.textContent = '⚡ соединяемся...';
                this.statusElement = span_status;

                div_input.appendChild(input_item);
                div_input.appendChild(span_status);

                div_itembox.appendChild(div_itemheader);
                div_itembox.appendChild(div_output);
                div_itembox.appendChild(div_input);
                
                this.container.appendChild(div_itembox);
                this.element = div_itembox;

                input_item.addEventListener('keydown', (e) => {
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
                const wsUrl = `${protocol}//${window.location.host}/ws/${this.itemId}`;
                this.socket = new WebSocket(wsUrl);

                this.socket.onopen = () => {
                    this.statusElement.textContent = '✅';
                    if (!this.isNew) this.loadHistory();
                };
                this.socket.onmessage = (e) => {
                    const msg = JSON.parse(e.data);
                    this.addOutputLine(msg.type, msg.line);
                };
                this.socket.onclose = () => {
                    this.statusElement.textContent = '❌';
                };
                this.socket.onerror = () => {
                    this.statusElement.textContent = '⚠️';
                };
            }

            sendReconnect() {
                if (this.socket?.readyState === WebSocket.OPEN) {
                    this.socket.send('/reconnect');
                }
            }

            async loadHistory() {
                try {
                    const resp = await fetch(`/items/${this.itemId}/history`);
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
        window.onload = () => itemsManager.init();
        window.onbeforeunload = () => {
            itemsManager.items.forEach(s => s.socket?.close());
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


@app.post("/items")
async def create_item():
    id = await object_manager.create_item()
    return {"id": id}


@app.delete("/items/{id}")
async def delete_item(id: str):
    await object_manager.close_item(id)
    return {"status": "closed"}


@app.get("/items/{id}")
async def get_item(id: str):
    exists = await object_manager.item_exists(id)
    if exists:
        return {"id": id, "active": True}
    raise HTTPException(status_code=404, detail=f"{id=}Item not found")


@app.get("/items/{id}/history")
async def get_item_history(id: str):
    session = await object_manager.get_item(id)
    if not session:
        raise HTTPException(status_code=404, detail=f"{id=}Item not found")

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


@app.get("/items")
async def list_items():
    ids = await object_manager.get_all_item_ids()
    return {"items": ids}


@app.websocket("/ws/{id}")
async def websocket_endpoint(websocket: WebSocket, id: str):
    session = await object_manager.get_item(id)
    if not session:
        await websocket.close(code=1008, reason="Invalid session")
        return

    # Подключаем процесс, если ещё не подключён
    if not session._conn:
        await session.connect()

    # --- 1. Создаём очередь для этого клиента ---
    output_queue = asyncio.Queue()
    await object_manager.register_queue(id, output_queue)

    # --- 2. Патчим методы истории (только один раз!) ---
    if id not in object_manager._patched:
        # Сохраняем оригиналы как атрибуты экземпляра сессии
        session._original_append_stdout = session.history.append_stdout
        session._original_append_stderr = session.history.append_stderr

        def patched_append_stdout(data):
            # Сначала вызываем оригинал (сохраняем в истории)
            session._original_append_stdout(data)
            # Рассылаем всем подключённым клиентам
            asyncio.create_task(object_manager.broadcast(id, ("stdout", data)))

        def patched_append_stderr(data):
            session._original_append_stderr(data)
            asyncio.create_task(object_manager.broadcast(id, ("stderr", data)))

        session.history.append_stdout = patched_append_stdout
        session.history.append_stderr = patched_append_stderr
        object_manager._patched.add(id)

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
        await object_manager.unregister_queue(id, output_queue)


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


# =====================================================================================================================
