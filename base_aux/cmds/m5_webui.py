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
    ITEM_CLASS: type[CmdTerminal_OsAio] = CmdTerminal_OsAio
    items: dict[str, CmdTerminal_OsAio]
    _last_index: int = 0

    def __init__(self):
        self.items = {}
        self._client_output_queues: dict[str, list[asyncio.Queue]] = {}
        self._patched: set[str] = set()

    # -----------------------------------------------------------------------------------------------------------------
    async def create_item(self, id: str | None = None) -> str:
        if id is None:
            self._last_index += 1
            id = f"[{self._last_index}]{self.ITEM_CLASS.get_name()}"
        if id not in self.items:
            new_item = self.ITEM_CLASS(id=id)
            self.items[id] = new_item
            self._client_output_queues[id] = []
        return id

    async def get_item(self, id: str) -> CmdTerminal_OsAio | None:
        return self.items.get(id)

    async def del_item(self, id: str) -> None:
        """Принудительно закрывает обьект очищает очереди."""
        item = self.items.pop(id, None)
        if not item:
            return

        await item.disconnect()
        self._client_output_queues.pop(id, None)
        self._patched.discard(id)

    # -----------------------------------------------------------------------------------------------------------------
    async def add__client_output_queue(self, id: str, queue: asyncio.Queue) -> None:
        """Добавляет очередь для рассылки вывода."""
        if id not in self._client_output_queues:
            self._client_output_queues[id] = []
        self._client_output_queues[id].append(queue)

    async def del__client_output_queue(self, id: str, queue: asyncio.Queue) -> None:
        """Удаляет очередь и, если она последняя, восстанавливает оригинальные методы."""
        queues = self._client_output_queues.get(id)
        if queues and queue in queues:
            queues.remove(queue)

        # Если больше нет клиентов – восстанавливаем оригинальные методы истории
        if id in self.items and not queues:
            object_item = self.items[id]
            if hasattr(object_item, '_original_append_stdout'):
                object_item.history.add_data__stdin = object_item._original_add_input
                object_item.history.add_data__stdout = object_item._original_append_stdout
                object_item.history.add_data__stderr = object_item._original_append_stderr
                del object_item._original_add_input
                del object_item._original_append_stdout
                del object_item._original_append_stderr

            self._patched.discard(id)
            # Можно также удалить пустой список, но оставим для аккуратности
            self._client_output_queues[id] = []

    # -----------------------------------------------------------------------------------------------------------------
    async def broadcast(self, id: str, msg: tuple[str, str]) -> None:
        """Разослать сообщение (тип, строка) во все очереди item."""
        client_queues = self._client_output_queues.get(id, [])
        for client_queue in client_queues:
            await client_queue.put(msg)


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
        #div_app_header__id.disconnected {
            background-color: #8b0000;      /* тёмно-красный */
            transition: background-color 0.3s;
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
            justify-content: flex-start;  /* flex-start=по порядку/ space-between=равномерно*/
            align-items: center;
            gap: 8px;                     /* отступы между всеми детьми */
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
            margin-left: auto;        /* прижимает эту кнопку вправо вместе с последующими элементами*/
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
        .msg_stdin__style  { color: #ffffff; }
        .msg_stdout__style { color: #b5cea8; }
        .msg_stderr__style { color: #f48771; }
        .msg_system__style { color: #569cd6; font-style: italic; }
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
            healthSocket: null,                          // <-- новое поле
            
            async init() {
                const serverIds = await this.fetchServerItems();
                let storedIds = this.loadStoredIds();
                storedIds = storedIds.filter(id => serverIds.includes(id));
                this.saveStoredIds(storedIds);

                for (const id of storedIds) {
                    this.addItemBlock(id);
                }

                if (this.items.size === 0) {
                    await this.createNewItem();
                }

                this.addItemBtn.addEventListener('click', () => this.createNewItem());
                
                this.initHealthCheck();                   // <-- вызов после всего
            },

            initHealthCheck() {
                const connect = () => {
                    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                    this.healthSocket = new WebSocket(`${protocol}//${window.location.host}/ws/ping`);
                    
                    this.healthSocket.onopen = () => {
                        document.getElementById('div_app_header__id').classList.remove('disconnected');
                    };
                    
                    this.healthSocket.onclose = () => {
                        document.getElementById('div_app_header__id').classList.add('disconnected');
                        setTimeout(() => connect(), 3000);   // переподключаемся через 3 сек
                    };
                    
                    this.healthSocket.onerror = () => {
                        document.getElementById('div_app_header__id').classList.add('disconnected');
                        this.healthSocket.close();           // инициируем закрытие, вызовется onclose
                    };
                };
                connect();
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
                this.addItemBlock(itemId);
                return itemId;
            },

            addItemBlock(itemId) {
                if (this.items.has(itemId)) return;
                const itemUI = new ItemUI(itemId, this.container);
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
            constructor(itemId, container) {
                this.itemId = itemId;
                this.container = container;
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
                
                const span_status = document.createElement('span');
                span_status.className = 'span_status__style';
                span_status.textContent = '⚡';
                this.statusElement = span_status;
                
                const span_itemid = document.createElement('span');
                span_itemid.className = 'span_itemid__style';
                span_itemid.textContent = `${this.itemId}`;
                
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
                
                div_itemheader.appendChild(span_status);
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

                div_input.appendChild(input_item);

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
                    this.loadHistory();
                };
                this.socket.onmessage = (e) => {
                    const msg = JSON.parse(e.data);
                    this.addOutputLine(msg.msg_style, msg.msg_text);
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
                    history.forEach(cmd => {
                        if (cmd.input) this.addOutputLine('msg_stdin__style', `→ ${cmd.input}`);
                        cmd.stdout?.forEach(l => this.addOutputLine('msg_stdout__style', l));
                        cmd.stderr?.forEach(l => this.addOutputLine('msg_stderr__style', l));
                    });
                    this.addOutputLine('msg_system__style', '=== HISTORY ===');
                } catch (err) {
                    this.addOutputLine('msg_stderr__style', `Ошибка loadHistory ${err.message}`);
                }
            }

            addOutputLine(msg_style, msg_text) {
                const div_msg = document.createElement('div');
                div_msg.className = msg_style;
                div_msg.textContent = msg_text;
                
                this.outputElement.appendChild(div_msg);
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
            if (itemsManager.healthSocket) itemsManager.healthSocket.close();
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
    await object_manager.del_item(id)
    return {"status": "closed"}


@app.get("/items/{id}")
async def get_item(id: str):
    exists = id in object_manager.items
    if exists:
        return {"id": id, "active": True}
    raise HTTPException(status_code=404, detail=f"{id=}Item not found")


@app.get("/items/{id}/history")
async def get_item_history(id: str):
    item = await object_manager.get_item(id)
    if not item:
        raise HTTPException(status_code=404, detail=f"{id=}Item not found")

    history_data = []
    for result in item.history:
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
    ids = list(object_manager.items)
    return {"items": ids}


@app.websocket("/ws/ping")
async def websocket_ping(websocket: WebSocket):
    await websocket.accept()
    try:
        # Держим соединение открытым, игнорируем входящие сообщения
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass


@app.websocket("/ws/{id}")
async def websocket_endpoint(websocket: WebSocket, id: str):
    item = await object_manager.get_item(id)
    if not item:
        await websocket.close(code=1008, reason=f"{id=}/Invalid")
        return

    # Подключаем процесс, если ещё не подключён
    if not item._conn:
        await item.connect()

    # --- 1. Создаём очередь для этого клиента ---
    client_output_queue = asyncio.Queue()
    await object_manager.add__client_output_queue(id, client_output_queue)

    # --- 2. Патчим методы истории (только один раз!) ---
    if id not in object_manager._patched:
        # Сохраняем оригиналы как атрибуты экземпляра item
        item._original_add_input = item.history.add_data__stdin
        item._original_append_stdout = item.history.add_data__stdout
        item._original_append_stderr = item.history.add_data__stderr

        def patched_append_stdout(data):
            # Сначала вызываем оригинал (сохраняем в истории)
            item._original_append_stdout(data)
            # Рассылаем всем подключённым клиентам
            asyncio.create_task(object_manager.broadcast(id, ("msg_stdout__style", data)))

        def patched_append_stderr(data):
            item._original_append_stderr(data)
            asyncio.create_task(object_manager.broadcast(id, ("msg_stderr__style", data)))

        def patched_add_input(data):
            item._original_add_input(data)
            # Добавляем префикс "→ " для единообразия с загрузкой истории
            asyncio.create_task(object_manager.broadcast(id, ("msg_stdin__style", f"→ {data}")))

        item.history.add_data__stdin = patched_add_input
        item.history.add_data__stdout = patched_append_stdout
        item.history.add_data__stderr = patched_append_stderr
        object_manager._patched.add(id)

    # --- 3. Задача отправки из очереди этого клиента в его WebSocket ---
    async def send_output():
        try:
            while True:
                msg_style, msg_text = await client_output_queue.get()
                try:
                    await websocket.send_json({"msg_style": msg_style, "msg_text": msg_text})
                except (WebSocketDisconnect, RuntimeError):
                    break
        except asyncio.CancelledError:
            pass

    send_task = asyncio.create_task(send_output())

    # --- 4. Принимаем команды от клиента ---
    try:
        await websocket.accept()
        while True:
            cmd = await websocket.receive_text()
            if cmd == '/reconnect':
                await item.reconnect()
                await websocket.send_json({"msg_style": "msg_system__style", "msg_text": "🔄 Сессия переподключена"})
            else:
                await item.send_command(cmd)
    except WebSocketDisconnect:
        pass
    finally:
        send_task.cancel()
        await send_task
        # Отписываем клиента
        await object_manager.del__client_output_queue(id, client_output_queue)


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


# =====================================================================================================================
