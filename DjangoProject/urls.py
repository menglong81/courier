"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
from DjangoProject import settings
from django.views import static
import toexcel.urls
import app_ticket.urls
from common.config import CONF
from django.shortcuts import redirect

APP_NAME = CONF['site_name']

urlpatterns = [
    url(r'^%s/admin/' % APP_NAME, admin.site.urls),
    url(r'^%s/toexcel/' % APP_NAME, include(toexcel.urls)),
    url(r'^%s/ticket/' % APP_NAME, include(app_ticket.urls)),
    url(r'^$', lambda x: redirect('/dictionary/website/index.html')),

    url(r'^media/%s/(?P<path>.*)$' % APP_NAME, static.serve, {'document_root': settings.MEDIA_ROOT}, name='media')
]

if settings.DEBUG is False:
    urlpatterns.append(url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'))