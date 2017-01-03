from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django import forms
import logging
import random
import string
import tempfile
from django.db import models



class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

class UploadFileForm(forms.Form):
    image = forms.FileField()

def handle_uploaded_file(f):
    _,tmp = tempfile.mkstemp()
    print tmp
    with open( tmp, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def imageButton(request):
    print "HERE I AM"
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print request.POST, request.FILES
        print form
        if form.is_valid():
            print "IS VALID"
            handle_uploaded_file(request.FILES['image'])
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return HttpResponseRedirect('/')