#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from threading import Thread, Lock, Condition
import socket
from application import Application
import request
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ClientAgent(Thread):
    """
    ClientAgent handles client connection
    """

    def __init__(self, conn, addr, app):
        self.conn = conn
        self.claddr = addr
        self.app = app
        Thread.__init__(self)

    def available(self, args):
        lst = self.app.avaliable()
        return json.dumps({"components": lst})

    def run(self):
        inp = self.conn.recv(10240)
        while inp:
            req = request.Request(req=inp)
            logger.debug('client send "%s" action and params: %s',
                         req.action, req.args)
            if req.action == "run":
                self.conn.send(json.dumps({"error": "invalid action"}))
                inp = self.conn.recv(10240)
                continue
            func = getattr(self, req.action, None)
            if callable(func):
                res = func(req.args)
                if isinstance(res, str):
                    self.conn.send(res)
                else:
                    self.conn.send(json.dumps(
                        {"error": "internal execution error"}))
            else:
                self.conn.send(json.dumps({"error": "unknown action"}))
            inp = self.conn.recv(10240)
        logger.debug('client %s is terminating', self.claddr)
        self.conn.close()


class Server(object):
    """
    Server is server implementation
    """

    def __init__(self, host='', port=4000):
        self.host = host
        self.port = port

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(1)
        logger.info('starting server on :%d', self.port)
        while True:
            conn, addr = s.accept()
            logger.debug('connected by :%s', addr)
            a = ClientAgent(conn, addr, Application())
            a.start()

if __name__ == "__main__":
    srv = Server()
    logger = logging.getLogger("server")
    srv.run()
