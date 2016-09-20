###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################
import redis
from time import sleep, time
import logging
import json
from raven import Client
from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

client = Client('https://8ff8d6c9c1e2413eb517774e481074c1:4a819bdfaa644649978440d6ee752545@sentry.io/97142')


class MyServerProtocol(WebSocketServerProtocol):
    i = 0

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        self.request = request
        "prefix.job.{uuid}"

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        payload = json.loads(r.get(payload.decode()).decode())

        def handler(message):
            state_message = payload[message['data'].decode().replace('["', '').replace('"]', '')]
            self.sendMessage(bytes(state_message + ' True', encoding='UTF-8'), isBinary)
            payload.pop(payload.keys()[payload.values().index(state_message)])

            if not payload:
                state.unsubscribe()
                state.close()
                thread.stop()
                self.sendMessage(b'DONE')

        state = r.pubsub()
        state.subscribe(**{'task_state': handler})
        thread = state.run_in_thread(sleep_time=0.01)

        # echo back message verbatim

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    try:
        import asyncio
    except ImportError:
        # Trollius >= 0.3 was renamed
        import trollius as asyncio

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
