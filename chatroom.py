from os import path as op
import sys

import tornado.web
import tornadio
import tornadio.router
import tornadio.server

import thread
import time

global connections

def readLog(threadName, delay):
    global connections
    file = open(sys.argv[1], 'r')
    while True:
        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(delay)
            file.seek(where)
        else:
            print threadName, 'read: ', line,
            for connection in connections:
                for p in connection.participants:
                    p.send(line)
                break

ROOT = op.normpath(op.dirname(__file__))

class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render("index.html")

class ChatConnection(tornadio.SocketConnection):
    # Class level variable
    participants = set()

    def __init__(self, protocol, io_loop, heartbeat_interval):
        tornadio.SocketConnection.__init__(self, protocol, io_loop, heartbeat_interval)

    def on_open(self, *args, **kwargs):
        self.participants.add(self)
        self.send("CONNECTED")
        global connections
        connections.add(self)
        
    def on_message(self, message):
        for p in self.participants:
            p.send(message)

    def on_close(self):
        self.participants.remove(self)
        self.send("DISCONNECTED")
        global connections
        connections.remove(self)

#use the routes classmethod to build the correct resource
ChatRouter = tornadio.get_router(ChatConnection)

#configure the Tornado application
application = tornado.web.Application(
    [(r"/", IndexHandler, None), ChatRouter.route()],
    enabled_protocols = ['websocket',
                         'flashsocket',
                         'xhr-multipart',
                         'xhr-polling'],
    flash_policy_port = 843,
    flash_policy_file = op.join(ROOT, 'flashpolicy.xml'),
    socket_io_port = 8001
)

if __name__ == "__main__":
    # initialize login
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    
    # initliaze connections instance
    global connections
    connections = set()
    
    try:
        thread.start_new_thread(readLog, ("LogReader", 1,) )
    except:
        print "Error: unable to start thread"
    
    # start server
    tornadio.server.SocketServer(application)
    


