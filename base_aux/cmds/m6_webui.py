import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from base_aux.cmds.m5_terminal1_os2_aio import *
from base_aux.cmds.m5_terminal2_serial2_aio import *
from base_aux.qeues.m1_event_broadcaster import EventBroadcaster, Nest_EventBroadcasterImplemented
from base_aux.tasks.m1_tasks_bg import Nest_TasksBg_AbcAio

import serial.tools.list_ports  # need import exactly this full path! and use same full path!


# =====================================================================================================================
event_broadcaster = EventBroadcaster()


# =====================================================================================================================
class Base_ManagerInstance(Nest_TasksBg_AbcAio):
    ITEM_CLASS: type[BaseAio_CmdTerminal]
    items: dict[str, BaseAio_CmdTerminal]

    def __init__(self, *args, **kwargs):
        self.items = {}
        super().__init__(*args, **kwargs)

    # -----------------------------------------------------------------------------------------------------------------
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self._tasks_bg__stop_delete()
        except:
            pass
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
        new_item = self.ITEM_CLASS(*args, eb=event_broadcaster, **kwargs)
        item_id = new_item.idn

        # 2=WORK -----------------------
        print(f"create_item:{item_id=}")
        self.items[item_id] = new_item

        await new_item.connect()

        # 3=broadcust -----------------------
        await event_broadcaster.broadcast({
            "item_id": item_id,
            "channel": "item_control",
            "action": "create_item",
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
                "action": "delete_item",
            })


# ----------------------------------------------------------------------------------------------------------------------
class Base_ManagerInst_Term(Base_ManagerInstance):
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
            "channel": "item_control",
            "action": "clear_history",
        })


# ----------------------------------------------------------------------------------------------------------------------
class ManagerInst_TermOs(Base_ManagerInst_Term):
    ITEM_CLASS = CmdTerminal_OsAio
    async def __aenter__(self):
        await self.create_first_item()
        return self

    async def create_first_item(self) -> None:
        item_idn = await self.create_item()
        item_inst = self.get_item(item_idn)
        await item_inst.connect()


# ----------------------------------------------------------------------------------------------------------------------
class ManagerInst_TermSerial(Base_ManagerInst_Term):
    ITEM_CLASS = CmdTerminal_SerialAio

    def _tasks_bg__create_start(self) -> None:
        self._tasks_bg__extend(self.monitor_instances())

    async def monitor_instances(
            self,
            poll_interval: float = 1.0,
            stop_event: asyncio.Event | None = None,
    ):
        """
        Непрерывно отслеживает подключение/отключение COM-портов.
        :param poll_interval: интервал опроса (сек)
        :param stop_event: событие для остановки мониторинга; если не передано, создаётся новое
        """
        if stop_event is None:
            stop_event = asyncio.Event()

        while not stop_event.is_set():
            known_ports = set(self.items)

            # 1=DETECT ------------------
            try:
                detected_port__objs = serial.tools.list_ports.comports()
                detected_port__addrs = {p.device for p in detected_port__objs}
                print(f"{detected_port__addrs=}")
            except Exception:
                # В случае ошибки (например, нет прав) пропускаем цикл
                await asyncio.sleep(poll_interval)
                continue

            # 2=WORK ------------------
            added = detected_port__addrs - known_ports
            removed = known_ports - detected_port__addrs

            for port in added:
                try:
                    await self.create_item(port=port, baudrate=115200)
                except Exception as e:
                    print(f"Error creating item for {port}: {e}")

            for port in removed:
                try:
                    await self.del_item(port)
                except Exception as e:
                    print(f"Error deleting item for {port}: {e}")

            await asyncio.sleep(poll_interval)


# ----------------------------------------------------------------------------------------------------------------------
# manager_inst__termos = ManagerInst_TermOs()
manager_inst__termos = ManagerInst_TermSerial()


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

templates = Jinja2Templates(directory=os.path.dirname(__file__))

# Уникальный идентификатор сервера: можно использовать время запуска
server_id = str(int(asyncio.get_event_loop().time()))


# ---------------------------------------------------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def html__root(request: Request):
    return templates.TemplateResponse(
        "m6_webui.html",                            # имя файла в папке шаблонов
        {"request": request, "server_id": server_id}  # контекст (request обязателен)
    )


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
    async def queue_to_ws__translator(ws: WebSocket):
        """
        GOAL: resend all msgs from clientQueue to clientWS
        """
        try:
            while True:
                msg = await client_queue.get()
                await ws.send_json(msg)
        except asyncio.CancelledError:
            pass

    queue_to_ws__task = asyncio.create_task(queue_to_ws__translator(websocket))

    # --------------------------------------------
    # WS-2=READER
    try:
        while True:
            msg = await websocket.receive_json()

            msg__channel = msg.get("channel")
            msg__itemid = msg.get("item_id")

            msg__action = msg.get("action")
            msg__text = msg.get("text")

            # ----------------------------------------------
            if msg__channel == "history_log":   # keep here

                item = manager_inst__termos.get_item(msg__itemid)
                if item and msg__text:
                    asyncio.create_task(item.send_cmd(msg__text))

            elif msg__channel == "item_control":
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
        await asyncio.wait_for(queue_to_ws__task, 2)
        event_broadcaster.unregister_client(client_id)


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=80)


# =====================================================================================================================
