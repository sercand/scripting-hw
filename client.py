#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import design
import request
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Client(object):

    def __init__(self, server_host='127.0.0.1', server_port=4000):
        self.host = server_host
        self.port = server_port
        self.conn = None

    def connect(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.host, self.port))
        self.conn = conn
        logger.debug('connected to server')        

    def close(self):
        logger.debug('closing connection with server')
        self.conn.close()
        self.conn = None

    def __send__(self, action, args):
        if self.conn is None:
            raise Exception('before executing run connect')
        req = request.Request(action=action, args=args)
        self.conn.send(str(req))
        data = self.conn.recv(10240)
        if data:
            return json.loads(data)
        else:
            # TODO raise Error
            return None

    def available(self):
        return self.__send__("available", {})
    def loaded(self):
        return self.__send__("loaded", {})

if __name__ == "__main__":
    logger = logging.getLogger("client")

    client = Client()
    client.connect()
    res = client.available()
    logger.info("client.available() returns: %s", res)
    res = client.loaded()
    logger.info("client.loaded() returns: %s", res)
    client.close()
