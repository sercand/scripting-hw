#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import string
import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class DesignEntry:

    def __init__(self):
        self.id = ""
        self.method = ""
        self.options = {}
        self.index = -1


class Design:

    def __init__(self):
        self.cmps = []

    def push(self, entry):
        self.cmps.append(entry)

    def size(self):
        return len(self.cmps)

    def save_to(self, path):
        with open(path, 'w') as f:
            json.dump(self, f)
