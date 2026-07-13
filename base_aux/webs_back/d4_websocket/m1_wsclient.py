import asyncio
from typing import Never, NoReturn

from starlette.websockets import WebSocket, WebSocketDisconnect

from base_aux.aux_dict.m1_dict_aux import json__ensure_serializable
from base_aux.aux_paradigm.m2_aio import TYPES__CALLBACK_AIO__DATA, AioAux
from base_aux.base_values.m3_exceptions import Exc__UnExpectedExc
from base_aux.tasks.m1_tasks_bg import Nest_TasksBg_AbcAio


# ======================================================================================================================
class WsClient(Nest_TasksBg_AbcAio):
    """
    GOAL
    used in FastApi
    as organised IO transportation/execution

    SPECIALLY CREATED FOR
        @app.websocket("/ws__broadcast")
        async def ws__client(websocket: WebSocket):
    """
    def __init__(
            self,
            websocket: WebSocket,
            queue_client: asyncio.Queue,
            callback_onmessage: TYPES__CALLBACK_AIO__DATA = None,
            callback_onclose: TYPES__CALLBACK_AIO__DATA = None,

            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.websocket = websocket
        self.queue_to_client = queue_client

        self.income_executor: TYPES__CALLBACK_AIO__DATA = callback_onmessage
        # self.outcome_executor = self._queue_to_ws__retranslator
        self._tasks_bg__callback_onexit: TYPES__CALLBACK_AIO__DATA = callback_onclose

    def _tasks_bg__create_start(self) -> None:
        self._event_stop.clear()    # DONT FORGET!!!

        self._tasks_bg__extend(self._loop_outcome())
        self._tasks_bg__extend(self._loop_income())

    # ==================================================================================================================
    async def outcome_executor(self, data: dict) -> None:
        await self.websocket.send_json(json__ensure_serializable(data))

    # ------------------------------------------------------------------------------------------------------------------
    # LOOPS
    async def _loop_outcome(self) -> Never | NoReturn:
        """
        GOAL: resend all msgs from clientQueue to clientWS

        just a _queue_to_ws__retranslator
        """
        print(f"[self.websocket.msg_outcome] start monitor")
        try:
            while not self._event_stop.is_set():
                msg_outcome = await self.queue_to_client.get()
                print(f"{msg_outcome=}")
                try:
                    await self.outcome_executor(msg_outcome)
                except asyncio.CancelledError:
                    raise
                except Exception as exc:
                    print(f"[self.websocket.msg_outcome]{exc!r}")
                    # клиент отвалился – выходим из задачи
                    break

        except asyncio.CancelledError:
            raise

        except WebSocketDisconnect:
            pass

        except BaseException as exc:
            Exc__UnExpectedExc(f"{exc!r}")

    # ------------------------------------------------------------------------------------------------------------------
    async def _loop_income(self) -> Never | NoReturn:
        try:
            while not self._event_stop.is_set():
                data = await self.websocket.receive_json()
                await AioAux(self.income_executor).callback_sync_aio__execute(data)

        except asyncio.CancelledError:
            raise

        except WebSocketDisconnect:
            pass

        except BaseException as exc:
            Exc__UnExpectedExc(f"{exc!r}")


# ======================================================================================================================
