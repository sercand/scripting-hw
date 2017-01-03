import logging
import json
import random
import string
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from . import design
from . import application
from . import button
logger = logging.getLogger(__name__)

COOKIE_DESIGN = "design"


def load_app(request):
    ap = application.Application()
    for av in ap.avaliable():
        ap.load(av)

    types = []
    loaded = ap.loaded()
    for t in loaded:
        types.append({'value': t, 'name': t.title().replace(
            '_', ' '), 'description': loaded[t]})

    cdesign = request.COOKIES.get('design')
    if cdesign is None:
        d = design.Design()
        cdesign = json.dumps(d.json())

    ap.loadDesignObj(json.loads(cdesign))
    cmps = []
    for c in ap.design.cmps:
        ccc = {'id': c.id, 'type': c.cmp_name, 'selected_method': c.method}
        mlist = []
        for m in c.component.methods():
            mlist.append(m[0])
        ccc['methods'] = mlist
        atts = []
        for a in c.component.attributes():
            if c.method in a[2]:
                att = {
                    'type': 'number',
                    'name': a[0],
                    'label': a[0].title().replace('_', ' ')
                }
                try:
                    val = c.component[a[0]]
                    att['value'] = val
                except:
                    att['value'] = 0
                atts.append(att)
        ccc['attributes'] = atts
        cmps.append(ccc)
    return ap, {'component_types': types, 'components': cmps}


def updateCmp(request):
    blacklist = ['cmpid', 'cmptype', 'cmpmethod', 'update', 'delete']
    app, _ = load_app(request)
    if request.method == 'POST':
        print request.POST
        cmpid = request.POST['cmpid']
        cmptype = request.POST['cmptype']
        if 'update' in request.POST:
            try:
                comp = app.design.get_entry(cmpid)
                if not cmptype == comp.cmp_name:
                    app.removeInstance(cmpid)
                    ncmpid = app.addInstance(cmptype, comp.index, '')
                    comp = app.design.get_entry(ncmpid)
                    comp.id = cmpid
                if 'cmpmethod' in request.POST:
                    cmpmethod = request.POST['cmpmethod']
                    if not cmpmethod == comp.method:
                        mlist = map(lambda x: x[0], comp.component.methods())
                        if cmpmethod in mlist:
                            comp.method = cmpmethod
                        else:
                            comp.method = ''
                for f in request.POST:
                    if not f in blacklist:
                        comp.component[f] = int(request.POST[f])
            except:
                print "no", cmpid
        elif 'delete' in request.POST:
            app.removeInstance(cmpid)

    response = HttpResponseRedirect('/')
    response.set_cookie(COOKIE_DESIGN, json.dumps(app.design.json()))
    return response


def addCmp(request):
    ap, _ = load_app(request)
    ap.addInstance(ap.loaded_component[0][0], len(ap.design.cmps), '')
    response = HttpResponseRedirect('/')
    response.set_cookie(COOKIE_DESIGN, json.dumps(ap.design.json()))
    return response


def index(request):
    ap, data = load_app(request)
    print data
    data["form"]=button.UploadFileForm()
    response = render_to_response('mat.html', data)
    response.set_cookie(COOKIE_DESIGN, json.dumps(ap.design.json()))
    return response


def reset(request):
    response = HttpResponseRedirect('/')
    response.set_cookie(COOKIE_DESIGN, '{"cmps":[]}')
    return response
