from typing import *
import asyncio
import uuid
from abc import ABC, abstractmethod
import datetime
import time


# =====================================================================================================================
class EventBroadcaster:
    """
    Управляет подключениями клиентов (подписчиков/слушателей) к основной очереди.
    распределяет от основной очереди сообщения на всех клиентов.
    """
    eb_queue: asyncio.Queue
    eb_task: asyncio.Task = None
    eb_history: list[dict]  # TODO: deque?

    def __init__(self, eb_queue: asyncio.Queue | None = None):
        if isinstance(eb_queue, asyncio.Queue):
            self.eb_queue = eb_queue
        elif eb_queue is None:
            self.eb_queue = asyncio.Queue()
        else:
            raise Exception(f"incorrect input type {eb_queue!r}")

        self.eb_history = []
        self.clients: dict[str, asyncio.Queue] = {}

    async def start_task(self):
        self.eb_task = asyncio.create_task(self._broadcasting())

    # -----------------------------------------------------------------------------------------------------------------
    async def _broadcasting(self):
        """
        GOAL: постоянное перенаправление сообщений из основной очереди на всех клиентов
        """
        while True:
            try:
                event = await self.eb_queue.get()
                self.eb_history.append(event)

                for q in self.clients.values():
                    try:
                        await q.put(event)
                    except asyncio.CancelledError:
                        raise
                    except Exception as exc:
                        print(f"{exc!r}")
            except asyncio.CancelledError:
                return

    # -----------------------------------------------------------------------------------------------------------------
    def register_client(self) -> tuple[str, asyncio.Queue]:
        client_id = str(uuid.uuid4())
        client_queue = asyncio.Queue()
        self.clients[client_id] = client_queue
        return client_id, client_queue

    def unregister_client(self, client_id: str):
        self.clients.pop(client_id, None)

    # -----------------------------------------------------------------------------------------------------------------
    async def broadcast(self, data: dict) -> None:
        """Отправить сообщение всем клиентам.
        можно взять eb_queue и напрямую посылать!

        ITS A QUICK METHOD! DONT DO ANYTHING!!! JUST PLACE INTO MAIN_QUEUE!!!!
        """
        print(f"[EventBroadcaster].broadcast({data})")
        await self.eb_queue.put(data)

    # -----------------------------------------------------------------------------------------------------------------


# =====================================================================================================================
class Nest_EventBroadcasterImplemented:
    _eb__obj: EventBroadcaster | None = None
    _eb__aux: dict | None = None

    def __init__(self, *args, eb: EventBroadcaster | None = None, eb__aux: dict | None = None, **kwargs):
        self._eb__obj = eb
        self._eb__aux = eb__aux or {}
        super().__init__(*args, **kwargs)

    async def eb__broadcast(self, channel: str | None = None, **kwargs) -> None:
        # 0=-------
        if self._eb__obj is None:
            return

        # 1=MAKE DATA -------
        load = dict(
            channel=channel,
            **self._eb__aux,
            **kwargs,
        )

        # 2=SEND -------
        await self._eb__obj.broadcast(load)


# =====================================================================================================================
