from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from django import forms
import logging
import random
import string
import tempfile
from . import views
from os.path import basename
import os
from .application import Application
import json
from .models import Design
from .design import id_generator
from .design import Design as DesignObj
from os import walk



def load_app(design):
    ap = Application()
    for av in ap.avaliable():
        ap.load(av)

    ap.loadDesignObj(design)
    return ap


def allComponents(request):
    ap = Application()
    for av in ap.avaliable():
        ap.load(av)

    types = []
    for c in ap.loaded_component:
        cl = c[3]
        a = []
        for at in cl.attributes():
            a.append({'name': at[0], 'type': at[1], 'required_by': at[2]})
        m = []
        for method in cl.methods():
            m.append({'name': method[0], 'descrition': method[1]})
        types.append({
            'name': c[0].title().replace('_', ' '),
            'description': cl.description(),
            'attributes': a,
            'methods': m,
        })
    return JsonResponse({'components': types})

def get_previous_file(id):
    for (dirpath, dirnames, filenames) in walk('static/incoming'):
        for f in filenames:
            if f.startswith(id):
                ext = f.split('.')[-1]
                print f,ext
                return 'static/incoming/{}'.format(f), ext
    return "static/default.png","png"

def calculate(request):
    if request.method == 'POST':
        incoming = json.loads(request.body)
        inputfile,inputext=get_previous_file(incoming['id'])
        ap = load_app(incoming['design'])
        random = "static/output/"+id_generator(30)+"."+inputext
        ap.execute(inputfile, random)
        return JsonResponse({'picture': '/'+random})
    return JsonResponse({'error': 'POST required'})


def newDesign(request):
    do = DesignObj()
    nid = id_generator(10)
    jd = json.dumps(do.json())
    d = Design(id=id_generator(10),data=jd)
    d.save()
    return JsonResponse({'id': nid,'design':do.json()})
    
def getDesign(request,theid):
    try:
        d = Design.objects.filter(id=theid)[0]
        data = json.loads(d.data)
        return JsonResponse({'id': theid, 'design': data})
    except Exception as e:
        print e
        return JsonResponse({'error':'design not found'})