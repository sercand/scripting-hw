#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


class Request(object):

    def __init__(self, action=None, args=None, req=None):
        self.action = action
        self.args = args
        if not req is None and (action is None or args is None):
            res = json.loads(req)
            self.action = res['action']
            self.args = res['args']

    def json(self):
        json_op = getattr(self.args, "json", None)
        if callable(json_op):
            return {"action": self.action, "args": self.args.json()}
        else:
            return {"action": self.action, "args": self.args}

    def __str__(self):
        return json.dumps(self.json())
