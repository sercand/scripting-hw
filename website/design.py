#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import string
import random


def id_generator(size=6, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))


class DesignEntry:

    def __init__(self, cmp, cmp_name):
        self.id = id_generator()
        self.cmp_name = cmp_name
        self.component = cmp
        self.index = -1
        self.method = ""

    def json(self):
        return {"id": self.id,
                "cmp": self.cmp_name,
                "method": self.method,
                "args": self.component.__dict__}


class Design:

    def __init__(self):
        self.cmps = []

    def push(self, entry):
        if entry.index < 0:
            entry.index = self.size()
            self.cmps.append(entry)
        else:
            self.cmps.insert(entry.index, entry)

    def size(self):
        return len(self.cmps)

    def save_to(self, path):
        with open(path, 'w') as f:
            json.dump(self.json(), f)

    def json(self):
        cmps = []
        for x in self.cmps:
            cmps.append({"id": x.id,
                         "cmp": x.cmp_name,
                         "method": x.method,
                         "args": x.component.__dict__})

        return {"cmps": cmps}

    def get_cmp(self, cid):
        for x in self.cmps:
            if x.id == cid:
                return x.component
        raise Exception(id + ' not found')

    def get_entry(self, cid):
        for x in self.cmps:
            if x.id == cid:
                return x
        raise Exception(id + ' not found')

    def remove(self, id):
        index = -1
        for x in self.cmps:
            index += 1
            if x.id == id:
                break
        if index > -1:
            self.cmps.pop(index)
