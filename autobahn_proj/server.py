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
import redis as redis
from time import sleep

from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        i = 0
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        google = False
        yandex = False
        instagram = False

        payload = str(payload)
        print(payload)
        if r'\xd' in payload:
            index = payload.find('=')
            part = payload[index:].replace(r'\x', '%').upper()
            payload = payload[2:index] + part[:-1]
        else:
            payload = payload[2:-1]

        while not google or not yandex or not instagram:
            google = r.get(payload + 'Google') == b'Google'
            yandex = r.get(payload + 'Yandex') == b'Yandex'
            instagram = r.get(payload + 'Instagram') == b'Instagram'

            self.sendMessage(bytes("Google %s" % google, encoding='utf-8'), isBinary)
            self.sendMessage(bytes("Yandex %s" % yandex, encoding='utf-8'), isBinary)
            self.sendMessage(bytes("Instagram %s" % instagram, encoding='utf-8'), isBinary)
            if i >= 30:
                if not google:
                    self.sendMessage(b'google-error')
                if not yandex:
                    self.sendMessage(b'yandex-error')
                if not instagram:
                    self.sendMessage(b'instagram-error')
                break
            sleep(1)
            i += 1
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
