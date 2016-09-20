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


        # google = False
        # yandex = False
        # instagram = False

        # payload = str(payload)
        # print(payload)
        # if r'\xd' in payload:  # if user entered cyrillic keywords they will be formatted in a simple byte literals
        #     try:
        #         index = payload.find('=')
        #         part = payload[index:].replace(r'\x', '%').upper()
        #         payload = payload[2:index] + part[:-1]
        #     except:
        #         client.captureException()
        # else:
        #     payload = payload[2:-1]
        def handler(message):
            state_message = payload[message['data'].decode().replace('["', '').replace('"]', '')]
            self.sendMessage(bytes(state_message + 'True', encoding='UTF-8'), isBinary)
            # payload.pop(state_message)
            self.i += 1

            if self.i == 3:
                state.unsubscribe()
                state.close()
                thread.stop()

        state = r.pubsub()
        state.subscribe(**{'task_state': handler})
        thread = state.run_in_thread(sleep_time=0.01)


        # while not google or not yandex or not instagram:  # requests message that the task is executed from the Redis
        #     google = r.get(payload + 'Google') == b'Google'
        #     yandex = r.get(payload + 'Yandex') == b'Yandex'
        #     instagram = r.get(payload + 'Instagram') == b'Instagram'
        #
        #     self.sendMessage(bytes("Google %s" % google, encoding='utf-8'), isBinary)  # sends a message to the client about the status of the task.
        #     self.sendMessage(bytes("Yandex %s" % yandex, encoding='utf-8'), isBinary)
        #     self.sendMessage(bytes("Instagram %s" % instagram, encoding='utf-8'), isBinary)
        #     if i >= 30:  # if the job is not be executed, sends an error to the client
        #         if not google:
        #             self.sendMessage(b'google-error')
        #         if not yandex:
        #             self.sendMessage(b'yandex-error')
        #         if not instagram:
        #             self.sendMessage(b'instagram-error')
        #         break
        #     sleep(1)
        #     i += 1
        self.sendMessage(b'DONE')

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
