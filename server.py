#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from threading import Thread, Lock, Condition
import socket
from application import Application
import request
import json
import os
import imp
import inspect
from wand.image import Image
import base64
import StringIO
from io import BytesIO

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
        self.lock = Lock()
        Thread.__init__(self)

    def available(self, args):
        lst = self.app.avaliable()
        return json.dumps({"components": lst})

    def loaded(self, args):
        lst = self.app.loaded()
        return json.dumps({"components": lst})

    def load(self, args):
        self.app.load(args["compid"])
        lst = self.app.loaded()
        return json.dumps({"components": lst})

    def add_instance(self, args):
        _id = self.app.addInstance(args["cmp"], args["index"], args["method"])
        i = self.app.instance(_id)
        for a in args["args"]:
            i[a] = args["args"][a]
        print i.__dict__
        return json.dumps({"id": _id})

    def remove_instance(self, args):
        self.app.removeInstance(args["component_id"])
        return json.dumps({"components": ""})

    def get_design(self, args):
        return json.dumps(self.app.design.json())

    def set_design(self, args):
        i = self.app.loadDesignObj(args)
        return json.dumps(self.app.design.json())

    def component_methods(self, args):
        compid = args["name"]
        themodule = imp.load_source(compid, "components/" + compid + ".py")
        className = None
        for xn, obj in inspect.getmembers(themodule):
            if inspect.isclass(obj):
                if str(obj).startswith(compid):
                    className = str(obj).split('.')[1]
        class_ = getattr(themodule, className)
        v = class_().methods()

        ret_dict = {}
        for i in v:
            ret_dict[i[0]] = i[1]
        return json.dumps(ret_dict)

    def component_attributes(self, args):
        compid = args["name"]
        themodule = imp.load_source(compid, "components/" + compid + ".py")
        className = None
        for xn, obj in inspect.getmembers(themodule):
            if inspect.isclass(obj):
                if str(obj).startswith(compid):
                    className = str(obj).split('.')[1]
        class_ = getattr(themodule, className)
        v = class_().attributes()

    def __upload_image__(self, data):
        self.lock.acquire()
        req = request.Request(req=data)
        total = req.args['total']
        imagedata = ""

        inp = self.conn.recv(10240)

        while inp:
            imagedata += inp
            if len(imagedata) >= total:
                break
            else:
                got = len(imagedata)
                remain = total - got
                if remain < 10240:
                    inp = self.conn.recv(remain)
                else:
                    inp = self.conn.recv(10240)

        image_binary = base64.b64decode(imagedata)

        with Image(blob=image_binary) as img:
            for c in self.app.design.cmps:
                self.app.callMethod(c.id, c.method, img)
            output = BytesIO()
            img.save(file=output)
            imageStr = base64.b64encode(output.getvalue()) #output.read().encode('base64')
            total = len(imageStr)
            self.conn.send(json.dumps({"total": total}))
            self.conn.sendall(imageStr)

        self.lock.release()

    def run(self):
        inp = self.conn.recv(10240)
        while inp:
            self.lock.acquire()
            req = request.Request(req=inp)
            logger.debug('client send "%s" action and params: %s',
                         req.action, req.args)
            if req.action == "run":
                self.conn.send(json.dumps({"error": "invalid action"}))
                self.lock.release()
                inp = self.conn.recv(10240)
                continue
            elif req.action == "image":
                self.lock.release()
                self.__upload_image__(inp)
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
            self.lock.release()
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
    srv = Server(port=4000)
    logger = logging.getLogger("server")
    srv.run()
