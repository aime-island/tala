import sys
import json

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import Data

from utils.text import save_corpus
from utils.files import read_files
from utils.utterances import make_queue, save_utterances
from threading import Thread

from queue import Queue, Empty
utterances_audio = Queue()
utterances_transcript = Queue()


class GetFiles(WebSocketServerProtocol):
    def onMessage(self, payload, isBinary):
        files = read_files()
        obj = json.dumps(files, ensure_ascii=False).encode('utf8')
        self.sendMessage(obj, isBinary=False)


class GetText(WebSocketServerProtocol):
    utterances_unread = Queue()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            self.message = json.loads(payload.decode('utf8'))
            if self.message['type'] == 'select_file':
                global selected_file
                selected_file = self.message['data']
                self.utterances_unread = Queue()
                self.unread_worker = Thread(
                    target=make_queue,
                    args=(self.utterances_unread, selected_file))
                self.unread_worker.start()
            else:
                try:
                    utt = self.utterances_unread.get(block=True, timeout=1)
                    obj = json.dumps(utt, ensure_ascii=False).encode('utf8')
                    self.sendMessage(obj, isBinary=False)
                except Empty:
                    obj = {'id': 'none', 'utterance': 'SKJALIÐ ER BÚIÐ'}
                    obj = json.dumps(obj, ensure_ascii=False).encode('utf8')
                    self.sendMessage(obj, isBinary=False)


class SubmitText(WebSocketServerProtocol):

    def onMessage(self, payload, isBinary):
        if isBinary:
            save_corpus(payload, self.name, self)
            self.name = ''
        else:
            self.name = payload.decode('utf8')


class Audio(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        self.save_worker = Thread(
            target=save_utterances,
            args=(utterances_transcript, utterances_audio, selected_file))
        self.save_worker.start()

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    def onMessage(self, payload, isBinary):
        if not isBinary:
            self.message = json.loads(payload.decode('utf8'))
            utterances_transcript.put(self.message)
        else:
            utterances_audio.put(payload)


def start():

    log.startLogging(sys.stdout)

    fileFactory = WebSocketServerFactory()
    fileFactory.protocol = GetFiles
    fileFactory.startFactory()
    fResource = WebSocketResource(fileFactory)

    textFactory = WebSocketServerFactory()
    textFactory.protocol = GetText
    textFactory.startFactory()
    gResource = WebSocketResource(textFactory)

    submitTextFactory = WebSocketServerFactory()
    submitTextFactory.protocol = SubmitText
    submitTextFactory.startFactory()
    sResource = WebSocketResource(submitTextFactory)

    AudioFactory = WebSocketServerFactory()
    AudioFactory.protocol = Audio
    AudioFactory.startFactory()
    aResource = WebSocketResource(AudioFactory)

    # Establish a dummy root resource
    root = Data("", "text/plain")
    root.putChild(b"gettext", gResource)
    root.putChild(b"submittext", sResource)
    root.putChild(b"getfiles", fResource)
    root.putChild(b"audio", aResource)

    # both under one Twisted Web Site
    site = Site(root)
    reactor.listenTCP(9000, site)

    reactor.run()
