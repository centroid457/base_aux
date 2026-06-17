import asyncio
from typing import *
from abc import abstractmethod

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from base_aux.cmds.m5_terminal1_os2_aio import *
from base_aux.cmds.m5_terminal2_serial2_aio import *
from base_aux.qeues.m1_event_broadcaster import EventBroadcaster, Nest_EventBroadcasterImplemented
from base_aux.cmds.m0_tasks_bg import Nest_TasksBg_AbcAio

import serial.tools.list_ports


# =====================================================================================================================
event_broadcaster = EventBroadcaster()


# =====================================================================================================================
class ManagerInstance(Nest_TasksBg_AbcAio):
    ITEM_CLASS: type[BaseAio_CmdTerminal]
    items: dict[str, BaseAio_CmdTerminal]

    def __init__(self, *args, **kwargs):
        self.items = {}
        super().__init__(*args, **kwargs)

    # -----------------------------------------------------------------------------------------------------------------
    async def __aenter__(self):
        try:
            self._tasks_bg__create_start()
        except:
            pass
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._tasks_bg__stop_delete()
        for item in self.items:
            await self.del_item(item)

    # -----------------------------------------------------------------------------------------------------------------
    @abstractmethod
    async def monitor_instances(self) -> Never | NoReturn:
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def get_item(self, idn: str) -> BaseAio_CmdTerminal | None:
        return self.items.get(idn)

    # CMDS -------------------------------------------------------------------------------------------------------------
    async def create_item(self, *args, **kwargs) -> str:
        # 1=detect --------------------------
        new_item = self.ITEM_CLASS(*args, **kwargs)
        item_id = new_item.idn

        if isinstance(new_item, Nest_EventBroadcasterImplemented):
            new_item.eb__setup(event_broadcaster, aux_data=dict(item_id=item_id))

        # 2=WORK -----------------------
        print(f"create_item:{item_id=}")
        self.items[item_id] = new_item

        await new_item.connect()

        # 3=broadcust -----------------------
        await event_broadcaster.broadcast({
            "item_id": item_id,
            "channel": "item_control",
            "load": {
                "action": "create_item",
            }
        })
        return item_id

    async def del_item(self, idn: str) -> None:
        # 1=detect --------------------------
        item = self.items.pop(idn, None)
        if item:
            # 2=WORK ----------------------------
            await item.disconnect()

            # 3=broadcust -----------------------
            await event_broadcaster.broadcast({
                "item_id": idn,
                "channel": "item_control",
                "load": {
                    "action": "delete_item",
                }
            })


# ----------------------------------------------------------------------------------------------------------------------
class ManagerInst_Term(ManagerInstance):
    ITEM_CLASS = CmdTerminal_OsAio

    # SPECIAL methods --------------------------------------------
    async def clear_history(self, idn: str) -> None:
        # 1=detect --------------------------
        item = self.items.get(idn)
        if not item:
            return

        # 2=WORK ----------------------------
        item.history.clear()

        # 3=broadcust -----------------------
        await event_broadcaster.broadcast({
            "item_id": idn,                 # FILTER
            "channel": "item_control",        # EVENT
            "load": {                           # LOAD
                "action": "clear_history",     # ACTION
            }
        })


# ----------------------------------------------------------------------------------------------------------------------
class ManagerInst_TermOs(ManagerInst_Term):
    ITEM_CLASS = CmdTerminal_SerialAio
    async def __aenter__(self):
        await self.create_first_item()
        return self

    async def create_first_item(self) -> None:
        item_idn = await self.create_item()
        item_inst = self.get_item(item_idn)
        await item_inst.connect()


# ----------------------------------------------------------------------------------------------------------------------
class ManagerInst_TermSerial(ManagerInst_Term):
    ITEM_CLASS = CmdTerminal_SerialAio

    def _tasks_bg__create_start(self) -> None:
        self._tasks_bg = [
                asyncio.create_task(self.monitor_instances()),
            ]

    async def monitor_instances(
            self,
            poll_interval: float = 1.0,
            stop_event: asyncio.Event | None = None,
    ):
        """
        Непрерывно отслеживает подключение/отключение COM-портов.

        :param create_item: async функция, вызываемая при появлении нового порта (принимает имя порта, например 'COM3')
        :param del_item: async функция, вызываемая при исчезновении порта
        :param poll_interval: интервал опроса (сек)
        :param stop_event: событие для остановки мониторинга; если не передано, создаётся новое
        """
        if stop_event is None:
            stop_event = asyncio.Event()

        known_ports = set()
        while not stop_event.is_set():
            # 1=DEFINE ------------------
            objs = serial.tools.list_ports.comports()
            if not objs:
                await asyncio.sleep(poll_interval)
                continue

            try:
                current_ports = {p.device for p in objs}
                print(current_ports)
            except Exception:
                # В случае ошибки (например, нет прав) пропускаем цикл
                await asyncio.sleep(poll_interval)
                continue

            # 2=WORK ------------------
            added = current_ports - known_ports
            removed = known_ports - current_ports

            for port in added:
                try:
                    await self.create_item(port=port)
                except Exception as e:
                    print(f"Error creating item for {port}: {e}")

            for port in removed:
                try:
                    await self.del_item(port)
                except Exception as e:
                    print(f"Error deleting item for {port}: {e}")

            known_ports = current_ports
            await asyncio.sleep(poll_interval)


# ----------------------------------------------------------------------------------------------------------------------
manager_inst__termos = ManagerInst_TermOs()
# manager_inst__termos = ManagerInst_TermSerial()


# TODO:
#  separate js into file
#  create full html in js


# =====================================================================================================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <script>uncache_loading__all_files_without_cache();</script>
    
    <meta charset="utf-8">
    <title>WebClient</title>
    
    <link rel="stylesheet" href="/base_aux/webs_front/d1_front2_css/universal_root.css">
    <script src="/base_aux/webs_front/d2_js1_vanilla/universal_root.js"></script>
    
    <style>
        /* ---------------------------------------------------------------------------------------------------------- */
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
        <h1 style="color: #fff">WebClient</h1>
        <div>
            <button id="btn_resync__id">resync</button>
            <button id="btn_add_item__id">Новый объект</button>
            <span data-auto__replace_with__btn_hard_reset></span>
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
                const msg__event = msg.channel;
                const msg__data = msg.load;
                
                const msg__action = msg__data?.action;
                const msg__text = msg__data?.text;
                
                if (msg__event === "history_log") {
                    const ui = itemsManager.items_map.get(msg__itemid);
                    if (ui) {
                        let style = '';
                        if (msg__action === 'stdout') style = 'msg_stdout__cls';
                        else if (msg__action === 'stderr') style = 'msg_stderr__cls';
                        else if (msg__action === 'stdin') style = 'msg_stdin__cls';
                        else style = 'msg_debug__cls';
                        
                        ui.addHistoryLine(style, msg__text);
                    }
                    
                } else if (msg__event === "item_control") {
                
                    if (msg__action === "create_item") {
                        const stored = itemsManager.get_IdsClient();
                        if (!stored.includes(msg__itemid)) {
                            stored.push(msg__itemid);
                            itemsManager.set_IdsClient(stored);
                        }
                        if (!itemsManager.items_map.has(msg__itemid)) {
                            itemsManager.addItemElement(msg__itemid);
                        }
                        
                    } else if (msg__action === "delete_item") {
                        const ui = itemsManager.items_map.get(msg__itemid);
                        if (ui) {
                            ui.destroy();
                            itemsManager.items_map.delete(msg__itemid);
                        }
                        const stored = itemsManager.get_IdsClient();
                        const updated = stored.filter(id => id !== msg__itemid);
                        itemsManager.set_IdsClient(updated);
                        
                    } else if (msg__action === "clear_history") {
                        const ui = itemsManager.items_map.get(msg__itemid);
                        if (ui) {
                            ui.element_OutputBox.innerHTML = '';
                        }
                    }
                    
                } else if (msg__event === "system") {
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
                    channel: "item_control",
                    load: {
                        action: "create_item",
                    },
                }));
            },
    
            async delItem(itemId) {
                if (ws_client?.readyState !== WebSocket.OPEN) return;

                ws_client.send(JSON.stringify({
                    item_id: itemId,
                    channel: "item_control",
                    load: {
                        action: "delete_item",
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
                btnClear.setAttribute('data-btn_outline', "blue");
                btnClear.textContent = 'clear';
                btnClear.title = 'Clear History';
                btnClear.onclick = () => this.sendDelHistory();
                
                const btnReconnect = document.createElement('button');
                btnReconnect.setAttribute('data-btn_outline', "blue");
                btnReconnect.textContent = 'Reconnect';
                btnReconnect.title = 'Reconnect';
                btnReconnect.onclick = () => this.sendReconnect();
                
                const btnClose = document.createElement('button');
                btnClose.setAttribute('data-btn_outline', "red");
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
                        channel: "history_log",
                        load: {
                            action: "stdin",  // FIXME: or just stdin/msg_stdin__cls
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
                    channel: "item_control",
                    load: {
                        action: "reconnect_item",
                    },
                }));
            }
    
            sendDelHistory() {
                if (ws_client?.readyState !== WebSocket.OPEN) return;

                ws_client.send(JSON.stringify({
                    item_id: this.itemId,
                    channel: "item_control",
                    load: {
                        action: "clear_history",
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
    await event_broadcaster.start_task()

    async with manager_inst__termos:

        yield  # <-- здесь сервер работает и обрабатывает запросы

        # --- Код, выполняемый ПРИ ОСТАНОВКЕ сервера (бывший shutdown_event) ---
        # for item_id, item in manager_inst__termos.items.items():
        #     print(f"FastApi.Shutdown: {item_id=}")
        #     await item.disconnect()

        print(f"FastApi.Shutdown: FINISHED")
        # ---------------------------------------------------------------------


# =====================================================================================================================
app = FastAPI(title="WebClient", lifespan=lifespan)
app.mount("/base_aux", StaticFiles(directory="../"), name="base_aux")

# Уникальный идентификатор сервера: можно использовать время запуска
server_id = str(int(asyncio.get_event_loop().time()))


# ---------------------------------------------------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def html__root():
    return HTML_TEMPLATE


@app.get("/item/list")
async def list_items():
    ids = list(manager_inst__termos.items)
    return {"items": ids}

# ---------------------------------------------------------------------------------------------------------------------
@app.get("/item/history/get/{idn}")
async def get_history(idn: str):
    item = manager_inst__termos.get_item(idn)
    if not item:
        raise HTTPException(status_code=404, detail=f"[{idn=}]Item not found")

    history_data: list[dict] = []
    for result in item.history:
        history_data.append({
            "input": result.INPUT,
            "stdout": result.STDOUT,
            "stderr": result.STDERR,
            # "debug": result.DEBUG,
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
    await websocket.send_json({"channel": "server_id", "id": server_id})

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
    client_id, client_queue = event_broadcaster.register_client()

    # --------------------------------------------
    # WS-1=WRITER = задача перенаправления событий из очереди в WebSocket
    async def queue_to_ws__translator():
        """
        GOAL: resend all msgs from clientQueue to clientWS
        """
        try:
            while True:
                msg = await client_queue.get()
                await websocket.send_json(msg)
        except asyncio.CancelledError:
            pass

    queue_to_ws__task = asyncio.create_task(queue_to_ws__translator())

    # --------------------------------------------
    # WS-2=READER
    try:
        while True:
            msg = await websocket.receive_json()

            msg__event = msg.get("channel")
            msg__itemid = msg.get("item_id")
            msg__data = msg.get("load")

            if msg__data:
                msg__action = msg__data.get("action")
                msg__text = msg__data.get("text")
            else:
                msg__action = None
                msg__text = None

            # ----------------------------------------------
            if msg__event == "history_log":   # keep here

                item = manager_inst__termos.get_item(msg__itemid)
                if item and msg__text:
                    asyncio.create_task(item.send_cmd(msg__text))

            elif msg__event == "item_control" and msg__data:
                if msg__action == "clear_history":
                    asyncio.create_task(manager_inst__termos.clear_history(msg__itemid))

                elif msg__action == "reconnect_item":
                    item = manager_inst__termos.get_item(msg__itemid)
                    asyncio.create_task(item.reconnect())

                elif msg__action == "create_item":
                    asyncio.create_task(manager_inst__termos.create_item())

                elif msg__action == "delete_item":
                    asyncio.create_task(manager_inst__termos.del_item(msg__itemid))

        # --------------------------------------------
    except WebSocketDisconnect:
        pass
    finally:
        queue_to_ws__task.cancel()
        await queue_to_ws__task
        event_broadcaster.unregister_client(client_id)


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=80)


# =====================================================================================================================
