from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django import forms
import logging
import random
import string


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


def updateCmp(request):
    print "thepost request", request
    if request.method == 'POST':
        print request.POST
        form = ComponentUpdate(request.POST)
        if form.is_valid():
            cmpid = request.POST['cmpid']
            cmptype = request.POST['cmptype']
            cmpmethod = request.POST['cmpmethod']
            print "thepost form is valid", cmpid, ":", cmptype, ':', cmpmethod
            if 'update' in request.POST:
                print "update"
                for c in components:
                    if c['id'] == cmpid:
                        c['type'] = cmptype
                        c['selected_method'] = cmpmethod
                        break
            elif 'delete' in request.POST:
                print "delete"
                idx = [i for i, a in enumerate(components) if a[
                    'id'] == cmpid][0]
                print idx
        else:
            print "thepost is not valid", form
    return HttpResponseRedirect('/')


def addCmp(request):
    print "thepost request", request
    if request.method == 'POST':
        print request.POST
    components.append({
        'id': id_generator(),
        'type': '',
        'methods': ['resize_width',
                    'resize_height',
                    'resize_with_value',
                    'resize_with_ratio'],
        'selected_method': '',
        'attributes': [{
            'value': 400,
            'type': 'number',
            'name': 'width',
            'label': 'Width'
        }],
    })
    return HttpResponseRedirect('/')


def index(request):
    return render(request, 'mat.html', thedata)
