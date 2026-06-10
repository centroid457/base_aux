import asyncio
import uuid
from abc import abstractmethod


# =====================================================================================================================
class EventBroadcaster:
    """
    Управляет подключениями клиентов (подписчиков/слушателей) к основной очереди.
    распределяет от основной очереди сообщения на всех клиентов.
    """
    main_queue: asyncio.Queue
    task_broadcasting: asyncio.Task = None

    def __init__(self, main_queue: asyncio.Queue | None = None):
        if isinstance(main_queue, asyncio.Queue):
            self.main_queue = main_queue
        elif main_queue is None:
            self.main_queue = asyncio.Queue()
        else:
            raise Exception(f"incorrect input type {main_queue!r}")

        self.clients: dict[str, asyncio.Queue] = {}

    async def start_task(self):
        self.task_broadcasting = asyncio.create_task(self._broadcasting())

    # -----------------------------------------------------------------------------------------------------------------
    async def _broadcasting(self):
        """
        GOAL: постоянное перенаправление сообщений из основной очереди на всех клиентов
        """
        while True:
            try:
                msg = await self.main_queue.get()

                for q in self.clients.values():
                    try:
                        await q.put(msg)
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
    async def broadcast(self, msg: dict):
        """Отправить сообщение всем клиентам.
        можно взять main_queue и напрямую посылать!

        ITS A QUICK METHOD! DONT DO ANYTHING!!! JUST PLACE INTO MAIN_QUEUE!!!!
        """
        try:
            print(f"[EventBroadcaster].broadcast({msg})")
        except:
            pass
        await self.main_queue.put(msg)

    # -----------------------------------------------------------------------------------------------------------------


# =====================================================================================================================
class Nest_EventBroadcasterImplemented:
    _event_broadcaster: EventBroadcaster | None = None

    def __init__(self, *args, **kwargs):
        # DONT USE ANYTHING HERE!
        super().__init__(*args, **kwargs)

    @abstractmethod
    def event_broadcaster__setup(self, eb: EventBroadcaster) -> None:
        self._event_broadcaster = eb

    async def event_broadcaster__broadcast(self, msg: dict) -> None:
        if self._event_broadcaster is not None:
            await self._event_broadcaster.broadcast(msg)


# =====================================================================================================================
