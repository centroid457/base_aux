import asyncio
import os
from typing import Optional
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from base_aux.cmds.m4_terminal1_os2_aio import *


# =====================================================================================================================
class ObjectManager:
    ITEM_CLASS: type[CmdTerminal_OsAio] = CmdTerminal_OsAio
    items: dict[str, CmdTerminal_OsAio]
    _last_index: int = 0

    def __init__(self):
        self.items = {}

    async def create_item(self, id: str | None = None) -> str:
        if id is None:
            self._last_index += 1
            id = f"[{self._last_index}]{self.ITEM_CLASS.get_name()}"
        if id not in self.items:
            new_item = self.ITEM_CLASS(id=id)
            self.items[id] = new_item
        return id

    async def get_item(self, id: str) -> CmdTerminal_OsAio | None:
        return self.items.get(id)

    async def del_item(self, id: str) -> None:
        item = self.items.pop(id, None)
        if item:
            await item.disconnect()


# -----------------------------------------------------------------------------------------------------------------
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
        // Глобальный менеджер обьектов
        // --------------------------------------------------------------
        const itemsManager = {
            items: new Map(),   // its a DICT=.set(itemId, itemUI)
            container_items: document.getElementById('div_items_container__id'),
            btn_AddItem: document.getElementById('btn_add_item__id'),
            socket_HealthCheck: null,
            
            async init() {
                const serverIds = await this.get_IdsServer();
                let storedIds = this.get_IdsClient();
                storedIds = storedIds.filter(id => serverIds.includes(id));
                this.set_IdsClient(storedIds);

                for (const id of storedIds) {
                    this.addItemBlock(id, false);
                }

                if (this.items.size === 0) {
                    await this.createNewItem();
                }

                this.btn_AddItem.addEventListener('click', () => this.createNewItem());
                
                this.initHealthCheck();                   // <-- вызов после всего
            },

            initHealthCheck() {
                const connect = () => {
                    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                    this.socket_HealthCheck = new WebSocket(`${protocol}//${window.location.host}/ws/ping`);
                    
                    this.socket_HealthCheck.onopen = () => {
                        document.getElementById('div_app_header__id').classList.remove('disconnected');
                    };
                    
                    this.socket_HealthCheck.onclose = () => {
                        document.getElementById('div_app_header__id').classList.add('disconnected');
                        setTimeout(() => connect(), 3000);   // переподключаемся через 3 сек
                    };
                    
                    this.socket_HealthCheck.onerror = () => {
                        document.getElementById('div_app_header__id').classList.add('disconnected');
                        this.socket_HealthCheck.close();           // инициируем закрытие, вызовется onclose
                    };
                };
                connect();
            },
    
            async get_IdsServer() {
                try {
                    const resp = await fetch('/items');
                    const data = await resp.json();
                    return data.items || [];
                } catch {
                    return [];
                }
            },

            get_IdsClient() {
                const stored = localStorage.getItem('terminal_session_ids');
                return stored ? JSON.parse(stored) : [];
            },

            set_IdsClient(ids) {
                localStorage.setItem('terminal_session_ids', JSON.stringify(ids));
            },

            async createNewItem() {
                const resp = await fetch('/items', { method: 'POST' });
                const data = await resp.json();
                const itemId = data.id;
                const stored = this.get_IdsClient();
                stored.push(itemId);
                this.set_IdsClient(stored);
                this.addItemBlock(itemId, true);
                return itemId;
            },

            addItemBlock(itemId, isNew) {
                if (this.items.has(itemId)) return;
                const itemUI = new ItemUI(itemId, this.container_items, isNew);
                // this.container_items.appendChild(itemUI.element_ItemBox); - так нельзя!!!!
                this.items.set(itemId, itemUI);
                itemUI.init();
            },

            async closeItem(itemId) {
                await fetch(`/items/${itemId}`, { method: 'DELETE' });
                const stored = this.get_IdsClient();
                const updated = stored.filter(id => id !== itemId);
                this.set_IdsClient(updated);
                
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
            constructor(itemId, container_items, isNew) {
                this.itemId = itemId;
                this.container_items = container_items; 
                this.isNew = isNew;
                
                this.socket = null;
                
                this.element_ItemBox = null;
                this.element_OutputBox = null;
                this.element_InputBox = null;
                this.element_Status = null;
            }

            init() {
                this.render();
                this.connectWebSocket();
            }

            render() {
                const div_itembox = document.createElement('div');
                div_itembox.className = 'div_itembox__style';
                div_itembox.dataset.itemId = this.itemId;

                // Header -------------------------------------------
                const div_itemheader = document.createElement('div');
                div_itemheader.className = 'div_termheader__style';
                
                const span_status = document.createElement('span');
                span_status.className = 'span_status__style';
                span_status.textContent = '⚡';
                this.element_Status = span_status;
                
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

                // Output -------------------------------------------
                const div_output = document.createElement('div');
                div_output.className = 'div_output__style';
                this.element_OutputBox = div_output;

                // Input area
                const div_input = document.createElement('div');
                div_input.className = 'div_input__style';
                
                const input_item = document.createElement('input');
                input_item.type = 'text';
                input_item.className = 'input_item__style';
                input_item.placeholder = 'Введите команду и нажмите Enter';
                this.element_InputBox = input_item;

                div_input.appendChild(input_item);

                div_itembox.appendChild(div_itemheader);
                div_itembox.appendChild(div_output);
                div_itembox.appendChild(div_input);
                
                this.element_ItemBox = div_itembox;
                this.container_items.appendChild(this.element_ItemBox); // добавляем в DOM! нельзя вынести вверх!!!!

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
                    this.element_Status.textContent = '✅';
                    if (!this.isNew) {
                        this.loadHistory();
                    }
                };
                this.socket.onmessage = (e) => {
                    const msg = JSON.parse(e.data);
                    this.addHistoryLine(msg.msg_style, msg.msg_text);
                };
                this.socket.onclose = () => {
                    this.element_Status.textContent = '❌';
                };
                this.socket.onerror = () => {
                    this.element_Status.textContent = '⚠️';
                };
            }

            sendReconnect() {
                if (this.socket?.readyState === WebSocket.OPEN) {
                    this.socket.send('/reconnect');
                }
            }

            async loadHistory() {
                // Очищаем окно перед загрузкой, чтобы избежать дублей
                this.element_OutputBox.innerHTML = '';
                try {
                    const resp = await fetch(`/items/${this.itemId}/history`);
                    const history = await resp.json();
                    history.forEach(cmd => {
                        if (cmd.input) this.addHistoryLine('msg_stdin__style', `→ ${cmd.input}`);
                        cmd.stdout?.forEach(l => this.addHistoryLine('msg_stdout__style', l));
                        cmd.stderr?.forEach(l => this.addHistoryLine('msg_stderr__style', l));
                    });
                    this.addHistoryLine('msg_system__style', '=== HISTORY ===');
                } catch (err) {
                    this.addHistoryLine('msg_stderr__style', `Ошибка loadHistory ${err.message}`);
                }
            }

            addHistoryLine(msg_style, msg_text) {
                const div_msg_line = document.createElement('div');
                div_msg_line.className = msg_style;
                div_msg_line.textContent = msg_text;
                
                this.element_OutputBox.appendChild(div_msg_line);
                this.element_OutputBox.scrollTop = this.element_OutputBox.scrollHeight;
            }

            destroy() {
                this.socket?.close();
                this.element_ItemBox?.remove();
            }
        }

        // --------------------------------------------------------------
        // Запуск
        // --------------------------------------------------------------
        window.onload = () => itemsManager.init();
        window.onbeforeunload = () => {
            itemsManager.items.forEach(s => s.socket?.close());
            if (itemsManager.socket_HealthCheck) itemsManager.socket_HealthCheck.close();
        };
    </script>
</body>
</html>
"""


# =====================================================================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Код, выполняемый ПРИ СТАРТЕ сервера (бывший startup_event) ---
    print(f"FastApi.Startup: START")
    first_id = await object_manager.create_item()
    first_item = object_manager.items.get(first_id)
    if first_item:
        print(f"FastApi.Startup: {first_id=}")
        await first_item.connect()
    # ------------------------------------------------------------------

    yield  # <-- здесь сервер работает и обрабатывает запросы

    # --- Код, выполняемый ПРИ ОСТАНОВКЕ сервера (бывший shutdown_event) ---
    for item_id, item in list(object_manager.items.items()):
        print(f"FastApi.Shutdown: {item_id=}")
        await item.disconnect()

    print(f"FastApi.Shutdown: FINISHED")
    # ---------------------------------------------------------------------


# =====================================================================================================================
app = FastAPI(title="Web Terminal", lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
async def get_html():
    return HTML_TEMPLATE


@app.get("/items")
async def list_items():
    ids = list(object_manager.items)
    return {"items": ids}


@app.post("/items")
async def create_item():
    id = await object_manager.create_item()
    return {"id": id}


@app.delete("/items/{id}")
async def del_item(id: str):
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

    # Создаём очередь для этого клиента
    client_output_queue = asyncio.Queue()

    # Создаём слушателя, который будет класть сообщения в очередь
    def listener(msg_style, msg_text):
        asyncio.create_task(client_output_queue.put((msg_style, msg_text)))

    item.history.listener__add(listener)

    # Подключаем процесс, если ещё не подключён (теперь слушатель уже есть)
    if not item._conn:
        await item.connect()

    # Задача отправки из очереди в WebSocket
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

    try:
        await websocket.accept()
        while True:
            cmd = await websocket.receive_text()
            if cmd == '/reconnect':
                await item.reconnect()
            else:
                await item.send_command(cmd)
    except WebSocketDisconnect:
        pass
    finally:
        send_task.cancel()
        await send_task
        item.history.listener__del(listener)


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


# =====================================================================================================================
