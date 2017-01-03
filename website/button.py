from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django import forms
import logging
import random
import string
import tempfile
from . import views
from os.path import basename
import os

class UploadFileForm(forms.Form):
    image = forms.FileField()

def handle_uploaded_file(f):
    _,tmp = tempfile.mkstemp()
    print tmp
    with open( tmp, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return tmp

def imageButton(request):
    if request.method == 'POST':
        app,_=views.load_app(request)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            inputfile = handle_uploaded_file(request.FILES['image'])
            ff= str(request.FILES[u'image']).split('.')                        
            out='static/output/'+basename(inputfile)+"."+ff[-1]
            try:
                app.execute(inputfile,out)
                os.remove(inputfile)
                return HttpResponseRedirect('/'+out)
            except:
                print "failed to process" 
    return HttpResponseRedirect('/')