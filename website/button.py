from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django import forms
import logging
import random
import string
import tempfile


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

logger = logging.getLogger(__name__)

lastid = 2

types = [{'name': 'Fx', 'value': 'fx'},
         {'name': 'Resize', 'value': 'resize'},
         {'name': 'Rotate', 'value': 'rotate'},
         {'name': 'Crop', 'value': 'crop'}]
components = [{
    'id': id_generator(),
    'type': 'fx',
    'methods': ['resize_width',
                'resize_height',
                'resize_with_value',
                'resize_with_ratio'],
    'selected_method':'resize_with_value',
    'attributes': [{
        'value': 400,
        'type': 'number',
        'name': 'width',
        'label': 'Width'
    }],
}, {
    'id': id_generator(),
    'type': 'crop',
    'methods': ['resize_width',
                'resize_height',
                'resize_with_value',
                'resize_with_ratio'],
    'selected_method':'',
    'attributes': [{
        'value': 400,
        'type': 'number',
        'name': 'width',
        'label': 'Width'
    }, {
        'value': 300,
        'type': 'number',
        'name': 'height',
        'label': 'Height'
    }],
}]
thedata = {'component_types': types, 'components': components}


class ComponentUpdate(forms.Form):
    cmpid = forms.CharField(required=True)
    cmptype = forms.CharField()
    cmpmethod = forms.CharField()

class UploadFileForm(forms.Form):
    file = forms.FileField()

def handle_uploaded_file(f):
    tmp = tempfile.NamedTemporaryFile()
    with open( tmp, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def imageButton(request):
    print "HERE I AM"
    if request.method == 'POST':
        myfile = request.FILES['image']
        handle_uploaded_file(myfile)
    return HttpResponseRedirect('/')
""""
        form = UploadFileForm(request.POST, request.FILES)
        print request.POST, request.FILES
        print form
        if form.is_valid():
            print "IS VALID"
            handle_uploaded_file(request.FILES['image'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return HttpResponseRedirect('/')"""