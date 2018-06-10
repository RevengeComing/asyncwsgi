import io
import httptools


class Request():
    __slots__ = [
        "parser", "body", "url", "headers", "pending"
    ]
    def __init__(self):
        self.parser = httptools.HttpRequestParser(self)
        self.body = io.BytesIO()
        self.url = None
        self.headers = []
        self.pending = True

    def feed(self, data):
        self.parser.feed_data(data)

    @property
    def method(self):
        return self.parser.get_method()

    @property
    def http_version(self):
        return self.parser.get_http_version()

    @property
    def should_upgrade(self):
        return self.parser.should_upgrade()     

    def on_message_begin(self):
        pass

    def on_url(self, url):
        self.url = url

    def on_header(self, name, value):
        self.headers.append((name, value))

    def on_headers_complete(self):
        pass

    def on_body(self, body):
        self.body.write(body)

    def on_message_complete(self):
        self.pending = False

    def on_chunk_header(self):
        pass

    def on_chunk_complete(self):
        pass

    def process(self):
        pass


class Response():
    pass