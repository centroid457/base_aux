from typing import *
import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import uvicorn

from pydantic import BaseModel
from functools import cached_property

import serial.tools.list_ports  # need import exactly this full path! and use same full path!

from base_aux.cmds.m5_terminal1_os2_aio import *
from base_aux.cmds.m5_terminal2_serial2_aio import *
from base_aux.qeues.m1_event_broadcaster import *
from base_aux.tasks.m1_tasks_bg import *
from base_aux.aux_paradigm.m2_aio import *
from base_aux.webs_back.d4_channels.m1_ws_server import WsServer
from base_aux.aux_eq.m4_eq_valid3_derivatives import EqValid_AttrsByKwargs


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
            "action": "history_clear",
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
        self._event_stop.clear()    # DONT FORGET!!!
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
manager_inst = ManagerInst_TermOs()
# manager_inst = ManagerInst_TermSerial()


# =====================================================================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Код, выполняемый ПРИ СТАРТЕ сервера (бывший startup_event) ---
    print(f"FastApi.Startup: START")
    await event_broadcaster.start_task()

    async with manager_inst:

        yield  # <-- здесь сервер работает и обрабатывает запросы

        # --- Код, выполняемый ПРИ ОСТАНОВКЕ сервера (бывший shutdown_event) ---
        # for item_id, item in manager_inst.items.items():
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


# =====================================================================================================================
class Model_RpcRequest(BaseModel):
    # transport: str    # WARN: DONT: use it here!
    channel: str
    action: str
    item_id: Optional[str] = None
    load: Optional[str | dict] = None


class Model_RpcResponse(BaseModel):
    ok: bool = True
    load: Any | dict = None


# ---------------------------------------------------------------------------------------------------------------------
TYPING__CMD_HANDLER = Callable[[Model_RpcRequest], Awaitable[Model_RpcResponse]]


class Base_RpcServer:
    RESPONSE_CLS: BaseModel = Model_RpcResponse

    # TODO: raise HTTPException or return Model_RpcResponse(False) ????? - NO! keep direct!
    # raise HTTPException(status_code=400, detail=result_msg)
    # raise HTTPException(status_code=404, detail=f"[{cmd.item_id=}]Item not found")

    def __init__(
            self,
            **kwargs,
    ):
        super().__init__(**kwargs)

    def _response_make(self, **kwargs) -> Model_RpcResponse:
        return self.RESPONSE_CLS(**kwargs)

    async def execute(self, cmd: Model_RpcRequest) -> Model_RpcResponse:
        for matcher, handler in self.SCHEMA.items():
            if matcher == cmd:          # срабатывает EqValid_AttrsByKwargs.__eq__
                try:
                    return await handler(cmd)
                except Exception as exc:
                    return Model_RpcResponse(ok=False, load=str(exc))
        # Неизвестная команда
        return Model_RpcResponse(
            ok=False,
            load=f"Unsupported request channel/action: {cmd}"
        )

    @property
    def SCHEMA(self) -> dict[EqValid_AttrsByKwargs, TYPING__CMD_HANDLER]:
        raise NotImplementedError()


# ---------------------------------------------------------------------------------------------------------------------
class RpcServer_Terminal(Base_RpcServer):
    RESPONSE_CLS = Model_RpcResponse

    def __init__(
            self,
            manager_inst,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.manager_inst = manager_inst

    @cached_property
    def SCHEMA(self) -> dict[EqValid_AttrsByKwargs, TYPING__CMD_HANDLER]:
        schema = {
            EqValid_AttrsByKwargs(channel="item_control", action="reconnect_item"): self._item__reconnect,
            EqValid_AttrsByKwargs(channel="item_control", action="disconnect_item"): self._item__disconnect,
            EqValid_AttrsByKwargs(channel="item_control", action="create_item"): self._item__create,
            EqValid_AttrsByKwargs(channel="item_control", action="delete_item"): self._item__delete,
            EqValid_AttrsByKwargs(channel="item_control", action="history_clear"): self._item__history_clear,
            EqValid_AttrsByKwargs(channel="item_control", action="send_stdin"): self._item__send_stdin,
            EqValid_AttrsByKwargs(channel="item_control", action="items_get"): self._items__list_get,
            EqValid_AttrsByKwargs(channel="item_control", action="history_get"): self._item__history_get,
            EqValid_AttrsByKwargs(channel="item_control", action="config_change"): self._item__config_change,
            EqValid_AttrsByKwargs(channel="item_control", action="config_get"): self._item__config_get,
        }
        return schema

    # -----------------------------------------------------------------------------------------------------------------
    # 1=NO NEED ANSWER --------------------------
    async def _item__reconnect(self, cmd: Model_RpcRequest) -> Model_RpcResponse | NoReturn:
        item = self.manager_inst.get_item(cmd.item_id)
        TasksBg_PoolGlobal().spawn(item.reconnect())
        return self._response_make()

    async def _item__disconnect(self, cmd: Model_RpcRequest) -> Model_RpcResponse | NoReturn:
        item = self.manager_inst.get_item(cmd.item_id)
        TasksBg_PoolGlobal().spawn(item.disconnect())
        return self._response_make()

    async def _item__create(self, cmd: Model_RpcRequest) -> Model_RpcResponse | NoReturn:
        TasksBg_PoolGlobal().spawn(self.manager_inst.create_item())
        return self._response_make()

    async def _item__delete(self, cmd: Model_RpcRequest) -> Model_RpcResponse | NoReturn:
        TasksBg_PoolGlobal().spawn(self.manager_inst.del_item(cmd.item_id))
        return self._response_make()

    async def _item__history_clear(self, cmd: Model_RpcRequest) -> Model_RpcResponse | NoReturn:
        TasksBg_PoolGlobal().spawn(self.manager_inst.clear_history(cmd.item_id))
        return self._response_make()

    # 2=NEED ANSWER-1=at least status ---------------------
    async def _item__send_stdin(self, cmd: Model_RpcRequest) -> Model_RpcResponse | NoReturn:
        item = self.manager_inst.get_item(cmd.item_id)
        if not item:
            return self._response_make(ok=False, load=f"[{cmd.item_id=}]Item not found")
        if cmd.load:
            await item.send_cmd(cmd.load)          # результат не возвращаем, как в исходном коде
        return self._response_make()

    async def _item__config_change(self, cmd: Model_RpcRequest) -> Model_RpcResponse | NoReturn:
        item = self.manager_inst.get_item(cmd.item_id)
        if not item:
            return self._response_make(ok=False, load=f"[{cmd.item_id=}]Item not found")
        if not cmd.load:
            return self._response_make(ok=False, load=f"BLANC[{cmd.load=}]")

        item.config_change(**cmd.load)
        await item.reconnect()
        return self._response_make()

    # 3=NEED ANSWER-2=data ---------------------------------
    async def _item__config_get(self, cmd: Model_RpcRequest) -> Model_RpcResponse | NoReturn:
        item = self.manager_inst.get_item(cmd.item_id)
        if not item:
            return self._response_make(ok=False, load=f"[{cmd.item_id=}]Item not found")

        result = item.config_get()
        return self._response_make(load=result)

    async def _items__list_get(self, cmd: Model_RpcRequest) -> Model_RpcResponse | NoReturn:
        ids = list(self.manager_inst.items)
        return self._response_make(load=ids)

    async def _item__history_get(self, cmd: Model_RpcRequest) -> Model_RpcResponse | NoReturn:
        item = self.manager_inst.get_item(cmd.item_id)
        if not item:
            return self._response_make(ok=False, load=f"[{cmd.item_id=}]Item not found")
        history_data = [
            {
                "input": r.INPUT,
                "stdout": r.STDOUT,
                "stderr": r.STDERR,
                "timestamp": r.timestamp.isoformat() if r.timestamp else None,
                "duration": r.duration,
                "finished_status": r.finished_status.value if r.finished_status else None,
                "retcode": r.retcode,
            }
            for r in item.history
        ]
        return self._response_make(load=history_data)


# ---------------------------------------------------------------------------------------------------------------------
rpc_server = RpcServer_Terminal(manager_inst=manager_inst)


@app.post("/channel__rpc", response_model=Model_RpcResponse)
async def channel__rpc(cmd: Model_RpcRequest):
    print(cmd)
    return await rpc_server.execute(cmd)


# =====================================================================================================================
@app.websocket("/ws__ping")
async def ws__ping(websocket: WebSocket):
    await websocket.accept()

    # При подключении отправляем клиенту идентификатор сервера
    await websocket.send_json({
        "channel": "server_id",
        "id": server_id,
    })

    try:
        while True:
            # Держим соединение открытым, игнорируем входящие сообщения
            # если убрать - будет сразу разрыв на окончании кода и соединение заново - бесконечное
            await websocket.receive_text()

    except WebSocketDisconnect:
        pass


# ---------------------------------------------------------------------------------------------------------------------
@app.websocket("/channel__ws_broadcast")
async def channel__ws_broadcast(websocket: WebSocket):
    # 2=PREPARE -----------------------
    await websocket.accept()
    client_id, client_queue = event_broadcaster.register_client()

    # 3=WORK --------------------------
    async with WsServer(
            websocket=websocket,
            queue_client=client_queue,
            callback_onclose=lambda: event_broadcaster.unregister_client(client_id),
            callback_onmessage=None,    # DONT: dont do any!
    ) as wsc:
        await wsc


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=80,

        ws_ping_interval=20,  # каждые 20 секунд сервер шлёт ping
        ws_ping_timeout=10  # если pong не пришёл за 10 сек – разрыв
    )


# =====================================================================================================================
