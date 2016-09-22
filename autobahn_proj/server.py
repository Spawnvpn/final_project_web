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
import settings
import sqlite3
import hashlib
from raven import Client
from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

client = Client(settings.RAVEN_URL)


class MyServerProtocol(WebSocketServerProtocol):

    done_count = 0

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        self.request = request
        "prefix.job.{uuid}"

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        r = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)

        def handler(message):
            self.sql_conn = sqlite3.connect(settings.DB_PATH)
            task_hash = message['data'].decode().replace('["', '').replace('"]', '')
            spider_state = self.sql_conn.execute('SELECT job, keywords FROM image_aggregator_task WHERE job="%s"' % task_hash).fetchone()
            # keywords_hash = hashlib.md5(spider_state[1])
            task_dict = r.get(hashlib.md5(spider_state[1].encode('unicode')))
            print(task_dict)
            if task_hash == spider_state[0]:
                self.sendMessage(bytes('True', encoding='UTF-8'), isBinary)
            # self.sendMessage(bytes(spider_state + ' True', encoding='UTF-8'), isBinary)
            spiders_quantity = int(r.get('quantity_spiders').decode())

            self.done_count += 1
            if task_hash == 'error':
                self.done_count += 1

            if self.done_count == spiders_quantity:
                state.unsubscribe()
                state.close()
                self.sql_conn.close()
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
