try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass
import gunicorn.workers.base as base


class GunicornWorker(base.Worker):
    pass