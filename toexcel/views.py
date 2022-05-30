#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file:views.py
# author: menglong.zhou@qunar.com

from django.shortcuts import render, HttpResponse

def dump(request):
    _admin = request.GET.get('admin')
    _models = request.GET.get('models')
    _app = request.GET.get('app')

    if None in [_admin, _models, _app]:
        return HttpResponse('Missing require parameter')

    admin_user = request.__dict__['user']

    if admin_user.is_anonymous is True:
        return HttpResponse('<h1>403 Forbidden</h1>')

    for per in admin_user.get_all_permissions():
        if _app.lower() in per and _models.lower() in per:
            break
    else:
        return HttpResponse('<h1>403 Forbidden</h1>')

    af = __import__('%s.admin' % _app, fromlist=[_app, 'admin'])      # admin file
    mf = __import__('%s.models' % _app, fromlist=[_app, 'models'])     # models file
    ac = getattr(af, _admin)                # admin class
    mc = getattr(mf, _models)               # models class


    if hasattr(ac, 'toexcel_fields') is False:
        ret = mc.objects.all().values_list()
    else:
        ret = list()
        ac_obj = ac(mc, ac)
        for obj in mc.objects.all():
            _l = list()
            for f in ac.toexcel_fields:
                print('f', f, type(f))
                if hasattr(obj, f):
                    _l.append(getattr(obj, f))
                else:
                    _l.append(getattr(ac_obj, f)(obj))
            ret.append(_l)


    if hasattr(ac, 'toexcel_tags') is False:
        try:
            title = list()
            for i in mc._meta.concrete_fields:
                title.append(i.verbose_name)
        except:
            title = mc.objects.all()[0:1].values()
            title = title[0].keys()
    else:
        title = ac.toexcel_tags

    if hasattr(ac, 'toexcel_choices_fields') is True and hasattr(ac, 'toexcel_choices_dict') is True:
        _ret = list()

        for r in ret:
            r = list(r)
            for i in range(len(ac.toexcel_choices_fields)):
                _fields = ac.toexcel_choices_fields[i]
                _fields_index = ac.toexcel_fields.index(_fields)
                _fields_dict = getattr(mc, ac.toexcel_choices_dict[i])
                r[_fields_index] = _fields_dict[r[_fields_index]][1]

            _ret.append(r)

        ret = _ret

    context = dict()
    context['title'] = title
    context['table'] = ret
    context['name'] = mc._meta.verbose_name_plural

    return render(request, 'toexcel.html', context)
