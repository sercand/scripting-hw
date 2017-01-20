import logging
import json
import random
import string
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from . import design
from . import application
from . import models

logger = logging.getLogger(__name__)

COOKIE_DESIGN = "design"
COOKIE_DESIGNID = "id"


def load_design(request):
    cdesign = request.COOKIES.get(COOKIE_DESIGN)
    cdesignid = request.COOKIES.get(COOKIE_DESIGNID)
    if cdesign is None:
        if not cdesignid is None:
            try:
                d = models.Design.objects.filter(id=cdesignid)[0]
                return json.loads(d.data), cdesignid
            except:
                d = design.Design()
                return d.json(), None
        else:
            d = design.Design()
            return d.json(), None
    return json.loads(cdesign), cdesignid


def load_app(request):
    ap = application.Application()
    for av in ap.avaliable():
        ap.load(av)

    types = []
    loaded = ap.loaded()
    for t in loaded:
        types.append({'value': t, 'name': t.title().replace(
            '_', ' '), 'description': loaded[t]})

    cdesign, cdesignid = load_design(request)
    try:
        ap.loadDesignObj(cdesign)
    except Exception as e:
        logger.error(e)
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
    return ap, cdesignid, {'component_types': types, 'components': cmps}


def updateCmp(request):
    blacklist = ['cmpid', 'cmptype', 'cmpmethod', 'update', 'delete']
    app, did, _ = load_app(request)
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
    if not did is None:
        response.set_cookie(COOKIE_DESIGNID, did)
    return response


def addCmp(request):
    ap, did, _ = load_app(request)
    ap.addInstance(ap.loaded_component[0][0], len(ap.design.cmps), '')
    response = HttpResponseRedirect('/')
    response.set_cookie(COOKIE_DESIGN, json.dumps(ap.design.json()))
    if not did is None:
        response.set_cookie(COOKIE_DESIGNID, did)
    return response


def index(request):
    ap, did, data = load_app(request)
    response = render_to_response('mat.html', data)
    response.set_cookie(COOKIE_DESIGN, json.dumps(ap.design.json()))
    if not did is None:
        response.set_cookie(COOKIE_DESIGNID, did)
    return response


def reset(request):
    response = HttpResponseRedirect('/')
    response.set_cookie(COOKIE_DESIGN, '{"cmps":[]}')
    response.delete_cookie(COOKIE_DESIGNID)
    return response
