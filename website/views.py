import logging
import json
import random
import string
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect
from . import design
from . import application
from . import models

logger = logging.getLogger(__name__)

COOKIE_DESIGNID = "id"

def load_design(id):
    try:
        d = models.Design.objects.filter(id=id)[0]
        return json.loads(d.data)
    except:
        d = design.Design()
        return d.json()


def load_app_for_id(theid):
    ap = application.Application()
    for av in ap.avaliable():
        ap.load(av)

    types = []
    loaded = ap.loaded()
    for t in loaded:
        types.append({'value': t, 'name': t.title().replace(
            '_', ' '), 'description': loaded[t]})

    cdesign = load_design(theid)
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
    return ap, {'component_types': types, 'components': cmps, 'design': json.dumps(cdesign),'designid': theid}


def load_app(request):
    cdesignid = request.COOKIES.get(COOKIE_DESIGNID)
    return load_app_for_id(cdesignid)


def index(request):
    designid = request.COOKIES.get(COOKIE_DESIGNID)
    if designid is None:
        designid = design.id_generator(10)
        d = design.Design()
        jd = json.dumps(d.json())
        models.Design.objects.create(id=designid, data=jd)

    return redirect('/edit/' + designid)


def edit(request, theid):
    _, data = load_app_for_id(theid)
    response = render_to_response('mat.html', data)
    response.set_cookie(COOKIE_DESIGNID, theid)
    return response
