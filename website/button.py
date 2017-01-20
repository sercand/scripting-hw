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

class UploadFileForm(forms.Form):
    image = forms.FileInput()

class UploadFileForm2(forms.Form):
    image = forms.ImageField(widget=forms.FileInput())
    id = forms.CharField()

def handle_uploaded_file(f):
    _,tmp = tempfile.mkstemp()
    print tmp
    with open( tmp, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return tmp

def imageButton(request):
    if request.method == 'POST':
        app, _,_ = views.load_app(request)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            inputfile = handle_uploaded_file(request.FILES['image'])
            ff= str(request.FILES[u'image']).split('.')
            out='static/output/'+basename(inputfile)+"."+ff[-1]
            try:
                app.execute(inputfile,out)
                os.remove(inputfile)
                return JsonResponse({'picture':'/'+out})
            except Exception as e:
                return JsonResponse({'error':'failed to process: {}'.format(e)})
    return JsonResponse({'error':'POST with a file required'})

def uploadImage(request):
    print request.method 
    if request.method == 'POST':
        form = UploadFileForm2(request.POST, request.FILES)
        if form.is_valid():
            inputfile = handle_uploaded_file(request.FILES['image'])
            ff = str(request.FILES[u'image']).split('.')
            out = 'static/incoming/'+ request.POST['id']+"."+ff[-1]
            os.rename(inputfile, out)
            return JsonResponse({'picture':'/'+out})
    return JsonResponse({'error':'POST with a file required'})