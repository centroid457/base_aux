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

    async def register_client(self, client_id: str, queue: asyncio.Queue):
        self._queues[client_id] = queue

    async def unregister_client(self, client_id: str):
        self._queues.pop(client_id, None)

    async def broadcast(self, message: dict):
        """Отправить сообщение всем клиентам."""
        for q in self._queues.values():
            await q.put(message)

    async def send_to_client(self, client_id: str, message: dict):
        q = self._queues.get(client_id)
        if q:
            await q.put(message)


client_manager = ClientManager()


# =====================================================================================================================
class InstManager:
    ITEM_CLASS: type[CmdTerminal_OsAio] = CmdTerminal_OsAio
    items: dict[str, CmdTerminal_OsAio]

    def __init__(self):
        self.items = {}

    def get_item(self, idn: str) -> CmdTerminal_OsAio | None:
        return self.items.get(idn)

    def clear_history(self, idn: str) -> None:
        item = self.items.get(idn)
        if item:
            item.history.clear()

    # new ------
    async def create_item(self, *args, **kwargs) -> str:
        # new_item = self.ITEM_CLASS(*args, **kwargs)
        # item_id = new_item.idn
        # print(f"create_item:{item_id=}")
        # self.items[item_id] = new_item
        # return item_id

        new_item = self.ITEM_CLASS(*args, **kwargs)
        item_id = new_item.idn
        print(f"create_item:{item_id=}")
        self.items[item_id] = new_item

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
                "type": "history",
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
            "type": "control",
            "data": {
                "subtype": "create",
                "item_id": item_id
            }
        })
        return item_id

    async def del_item(self, idn: str) -> None:
        # item = self.items.pop(idn, None)
        # if item:
        #     await item.disconnect()

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
                "type": "control",
                "data": {
                    "subtype": "delete",
                    "item_id": idn
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
        <button id="btn_add_item__id">Новый объект</button>
    </header>
    <main id="items_container__id" data-gap1rem></main>
    <footer>footer</footer>

    <script>
        // NEW ---------------
        // Глобальный WebSocket
        let globalSocket = null;
        let clientId = null; // если нужно
        
        function connectGlobalWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            globalSocket = new WebSocket(`${protocol}//${window.location.host}/ws/client`);
        
            globalSocket.onopen = () => {
                console.log("Global WebSocket connected");
                // После соединения можно запросить начальный список терминалов через REST (как и раньше)
                itemsManager.init(); // но init уже должен быть вызван один раз
            };
        
            globalSocket.onmessage = (e) => {
                const msg = JSON.parse(e.data);
                // msg = { item_id, type, data }
                if (msg.type === "history") {
                    const ui = itemsManager.items_map.get(msg.item_id);
                    if (ui) {
                        const subtype = msg.data.subtype;
                        const text = msg.data.text;
                        let style = '';
                        if (subtype === 'stdout') style = 'msg_stdout__cls';
                        else if (subtype === 'stderr') style = 'msg_stderr__cls';
                        else if (subtype === 'stdin') style = 'msg_stdin__cls';
                        else if (subtype === 'system') style = 'msg_system__cls';
                        else style = 'msg_debug__cls';
                        ui.addHistoryLine(style, text);
                    }
                } else if (msg.type === "control") {
                    if (msg.data.subtype === "create") {
                        const newId = msg.data.item_id;
                        if (!itemsManager.items_map.has(newId)) {
                            itemsManager.addItem(newId);
                        }
                    } else if (msg.data.subtype === "delete") {
                        const delId = msg.data.item_id;
                        const ui = itemsManager.items_map.get(delId);
                        if (ui) {
                            ui.destroy();
                            itemsManager.items_map.delete(delId);
                        }
                    }
                } else if (msg.type === "system") {
                    // например, подтверждение очистки истории
                    console.log(msg.data.text);
                }
            };
        
            globalSocket.onclose = () => {
                console.log("Global WebSocket closed, reconnecting in 3s...");
                setTimeout(connectGlobalWebSocket, 3000);
            };
        }
    
    
    
        // --------------------------------------------------------------
        // Глобальный менеджер обьектов
        // --------------------------------------------------------------
        const itemsManager = {
            items_map: new Map(),
            
            async init() {
                const serverIds = await this.get_IdsServer();

                for (const idn of serverIds) {
                    this.addItem(idn);
                }

                btn_add_item__id.addEventListener('click', () => this.createNewItem());
            },
    
            async get_IdsServer() {
                try {
                    const resp = await fetch('/item/list');
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
                const resp = await fetch('/item/create', { method: 'POST' });
                const data = await resp.json();
                const itemId = data.idn;
                const stored = this.get_IdsClient();
                stored.push(itemId);
                this.set_IdsClient(stored);
                this.addItem(itemId);
                return itemId;
            },

            addItem(itemId) {
                if (this.items_map.has(itemId)) return;
                
                const item_new = new ItemUI(itemId);
                // items_container__id.appendChild(item_new.element_ItemBox);   // так нельзя!!!!
                this.items_map.set(itemId, item_new);
                item_new.init();
            },

            async delItem(itemId) {
                await fetch(`/item/del/${itemId}`, { method: 'DELETE' });
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
            constructor(itemId) {
                this.itemId = itemId;
                // this.socket = null; // больше не требуется!
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
                div_itembox.className = 'item__cls';

                // HEADER -------------------------------------------
                const item_header = document.createElement('header');
                const item_header_div1 = document.createElement('div');
                const item_header_div2 = document.createElement('div');
                
                item_header.appendChild(item_header_div1);
                item_header.appendChild(item_header_div2);
                
                // -------------------------------------------
                const span_status = document.createElement('span');
                span_status.textContent = '⚡';
                this.element_Status = span_status;
                
                const span_itemid = document.createElement('span');
                span_itemid.className = 'span_item_id__cls';
                span_itemid.textContent = `${this.itemId}`;
                
                item_header_div1.appendChild(span_status);
                item_header_div1.appendChild(span_itemid);
                
                // -------------------------------------------
                const btn_clear_history = document.createElement('button');
                btn_clear_history.className = 'button_blue_outline__cls';
                btn_clear_history.textContent = 'clear';
                btn_clear_history.title = 'ClearHistory';
                btn_clear_history.onclick = () => this.sendDelHistory();
                
                const btn_reconnect = document.createElement('button');
                btn_reconnect.className = 'button_blue_outline__cls';
                btn_reconnect.textContent = '🔄';
                btn_reconnect.title = 'Reconnect';
                btn_reconnect.onclick = () => this.sendReconnect();
                
                const btn_close = document.createElement('button');
                btn_close.className = 'button_red_outline__cls';
                btn_close.title = 'Закрыть';
                btn_close.textContent = 'X';
                btn_close.onclick = () => itemsManager.delItem(this.itemId);

                item_header_div2.appendChild(btn_clear_history);
                item_header_div2.appendChild(btn_reconnect);
                item_header_div2.appendChild(btn_close);
                
                // MAIN -------------------------------------------
                const item_main = document.createElement('main');
                item_main.setAttribute("data-scrollbar__dark", "");
                this.element_OutputBox = item_main;

                // FOOTER -----------------------------------------
                const item_footer = document.createElement('footer');
                
                const item_input = document.createElement('input');
                item_input.type = 'text';
                item_input.placeholder = 'Введите команду и нажмите Enter';
                this.element_InputBox = item_input;

                item_footer.appendChild(item_input);

                div_itembox.appendChild(item_header);
                div_itembox.appendChild(item_main);
                div_itembox.appendChild(item_footer);
                
                this.element_ItemBox = div_itembox;
                
                items_container__id.appendChild(this.element_ItemBox); // добавляем в DOM! нельзя вынести вверх!!!!


                //item_input.addEventListener('keydown', (e) => {
                //    if (e.key === 'Enter' && this.socket?.readyState === WebSocket.OPEN) {
                //        const cmd = e.target.value.trim();
                //        if (cmd) {
                //           this.socket.send(cmd);
                //           e.target.value = '';
                //       }
                //    }
                //});
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
                    //this.element_Status.textContent = '⚠️';
                };
            }

            sendReconnect() {
                //if (this.socket?.readyState === WebSocket.OPEN) {
                //    this.socket.send('cmd_reconnect');
                //}
                
                if (globalSocket?.readyState === WebSocket.OPEN) {
                    globalSocket.send(JSON.stringify({
                        cmd: "reconnect",
                        item_id: this.itemId
                    }));
                }
            }
            
            sendDelHistory() {
                //this.element_OutputBox.innerHTML = '';
                //
                //if (this.socket?.readyState === WebSocket.OPEN) {
                //    this.socket.send('cmd_sendDelHistory');
                //}
                
                this.element_OutputBox.innerHTML = '';
                if (globalSocket?.readyState === WebSocket.OPEN) {
                    globalSocket.send(JSON.stringify({
                        cmd: "clear_history",
                        item_id: this.itemId
                    }));
                }
            }

            async loadHistory() {
                // Очищаем окно перед загрузкой, чтобы избежать дублей
                this.element_OutputBox.innerHTML = '';
                try {
                    const resp = await fetch(`/item/history/get/${this.itemId}`);
                    const history = await resp.json();
                    history.forEach(cmd => {
                        if (cmd.input) this.addHistoryLine('msg_stdin__cls', `→ ${cmd.input}`);
                        cmd.stdout?.forEach(l => this.addHistoryLine('msg_stdout__cls', l));
                        cmd.stderr?.forEach(l => this.addHistoryLine('msg_stderr__cls', l));
                        cmd.debug?.forEach(l => this.addHistoryLine('msg_debug__cls', l));
                    });
                    this.addHistoryLine('msg_debug__cls', '=== HISTORY ===');
                } catch (err) {
                    this.addHistoryLine('msg_stderr__cls', `Ошибка loadHistory ${err.message}`);
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
        //window.onload = () => itemsManager.init();
        //window.onbeforeunload = () => {
        //    itemsManager.items_map.forEach(s => s.socket?.close());
        //};
        
        window.onload = () => {
            connectGlobalWebSocket();
            // Дождёмся открытия сокета? Можно сначала получить список через REST, а сокет использовать для событий
            // Но инициализацию itemsManager лучше запустить после получения списка
            itemsManager.init(); // теперь внутри init будет только REST-запрос /item/list и создание UI
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


@app.get("/item/list")
async def list_items():
    ids = list(object_manager.items)
    return {"items": ids}


# ---------------------------------------------------------------------------------------------------------------------
@app.post("/item/create")
async def create_item(idn: str = None):
    # print(f"{idn=}")
    # if idn is not None:
    #     idn = await object_manager.create_item(idn=idn)
    # else:
    #     idn = await object_manager.create_item()

    idn = await object_manager.create_item()

    return {"idn": idn}


@app.delete("/item/del/{idn}")
async def del_item(idn: str):
    await object_manager.del_item(idn)
    return {"status": "closed"}


@app.get("/item/{idn}")
async def get_item(idn: str):
    if idn in object_manager.items:
        return {"idn": idn, }
    raise HTTPException(status_code=404, detail=f"[{idn=}]Item not found")


# ---------------------------------------------------------------------------------------------------------------------
@app.delete("/item/history/del/{idn}")
async def del_history(idn: str):
    object_manager.clear_history(idn)
    return {"status": "closed"}


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
    try:
        # Держим соединение открытым, игнорируем входящие сообщения
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass


# ---------------------------------------------------------------------------------------------------------------------
@app.websocket("/ws/client")
async def ws_client(websocket: WebSocket):
    client_id = str(uuid.uuid4())
    await websocket.accept()
    queue = asyncio.Queue()
    await client_manager.register_client(client_id, queue)

    # Задача отправки сообщений из очереди в WebSocket
    async def sender():
        try:
            while True:
                msg = await queue.get()
                await websocket.send_json(msg)
        except asyncio.CancelledError:
            pass

    send_task = asyncio.create_task(sender())

    try:
        while True:
            data = await websocket.receive_json()
            cmd = data.get("cmd")
            if cmd == "send_command":
                item_id = data["item_id"]
                command = data["data"]
                item = object_manager.get_item(item_id)
                if item:
                    asyncio.create_task(item.send_cmd(command))
            elif cmd == "clear_history":
                item_id = data["item_id"]
                object_manager.clear_history(item_id)
                # Можно отправить подтверждение
                await websocket.send_json({
                    "item_id": item_id,
                    "type": "system",
                    "data": {"subtype": "info", "text": "History cleared"}
                })
            elif cmd == "reconnect":
                item_id = data["item_id"]
                item = object_manager.get_item(item_id)
                if item:
                    asyncio.create_task(item.reconnect())
            elif cmd == "create_item":
                # Создание терминала через WebSocket (альтернатива REST)
                await object_manager.create_item()
            elif cmd == "delete_item":
                item_id = data["item_id"]
                await object_manager.del_item(item_id)
    except WebSocketDisconnect:
        pass
    finally:
        send_task.cancel()
        await send_task
        await client_manager.unregister_client(client_id)


# ---------------------------------------------------------------------------------------------------------------------
@app.websocket("/ws/{idn}")
async def ws__endpoint(websocket: WebSocket, idn: str):
    item = object_manager.get_item(idn)
    if not item:
        await websocket.close(code=1008, reason=f"{idn=}/Invalid")
        return

    # Создаём очередь для этого клиента
    client_queue = asyncio.Queue()

    # Создаём слушателя, который будет класть сообщения в очередь
    def listener(msg_style, msg_text):
        asyncio.create_task(client_queue.put((msg_style, msg_text)))

    item.history.listener__add(listener)

    # Подключаем процесс, если ещё не подключён (теперь слушатель уже есть)
    if not item._conn:
        await item.connect()

    # Задача отправки из очереди в WebSocket
    async def send_output():
        try:
            while True:
                msg_style, msg_text = await client_queue.get()
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
