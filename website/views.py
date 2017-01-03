import logging
import json
import random
import string
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from . import design
from . import application
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
                atype = 'number'
                inputtype = 'int'
                props = {}
                try:
                    props = a[3]
                    if props is None:
                        props = {}
                except:
                    print ""

                if a[1] == 'str':
                    atype = 'text'
                    inputtype = 'text'
                    if 'enum' in props:
                        inputtype = 'enum'
                elif a[1] == 'float':
                    atype = 'number'
                    inputtype = 'float'
                elif a[1] == 'int':
                    atype = 'number'
                    inputtype = 'int'
                    props['step'] = 1

                att = {
                    'type': atype,
                    'inputtype': inputtype,
                    'name': a[0],
                    'label': a[0].title().replace('_', ' '),
                    'props': props,
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

        if 'delete' in request.POST:
            app.removeInstance(cmpid)
        else:
            try:
                cmptype = request.POST['cmptype']
                comp = app.design.get_entry(cmpid)
                if not cmptype == comp.cmp_name:
                    i = comp.index
                    app.removeInstance(cmpid)
                    print "old index", i
                    ncmpid = app.addInstance(cmptype, i, '')
                    comp = app.design.get_entry(ncmpid)
                    comp.id = cmpid
                if 'cmpmethod' in request.POST:
                    cmpmethod = request.POST['cmpmethod']
                    mlist = map(lambda x: x[0], comp.component.methods())
                    if cmpmethod in mlist:
                        if not cmpmethod == comp.method:
                            comp.method = cmpmethod
                    else:
                        comp.method = ''
                atts = comp.component.attributes()
                for f in request.POST:
                    if f in blacklist:
                        continue
                    for a in atts:
                        if a[0] == f:
                            if a[1] == 'int':
                                comp.component[f] = int(request.POST[f])
                            elif a[1] == 'float':
                                comp.component[f] = float(request.POST[f])
                            else:
                                comp.component[f] = request.POST[f]
                            break
            except:
                print "no", cmpid
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
    response = render_to_response('mat.html', data)
    response.set_cookie(COOKIE_DESIGN, json.dumps(ap.design.json()))
    return response


def reset(request):
    response = HttpResponseRedirect('/')
    response.set_cookie(COOKIE_DESIGN, '{"cmps":[]}')
    return response
