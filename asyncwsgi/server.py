import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

from .models import Request
from .wsgi import run_with_cgi


class AsyncWSGIServer(asyncio.Protocol):
    __slots__ = [
        'transport', 'request', 'pending_request'
    ]

    def __init__(self, app):
        self.app = app
    
    def connection_made(self, transport):
        self.transport = transport
        self.request = None
        self.pending_request = None

    def data_received(self, data):
        if self.pending_request:
            self.request.feed(data)
        else:
            self.request = self.pending_request = Request()
            self.request.feed(data)

        if not self.request.pending:
            _in = self.request.body
            _out = self.transport
            run_with_cgi(self.app, self.request, _in, _out)
            self.pending_request = None
            self.transport.close()

    def connection_lost(self, exc):
        pass


def run(app, host="localhost", port=8000):
    loop = asyncio.get_event_loop()
    
    coro = loop.create_server(lambda: AsyncWSGIServer(app), host, port)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()