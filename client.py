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
            resp = json.loads(data)
            if not resp.has_key('error'):
                return resp
            else:
                raise Exception('server responded with: ' + resp['error'])
        else:
            raise Exception('no result')

    def available(self):
        return self.__send__("available", {})

    def loaded(self):
        return self.__send__("loaded", {})

    def load(self, compid):
        return self.__send__('load', {"compid": compid})

    def addInstance(self, componentname, index, method, atts):
        return self.__send__('add_instance', {"index": index,
                                              "cmp": componentname,
                                              "method": method,
                                              "args": atts})

    def removeInstance(self, cid):
        return self.__send__('remove_instance', {"component_id": cid})

    def getDesign(self):
        return self.__send__('get_design', {})

    def setDesign(self, designObj):
        return self.__send__('set_design', designObj)

    def componentMethods(self, componentname):
        return self.__send__('component_methods', {"name": componentname})

    def componentAttributes(self, componentname):
        return self.__send__('component_attributes', {"name": componentname})

    def getImage(self):
        # TODO
        return self.__send__('image', {})

    def getImageByUrl(self, url):
        # TODO
        return self.__send__('image_by_url', {"url": url})

if __name__ == "__main__":
    logger = logging.getLogger("client")

    client = Client()
    client.connect()
    res = client.available()
    logger.info("client.available() returns: %s", res)
    res = client.loaded()
    logger.info("client.loaded() returns: %s", res)
    client.close()
