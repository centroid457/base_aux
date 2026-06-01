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

    async def register_client(self, client_id: str) -> asyncio.Queue:
        client_queue = asyncio.Queue()
        self._queues[client_id] = client_queue
        return client_queue

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
        new_item = self.ITEM_CLASS(*args, **kwargs)
        item_id = new_item.idn
        print(f"create_item:{item_id=}")
        self.items[item_id] = new_item

        # Запускаем процесс терминала
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
        // Глобальный WebSocket
        let globalSocket = null;
    
        function connectGlobalWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            globalSocket = new WebSocket(`${protocol}//${window.location.host}/ws/client`);
    
            globalSocket.onopen = async () => {
                console.log("Global WebSocket connected");
                await syncWithServer();   // синхронизация после восстановления
            };
    
            globalSocket.onmessage = (e) => {
                const msg = JSON.parse(e.data);
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
                        const stored = itemsManager.get_IdsClient();
                        if (!stored.includes(newId)) {
                            stored.push(newId);
                            itemsManager.set_IdsClient(stored);
                        }
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
                        const stored = itemsManager.get_IdsClient();
                        const updated = stored.filter(id => id !== delId);
                        itemsManager.set_IdsClient(updated);
                    } else if (msg.data.subtype === "history_clear") {
                        const itemId = msg.data.item_id;
                        const ui = itemsManager.items_map.get(itemId);
                        if (ui) {
                            ui.element_OutputBox.innerHTML = '';
                        }
                    }
                } else if (msg.type === "system") {
                    console.log(msg.data.text);
                }
            };
    
            globalSocket.onclose = () => {
                console.log("Global WebSocket closed, reconnecting in 3s...");
                setTimeout(connectGlobalWebSocket, 3000);
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
                    itemsManager.addItem(id);
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
                    this.addItem(idn);
                }
                // 🔽 Добавить обработчик кнопки
                document.getElementById('btn_add_item__id').addEventListener('click', () => this.createNewItem());
            },
        
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
    
            async createNewItem() {
                await fetch('/item/create', { method: 'POST' });
                // Не создаём UI – ждём события от сервера
            },
    
            addItem(itemId) {
                if (this.items_map.has(itemId)) return;
                const itemUI = new ItemUI(itemId);
                this.items_map.set(itemId, itemUI);
                itemUI.init();
            },
    
            async delItem(itemId) {
                await fetch(`/item/del/${itemId}`, { method: 'DELETE' });
                // Сервер разошлёт событие delete, UI удалится в обработчике
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
                this.element_Status = null;
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
                const leftDiv = document.createElement('div');
                const rightDiv = document.createElement('div');
                header.appendChild(leftDiv);
                header.appendChild(rightDiv);
    
                const spanStatus = document.createElement('span');
                this.element_Status = spanStatus;
                const spanId = document.createElement('span');
                spanId.className = 'span_item_id__cls';
                spanId.textContent = this.itemId;
                leftDiv.appendChild(spanStatus);
                leftDiv.appendChild(spanId);
    
                const btnClear = document.createElement('button');
                btnClear.className = 'button_blue_outline__cls';
                btnClear.textContent = 'clear';
                btnClear.title = 'Clear History';
                btnClear.onclick = () => this.sendDelHistory();
                const btnReconnect = document.createElement('button');
                btnReconnect.className = 'button_blue_outline__cls';
                btnReconnect.textContent = '🔄';
                btnReconnect.title = 'Reconnect';
                btnReconnect.onclick = () => this.sendReconnect();
                const btnClose = document.createElement('button');
                btnClose.className = 'button_red_outline__cls';
                btnClose.textContent = 'X';
                btnClose.title = 'Close';
                btnClose.onclick = () => itemsManager.delItem(this.itemId);
                rightDiv.appendChild(btnClear);
                rightDiv.appendChild(btnReconnect);
                rightDiv.appendChild(btnClose);
    
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
    
                input.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' && globalSocket?.readyState === WebSocket.OPEN) {
                        const cmd = e.target.value.trim();
                        if (cmd) {
                            globalSocket.send(JSON.stringify({
                                cmd: "send_command",
                                item_id: this.itemId,
                                data: cmd
                            }));
                            e.target.value = '';
                        }
                    }
                });
            }
    
            sendReconnect() {
                if (globalSocket?.readyState === WebSocket.OPEN) {
                    globalSocket.send(JSON.stringify({
                        cmd: "reconnect",
                        item_id: this.itemId
                    }));
                }
            }
    
            sendDelHistory() {
                this.element_OutputBox.innerHTML = '';
                if (globalSocket?.readyState === WebSocket.OPEN) {
                    globalSocket.send(JSON.stringify({
                        cmd: "clear_history",
                        item_id: this.itemId
                    }));
                }
            }
    
            async loadHistory() {
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
                    this.addHistoryLine('msg_stderr__cls', `Ошибка loadHistory: ${err.message}`);
                }
            }
    
            addHistoryLine(style, text) {
                const line = document.createElement('div');
                line.className = style;
                line.textContent = text;
                this.element_OutputBox.appendChild(line);
                this.element_OutputBox.scrollTop = this.element_OutputBox.scrollHeight;
            }
    
            destroy() {
                this.element_ItemBox?.remove();
            }
        }
    
        // --------------------------------------------------------------
        // Запуск
        // --------------------------------------------------------------
        window.onload = async () => {
            await itemsManager.initUI();   // первичная загрузка через REST
            connectGlobalWebSocket();      // открываем сокет
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
    # Оповещаем всех клиентов об очистке истории
    await client_manager.broadcast({
        "type": "control",
        "data": {
            "subtype": "history_clear",
            "item_id": idn
        }
    })
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
async def ws__client(websocket: WebSocket):
    # client_id = str(uuid.uuid4())
    # await websocket.accept()
    #
    # client_queue = asyncio.Queue()
    # await client_manager.register_client(client_id, client_queue)
    #
    # # перенаправляем все события/сообщения из очереди в WebSocket
    # try:
    #     while True:
    #         msg = await client_queue.get()
    #         await websocket.send_json(msg)
    # except asyncio.CancelledError:
    #     pass
    # except WebSocketDisconnect:
    #     pass
    # finally:
    #     await client_manager.unregister_client(client_id)

    client_id = str(uuid.uuid4())
    await websocket.accept()

    client_queue = await client_manager.register_client(client_id)

    # задача перенаправления событий из очереди в WebSocket
    async def sender():
        try:
            while True:
                msg = await client_queue.get()
                await websocket.send_json(msg)
        except asyncio.CancelledError:
            pass

    send_task = asyncio.create_task(sender())

    # --------------------------------------------
    try:
        while True:
            data = await websocket.receive_json()
            cmd = data.get("cmd")

            if cmd == "send_command":   # keep here
                item_id = data["item_id"]
                command = data["data"]
                item = object_manager.get_item(item_id)
                if item:
                    asyncio.create_task(item.send_cmd(command))

            elif cmd == "clear_history":    # FIXME: move to POST??
                item_id = data["item_id"]
                object_manager.clear_history(item_id)
                # Рассылаем всем клиентам
                await client_manager.broadcast({
                    "type": "control",
                    "item_id": item_id,
                    "data": {
                        "subtype": "history_clear",
                        "item_id": item_id
                    }
                })

            elif cmd == "reconnect":    # FIXME: move to POST??
                item_id = data["item_id"]
                item = object_manager.get_item(item_id)
                if item:
                    asyncio.create_task(item.reconnect())

            elif cmd == "create_item":    # FIXME: move to POST??
                # Создание терминала через WebSocket (альтернатива REST)
                await object_manager.create_item()

            elif cmd == "delete_item":    # FIXME: move to POST??
                item_id = data["item_id"]
                await object_manager.del_item(item_id)

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
