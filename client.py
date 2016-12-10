#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import design
import request
import json
import logging
from threading import Thread, Lock, Condition

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Client(object):

    def __init__(self, server_host='127.0.0.1', server_port=4000):
        self.host = server_host
        self.port = server_port
        self.conn = None
        self.lock = Lock()

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
        self.lock.acquire()
        print "__send__", action
        if self.conn is None:
            raise Exception('before executing run connect')
        req = request.Request(action=action, args=args)
        print self.conn.send(str(req))
        data = self.conn.recv(10240)
        if data:
            resp = json.loads(data)
            if not resp.has_key('error'):
                print "__receive__", action
                self.lock.release()
                return resp
            else:
                raise Exception('server responded with: ' + resp['error'])
        else:
            raise Exception('no result')

    def __send_image__(self, action, image_data):
        self.lock.acquire()
        total = len(image_data)
        print total, "bytes image data"

        self.conn.send(json.dumps({"action": action, "args": {
            "total": total}}))

        sent = 0
        step = 9000

        while True:
            last = sent + step
            print "send", sent, "to", last
            breakonthis = False
            if last >= total:
                last = total
                breakonthis = True
            data = image_data[sent:last]
            self.conn.send(data)
            sent = last
            if breakonthis:
                break
        self.lock.release()

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

    def getImage(self, local_url):
        with open(local_url, "rb") as f:
            data = f.read()
            strr = data.encode("base64")
        return self.__send_image__('image', strr)

    def getImageByUrl(self, url):
        return self.__send__('image_by_url', {"url": url})


if __name__ == "__main__":
    logger = logging.getLogger("client")

    client = Client()
    client.connect()
    res = client.available()
    logger.info("client.available() returns: %s", res)
    res = client.loaded()
    logger.info("client.loaded() returns: %s", res)
    res = client.load('fx')
    logger.info("client.load() returns: %s", res)
    res = client.loaded()
    logger.info("client.loaded() returns: %s", res)
    res = client.addInstance('fx',3,'gamma',{'adj': 0.5})
    ins_id = res['id']
    logger.info("client.addInstance() returns: %s", res)
    res = client.removeInstance(ins_id)
    logger.info("client.removeInstance() returns: %s", res)
    client.close()
