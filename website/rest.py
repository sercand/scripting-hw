from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
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

def allComponents(request):
    ap = Application()
    for av in ap.avaliable():
        ap.load(av)

    types = []
    for c in ap.loaded_component:
        cl = c[3]
        a = []
        for at in cl.attributes():
            a.append({'name':at[0],'type':at[1],'required_by':at[2]})
        m = []
        for method in cl.methods():
            m.append({'name':method[0],'descrition':method[1]})
        types.append({
            'name': c[0].title().replace('_', ' '),
            'description': cl.description(),
            'attributes':a,
            'methods':m,
        })
    return JsonResponse({'components':types})

def calculate(request):
    if request.is_ajax():
        if request.method == 'POST':
            print 'Raw Data: "%s"' % request.raw_post_data
            incoming = json.loads(request.raw_post_data)
            design = incoming['design']
            incomngId = incoming['id']
            
            # TODO

            JsonResponse({'picture':'/static/output/TODO'})

    return JsonResponse({'error':'POST required'})