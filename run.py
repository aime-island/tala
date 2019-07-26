from threading import Thread
from server import start
from webserver import run


frontend = Thread(target=run)
frontend.start()
start()
