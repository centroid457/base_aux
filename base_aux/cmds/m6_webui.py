import asyncio
import os
from typing import Optional
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from base_aux.cmds.m5_terminal1_os2_aio import *


# =====================================================================================================================
class ClientManager:
    """Управляет подключениями клиентов и рассылкой событий."""
    def __init__(self):
        self._queues: dict[str, asyncio.Queue] = {}

    async def register_client(self) -> tuple[str, asyncio.Queue]:
        client_id = str(uuid.uuid4())
        client_queue = asyncio.Queue()
        self._queues[client_id] = client_queue
        return client_id, client_queue

    async def unregister_client(self, client_id: str):
        self._queues.pop(client_id, None)

    async def broadcast(self, msg: dict):
        """Отправить сообщение всем клиентам."""
        for q in self._queues.values():
            await q.put(msg)


client_manager = ClientManager()


# =====================================================================================================================
class InstManager:
    ITEM_CLASS: type[CmdTerminal_OsAio] = CmdTerminal_OsAio
    items: dict[str, CmdTerminal_OsAio]

    def __init__(self):
        self.items = {}

    def get_item(self, idn: str) -> CmdTerminal_OsAio | None:
        return self.items.get(idn)

    # CMDS ----------------------------------------------
    async def clear_history(self, idn: str) -> None:
        item = self.items.get(idn)
        if not item:
            return

        item.history.clear()
        await client_manager.broadcast({
            "item_id": idn,
            "type": "item_control",
            "data": {
                "subtype": "clear_history",
            }
        })

    async def create_item(self, *args, **kwargs) -> str:
        new_item = self.ITEM_CLASS(*args, **kwargs)
        item_id = new_item.idn
        print(f"create_item:{item_id=}")
        self.items[item_id] = new_item

        await new_item.connect()

        # Глобальный слушатель – отправляет все события терминала всем клиентам
        def global_listener(msg_style, msg_text):
            # Преобразуем в единый формат: (item_id, type, data)
            # msg_style может быть 'msg_stdout__cls', 'msg_stderr__cls', 'msg_stdin__cls', 'msg_system__cls' и т.д.
            # Определяем subtype
            subtype_map = {
                'msg_stdout__cls': 'stdout',
                'msg_stderr__cls': 'stderr',
                'msg_stdin__cls': 'stdin',
                'msg_system__cls': 'system',
                'msg_debug__cls': 'debug',
            }
            subtype = subtype_map.get(msg_style, 'unknown')
            asyncio.create_task(client_manager.broadcast({
                "item_id": item_id,
                "type": "history_log",
                "data": {
                    "subtype": subtype,
                    "text": msg_text
                }
            }))

        new_item.history.listener__add(global_listener)
        # Сохраняем слушателя, чтобы потом удалить при удалении терминала
        if not hasattr(new_item, '_global_listeners'):
            new_item._global_listeners = []
        new_item._global_listeners.append(global_listener)

        # Оповещаем всех клиентов о создании нового терминала
        await client_manager.broadcast({
            "item_id": item_id,
            "type": "item_control",
            "data": {
                "subtype": "create",
            }
        })
        return item_id

    async def del_item(self, idn: str) -> None:
        item = self.items.pop(idn, None)
        if item:
            # Удаляем глобальных слушателей
            if hasattr(item, '_global_listeners'):
                for listener in item._global_listeners:
                    item.history.listener__del(listener)
            await item.disconnect()
            # Оповещаем всех клиентов об удалении
            await client_manager.broadcast({
                "item_id": idn,
                "type": "item_control",
                "data": {
                    "subtype": "delete",
                }
            })


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
    
    <link rel="stylesheet" href="/base_aux/webs_front/d1_front2_css/universal_root.css?v=<?= filemtime('/base_aux/webs_front/d1_front2_css/universal_root.css') ?>">
    <script src="/base_aux/webs_front/d2_js1_vanilla/universal_root.js?v=<?= filemtime('/base_aux/webs_front/d2_js1_vanilla/universal_root.js') ?>"></script>
    
    <style>
        /* ---------------------------------------------------------------------------------------------------------- */
        * { 
            box-sizing: border-box;
        }
        body {
            background: #111;
            color: #ddd;
        }

        /* ------------------------------------ */
        .item__cls
        {
            display: flex;
            flex-direction: column;
            
            background: #333;
            border: 1px solid #444;
            border-radius: 6px;
            
            overflow: auto;
            _resize: vertical;
        }
        .item__cls header
        {
            background: #333;
            padding: 2px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .item__cls main
        {
            background: #222;
            padding: 12px;
            height: 300px;
            _min-height: 300px;
            _max-height: 800px;
            overflow-y: scroll;
            
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: monospace;
        }
        
        .item__cls input
        {
            font-size: 14px;
            color: #fff;
            border: 1px solid #555;
            font-family: monospace;
        }
        
        /* ------------------------------------ */
        .span_item_id__cls {
            font-weight: bold;
            font-size: 14px;
        }

        /* ---------------------------------------------------------------------------------------------------------- */
    </style>
    
</head>
<body>
    <header data-auto__ping_lost>
        <h1 style="color: #fff">WebTerminal</h1>
        <div>
            <button id="btn_resync__id">resync</button>
            <button id="btn_add_item__id">Новый объект</button>
        </div>
    </header>
    <main id="items_container__id" data-gap1rem></main>
    <footer>footer</footer>
    <script>
        // --------------------------------------------------------------
        // WebSocket
        // --------------------------------------------------------------
        let ws_client = null;
    
        function ws_client__connect() {
            console.log("[WsClient]🟡try connect");
            
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws_client = new WebSocket(`${protocol}//${window.location.host}/ws/client`);
        
            // ---------------------------------------------------
            ws_client.onmessage = (e) => {
                const msg = JSON.parse(e.data);
                
                const msg__itemid = msg.item_id;
                const msg__type = msg.type;
                const msg__data = msg.data;
                
                const msg__subtype = msg__data?.subtype;
                const msg__text = msg__data?.text;
                
                if (msg__type === "history_log") {
                    const ui = itemsManager.items_map.get(msg__itemid);
                    if (ui) {
                        let style = '';
                        if (msg__subtype === 'stdout') style = 'msg_stdout__cls';
                        else if (msg__subtype === 'stderr') style = 'msg_stderr__cls';
                        else if (msg__subtype === 'stdin') style = 'msg_stdin__cls';
                        else if (msg__subtype === 'system') style = 'msg_system__cls';
                        else style = 'msg_debug__cls';
                        ui.addHistoryLine(style, msg__text);
                    }
                    
                } else if (msg__type === "item_control") {
                
                    if (msg__subtype === "create") {
                        const stored = itemsManager.get_IdsClient();
                        if (!stored.includes(msg__itemid)) {
                            stored.push(msg__itemid);
                            itemsManager.set_IdsClient(stored);
                        }
                        if (!itemsManager.items_map.has(msg__itemid)) {
                            itemsManager.addItemElement(msg__itemid);
                        }
                        
                    } else if (msg__subtype === "delete") {
                        const ui = itemsManager.items_map.get(msg__itemid);
                        if (ui) {
                            ui.destroy();
                            itemsManager.items_map.delete(msg__itemid);
                        }
                        const stored = itemsManager.get_IdsClient();
                        const updated = stored.filter(id => id !== msg__itemid);
                        itemsManager.set_IdsClient(updated);
                        
                    } else if (msg__subtype === "clear_history") {
                        const ui = itemsManager.items_map.get(msg__itemid);
                        if (ui) {
                            ui.element_OutputBox.innerHTML = '';
                        }
                    }
                    
                } else if (msg__type === "system") {
                    console.log(msg__text);
                }
            };
    
            // ---------------------------------------------------
            ws_client.onopen = async () => {
                console.log("[WsClient]🟢connected");
                await syncWithServer();   // синхронизация после восстановления
            };
    
            ws_client.onclose = () => {
                console.log("[WsClient]🔴closed, reconnecting in 3s...");
                setTimeout(ws_client__connect, 3000);
            };
        }
    
        // --------------------------------------------------------------
        // Синхронизация после переподключения сокета
        // --------------------------------------------------------------
        async function syncWithServer() {
            const serverIds = await itemsManager.get_IdsServer();
            const localIds = Array.from(itemsManager.items_map.keys());
        
            // 1. Удаляем локальные терминалы, которых нет на сервере
            for (const id of localIds) {
                if (!serverIds.includes(id)) {
                    const ui = itemsManager.items_map.get(id);
                    if (ui) ui.destroy();
                    itemsManager.items_map.delete(id);
                }
            }
        
            // 2. Добавляем терминалы, которые есть на сервере, но отсутствуют локально
            for (const id of serverIds) {
                if (!itemsManager.items_map.has(id)) {
                    itemsManager.addItemElement(id);
                }
            }
        
            // 3. Обновляем localStorage
            itemsManager.set_IdsClient(serverIds);
        }
        
        document.getElementById('btn_resync__id').addEventListener('click', () => syncWithServer());

        // --------------------------------------------------------------
        // Глобальный менеджер объектов
        // --------------------------------------------------------------
        const itemsManager = {
            items_map: new Map(),
            
            // Инициализация UI через REST (вызывается один раз при загрузке страницы)
            async initUI() {
                const serverIds = await this.get_IdsServer();
                this.set_IdsClient(serverIds);
                for (const idn of serverIds) {
                    this.addItemElement(idn);
                }
                document.getElementById('btn_add_item__id').addEventListener('click', () => this.createNewItem());
            },
            
            addItemElement(itemId) {
                if (this.items_map.has(itemId)) return;
                const itemUI = new ItemUI(itemId);
                this.items_map.set(itemId, itemUI);
                itemUI.init();
            },
            
            // ---------------------------------------------------
            async get_IdsServer() {
                try {
                    const resp = await fetch('/item/list');
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
    
            // ---------------------------------------------------
            async createNewItem() {
                if (ws_client?.readyState !== WebSocket.OPEN) return;

                ws_client.send(JSON.stringify({
                    type: "item_control",
                    data: {
                        subtype: "create_item",
                    },
                }));
            },
    
            async delItem(itemId) {
                if (ws_client?.readyState !== WebSocket.OPEN) return;

                ws_client.send(JSON.stringify({
                    item_id: itemId,
                    type: "item_control",
                    data: {
                        subtype: "delete_item",
                    },
                }));
            }
        };

        // --------------------------------------------------------------
        // объект
        // --------------------------------------------------------------
        class ItemUI {
            constructor(itemId) {
                this.itemId = itemId;
                this.element_ItemBox = null;
                this.element_OutputBox = null;
                this.element_InputBox = null;
            }
    
            init() {
                this.render();
                this.loadHistory();
            }
    
            render() {
                const div_itembox = document.createElement('div');
                div_itembox.className = 'item__cls';
    
                // Header
                const header = document.createElement('header');
                const header_div1 = document.createElement('div');
                const header_div2 = document.createElement('div');
                header.appendChild(header_div1);
                header.appendChild(header_div2);
    
                const spanId = document.createElement('span');
                spanId.className = 'span_item_id__cls';
                spanId.textContent = this.itemId;
                header_div1.appendChild(spanId);
    
                const btnClear = document.createElement('button');
                btnClear.setAttribute('data-btn_blue_outline', "");
                btnClear.textContent = 'clear';
                btnClear.title = 'Clear History';
                btnClear.onclick = () => this.sendDelHistory();
                
                const btnReconnect = document.createElement('button');
                btnReconnect.setAttribute('data-btn_blue_outline', "");
                btnReconnect.textContent = '🔄';
                btnReconnect.title = 'Reconnect';
                btnReconnect.onclick = () => this.sendReconnect();
                
                const btnClose = document.createElement('button');
                btnClose.setAttribute('data-btn_red_outline', "");
                btnClose.textContent = 'X';
                btnClose.title = 'Close';
                btnClose.onclick = () => itemsManager.delItem(this.itemId);
                
                header_div2.appendChild(btnClear);
                header_div2.appendChild(btnReconnect);
                header_div2.appendChild(btnClose);
    
                // Output area
                const output = document.createElement('main');
                output.setAttribute('data-scrollbar__dark', '');
                this.element_OutputBox = output;
    
                // Input area
                const footer = document.createElement('footer');
                const input = document.createElement('input');
                input.type = 'text';
                input.placeholder = 'Введите команду и нажмите Enter';
                this.element_InputBox = input;
                footer.appendChild(input);
    
                div_itembox.appendChild(header);
                div_itembox.appendChild(output);
                div_itembox.appendChild(footer);
                this.element_ItemBox = div_itembox;
                document.getElementById('items_container__id').appendChild(div_itembox);
    
                input.addEventListener('change', () => this.sendInput());
            }
    
            // ---------------------------------------------------
            sendInput() {
                if (ws_client?.readyState !== WebSocket.OPEN) return;
                
                const io_line = this.element_InputBox.value.trim();
                if (io_line) {
                    ws_client.send(JSON.stringify({
                        item_id: this.itemId,
                        type: "history_log",
                        data: {
                            subtype: "stdin",  // FIXME: or just stdin/msg_stdin__cls
                            text: io_line,
                        }
                    }));
                    this.element_InputBox.value = '';
                }
            }
            
            sendReconnect() {
                if (ws_client?.readyState !== WebSocket.OPEN) return;
                
                ws_client.send(JSON.stringify({
                    item_id: this.itemId,
                    type: "item_control",
                    data: {
                        subtype: "reconnect_item",
                    },
                }));
            }
    
            sendDelHistory() {
                if (ws_client?.readyState !== WebSocket.OPEN) return;

                ws_client.send(JSON.stringify({
                    item_id: this.itemId,
                    type: "item_control",
                    data: {
                        subtype: "clear_history",
                    },
                }));
            }
    
            // ---------------------------------------------------
            async loadHistory() {
                this.element_OutputBox.innerHTML = '';
                try {
                    const resp = await fetch(`/item/history/get/${this.itemId}`);
                    const history = await resp.json();
                    history.forEach(log_line => {
                        if (log_line.input) this.addHistoryLine('msg_stdin__cls', `→ ${log_line.input}`);
                        log_line.stdout?.forEach(l => this.addHistoryLine('msg_stdout__cls', l));
                        log_line.stderr?.forEach(l => this.addHistoryLine('msg_stderr__cls', l));
                        log_line.debug?.forEach(l => this.addHistoryLine('msg_debug__cls', l));
                    });
                } catch (err) {
                    this.addHistoryLine('msg_stderr__cls', `Ошибка loadHistory: ${err.message}`);
                }
            }
    
            addHistoryLine(style_cls, text) {
                const line = document.createElement('div');
                line.className = style_cls;
                line.textContent = text;
                this.element_OutputBox.appendChild(line);
                this.element_OutputBox.scrollTop = this.element_OutputBox.scrollHeight;
            }
    
            // ---------------------------------------------------
            destroy() {
                this.element_ItemBox?.remove();
            }
        }
    
        // --------------------------------------------------------------
        // Запуск
        // --------------------------------------------------------------
        window.onload = async () => {
            await itemsManager.initUI();    // первичная загрузка через REST
            ws_client__connect();           // запуск коннетка сокета
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

# Уникальный идентификатор сервера: можно использовать время запуска
server_id = str(int(asyncio.get_event_loop().time()))


# ---------------------------------------------------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def html__root():
    return HTML_TEMPLATE


@app.get("/item/list")
async def list_items():
    ids = list(object_manager.items)
    return {"items": ids}

# ---------------------------------------------------------------------------------------------------------------------
@app.get("/item/history/get/{idn}")
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

    # При подключении отправляем клиенту идентификатор сервера
    await websocket.send_json({"type": "server_id", "id": server_id})

    try:
        # Держим соединение открытым, игнорируем входящие сообщения
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        pass


# ---------------------------------------------------------------------------------------------------------------------
@app.websocket("/ws/client")
async def ws__client(websocket: WebSocket):
    await websocket.accept()

    client_id, client_queue = await client_manager.register_client()

    # --------------------------------------------
    # WS-1=WRITER = задача перенаправления событий из очереди в WebSocket
    async def ws_sender():
        try:
            while True:
                msg = await client_queue.get()
                await websocket.send_json(msg)
        except asyncio.CancelledError:
            pass

    send_task = asyncio.create_task(ws_sender())

    # --------------------------------------------
    # WS-2=READER
    try:
        while True:
            msg = await websocket.receive_json()

            msg__type = msg.get("type")
            msg__itemid = msg.get("item_id")
            msg__data = msg.get("data")

            if msg__data:
                msg__subtype = msg__data.get("subtype")
                msg__text = msg__data.get("text")
            else:
                msg__subtype = None
                msg__text = None

            # ----------------------------------------------
            if msg__type == "history_log":   # keep here

                item = object_manager.get_item(msg__itemid)
                if item and msg__text:
                    asyncio.create_task(item.send_cmd(msg__text))

            elif msg__type == "item_control" and msg__data:
                if msg__subtype == "clear_history":
                    asyncio.create_task(object_manager.clear_history(msg__itemid))

                elif msg__subtype == "reconnect_item":
                    item = object_manager.get_item(msg__itemid)
                    asyncio.create_task(item.reconnect())

                elif msg__subtype == "create_item":
                    asyncio.create_task(object_manager.create_item())

                elif msg__subtype == "delete_item":
                    asyncio.create_task(object_manager.del_item(msg__itemid))

        # --------------------------------------------
    except WebSocketDisconnect:
        pass
    finally:
        send_task.cancel()
        await send_task
        await client_manager.unregister_client(client_id)


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=80)


# =====================================================================================================================
