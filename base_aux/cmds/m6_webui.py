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

from base_aux.cmds.m5_terminal1_os2_aio import *


# =====================================================================================================================
class InstManager:
    ITEM_CLASS: type[CmdTerminal_OsAio] = CmdTerminal_OsAio
    items: dict[str, CmdTerminal_OsAio]

    def __init__(self):
        self.items = {}

    async def create_item(self, *args, **kwargs) -> str:
        new_item = self.ITEM_CLASS(*args, **kwargs)
        item_id = new_item.idn
        print(f"create_item:{item_id=}")
        self.items[item_id] = new_item
        return item_id

    def get_item(self, idn: str) -> CmdTerminal_OsAio | None:
        return self.items.get(idn)

    async def del_item(self, idn: str) -> None:
        item = self.items.pop(idn, None)
        if item:
            await item.disconnect()

    def clear_history(self, idn: str) -> None:
        item = self.items.get(idn)
        if item:
            item.history.clear()


# -----------------------------------------------------------------------------------------------------------------
object_manager = InstManager()


# TODO:
#  separate js into file
#  create full html in js


# =====================================================================================================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>WebTerminal</title>
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
        [data-auto__ping_lost="1"] {
            background: #f00;
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
        .div_itembox__cls {
            background: #2d2d2d;
            border: 1px solid #444;
            border-radius: 6px;
            position: relative;
            display: flex;
            flex-direction: column;
        }
        
        .div_termheader__cls {
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
        .span_itemid__cls {
            font-weight: bold;
            color: #9cdcfe;
            font-size: 14px;
        }
        
        
        
        
        
        
        
        
        .btn_common__cls {
            background: #0e639c;
            color: white;
            border: none;
            padding: 4px 10px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
            margin-left: auto;        /* прижимает эту кнопку вправо вместе с последующими элементами*/
        }
        .btn_common__cls:hover { background: #1177bb; }
        
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
        .msg_debug__style { color: #569cd6; font-style: italic; }
        
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
    
    <link rel="stylesheet" href="/base_aux/webs_front/d1_front2_css/universal_root.css?v=<?= filemtime('/base_aux/webs_front/d1_front2_css/universal_root.css') ?>">
    <script src="/base_aux/webs_front/d2_js1_vanilla/universal_root.js?v=<?= filemtime('/base_aux/webs_front/d2_js1_vanilla/universal_root.js') ?>"></script>
    
</head>
<body>
    <div id="div_app_header__id" data-auto__ping_lost>
        <h1>WebTerminal</h1>
        <button id="btn_add_item__id">➕ Новый объект</button>
    </div>
    <div id="div_items_container__id"></div>

    <script>
        // --------------------------------------------------------------
        // Глобальный менеджер обьектов
        // --------------------------------------------------------------
        const itemsManager = {
            items_map: new Map(),   // its a DICT=.set(itemId, itemUI)
            
            async init() {
                const serverIds = await this.get_IdsServer();

                for (const idn of serverIds) {
                    this.addItemBlock(idn, false);
                }

                if (this.items_map.size === 0) {
                    await this.createNewItem();
                }

                btn_add_item__id.addEventListener('click', () => this.createNewItem());
            },
    
            async get_IdsServer() {
                try {
                    const resp = await fetch('/items');
                    const data = await resp.json();
                    return data.items || [];
                } catch (exc) {
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
                const itemId = data.idn;
                const stored = this.get_IdsClient();
                stored.push(itemId);
                this.set_IdsClient(stored);
                this.addItemBlock(itemId, true);
                return itemId;
            },

            addItemBlock(itemId, isNew) {
                if (this.items_map.has(itemId)) return;
                const itemUI = new ItemUI(itemId, isNew);
                // div_items_container__id.appendChild(itemUI.element_ItemBox);   // так нельзя!!!!
                this.items_map.set(itemId, itemUI);
                itemUI.init();
            },

            async closeItem(itemId) {
                await fetch(`/items/${itemId}`, { method: 'DELETE' });
                const stored = this.get_IdsClient();
                const updated = stored.filter(idn => idn !== itemId);
                this.set_IdsClient(updated);
                
                const itemUI = this.items_map.get(itemId);
                if (itemUI) {
                    itemUI.destroy();
                    this.items_map.delete(itemId);
                }

                if (this.items_map.size === 0) {
                    await this.createNewItem();
                }
            }
        };

        // --------------------------------------------------------------
        // Класс одного item
        // --------------------------------------------------------------
        class ItemUI {
            constructor(itemId, isNew) {
                this.itemId = itemId;
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
                div_itembox.className = 'div_itembox__cls';
                div_itembox.dataset.itemId = this.itemId;

                // Header -------------------------------------------
                const div_itemheader = document.createElement('div');
                div_itemheader.className = 'div_termheader__cls';
                
                const span_status = document.createElement('span');
                span_status.className = 'span_status__style';
                span_status.textContent = '⚡';
                this.element_Status = span_status;
                
                const span_itemid = document.createElement('span');
                span_itemid.className = 'span_itemid__cls';
                span_itemid.textContent = `${this.itemId}`;
                
                const btn_clear_history = document.createElement('button');
                btn_clear_history.className = 'btn_common__cls';
                btn_clear_history.textContent = 'clear';
                btn_clear_history.title = 'ClearHistory';
                btn_clear_history.onclick = () => this.sendDelHistory();
                
                const btn_reconnect = document.createElement('button');
                btn_reconnect.className = 'btn_common__cls';
                btn_reconnect.textContent = '🔄';
                btn_reconnect.title = 'Reconnect';
                btn_reconnect.onclick = () => this.sendReconnect();
                
                const btn_close = document.createElement('button');
                btn_close.className = 'btn_close__style';
                btn_close.title = 'Закрыть';
                btn_close.innerHTML = '&times;';
                btn_close.onclick = () => itemsManager.closeItem(this.itemId);
                
                div_itemheader.appendChild(span_status);
                div_itemheader.appendChild(span_itemid);
                div_itemheader.appendChild(btn_clear_history);
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
                
                div_items_container__id.appendChild(this.element_ItemBox); // добавляем в DOM! нельзя вынести вверх!!!!

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
                    //this.loadHistory();
                    
                    if (this.element_OutputBox && this.element_OutputBox.innerHTML == "") {
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
                    this.socket.send('cmd_reconnect');
                }
            }
            
            sendDelHistory() {
                this.element_OutputBox.innerHTML = '';
            
                if (this.socket?.readyState === WebSocket.OPEN) {
                    this.socket.send('cmd_sendDelHistory');
                }
            }

            async loadHistory() {
                // Очищаем окно перед загрузкой, чтобы избежать дублей
                this.element_OutputBox.innerHTML = '';
                try {
                    const resp = await fetch(`/items/history/${this.itemId}`);
                    const history = await resp.json();
                    history.forEach(cmd => {
                        if (cmd.input) this.addHistoryLine('msg_stdin__style', `→ ${cmd.input}`);
                        cmd.stdout?.forEach(l => this.addHistoryLine('msg_stdout__style', l));
                        cmd.stderr?.forEach(l => this.addHistoryLine('msg_stderr__style', l));
                        cmd.debug?.forEach(l => this.addHistoryLine('msg_debug__style', l));
                    });
                    this.addHistoryLine('msg_debug__style', '=== HISTORY ===');
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
            itemsManager.items_map.forEach(s => s.socket?.close());
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
    first_item = object_manager.get_item(first_id)
    if first_item:
        await first_item.connect()
    # ------------------------------------------------------------------

    yield  # <-- здесь сервер работает и обрабатывает запросы

    # --- Код, выполняемый ПРИ ОСТАНОВКЕ сервера (бывший shutdown_event) ---
    for item_id, item in object_manager.items.items():
        print(f"FastApi.Shutdown: {item_id=}")
        await item.disconnect()

    print(f"FastApi.Shutdown: FINISHED")
    # ---------------------------------------------------------------------


# =====================================================================================================================
app = FastAPI(title="WebTerminal", lifespan=lifespan)
app.mount("/base_aux", StaticFiles(directory="../"), name="base_aux")


# ---------------------------------------------------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def html__root():
    return HTML_TEMPLATE


@app.get("/items")
async def list_items():
    ids = list(object_manager.items)
    return {"items": ids}


# ---------------------------------------------------------------------------------------------------------------------
@app.post("/items")
async def create_item():
    idn = await object_manager.create_item()
    return {"idn": idn}


@app.delete("/items/{idn}")
async def del_item(idn: str):
    await object_manager.del_item(idn)
    return {"status": "closed"}


@app.get("/items/{idn}")
async def get_item(idn: str):
    if idn in object_manager.items:
        return {"idn": idn, }
    raise HTTPException(status_code=404, detail=f"[{idn=}]Item not found")


# ---------------------------------------------------------------------------------------------------------------------
@app.delete("/items/history/{idn}")
async def del_history(idn: str):
    object_manager.clear_history(idn)
    return {"status": "closed"}


@app.get("/items/history/{idn}")
async def get_history(idn: str):
    item = object_manager.get_item(idn)
    if not item:
        raise HTTPException(status_code=404, detail=f"[{idn=}]Item not found")

    history_data: list[dict] = []
    for result in item.history:
        history_data.append({
            "input": result.INPUT,
            "stdout": result.STDOUT,
            "stderr": result.STDERR,
            "debug": result.DEBUG,
            "timestamp": result.timestamp.isoformat() if result.timestamp else None,
            "duration": result.duration,
            "finished_status": result.finished_status.value if result.finished_status else None,
            "retcode": result.retcode
        })
    return history_data


# =====================================================================================================================
@app.websocket("/ws/ping")
async def ws__ping(websocket: WebSocket):
    await websocket.accept()
    try:
        # Держим соединение открытым, игнорируем входящие сообщения
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass


# ---------------------------------------------------------------------------------------------------------------------
@app.websocket("/ws/{idn}")
async def ws__endpoint(websocket: WebSocket, idn: str):
    item = object_manager.get_item(idn)
    if not item:
        await websocket.close(code=1008, reason=f"{idn=}/Invalid")
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
            if cmd == 'cmd_reconnect':
                await item.reconnect()
            else:
                await item.send_cmd(cmd)
    except WebSocketDisconnect:
        pass
    finally:
        send_task.cancel()
        await send_task
        item.history.listener__del(listener)


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=80)


# =====================================================================================================================
