"""
Django settings for DjangoProject project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from common.config import CONF

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'euf%^4&z)9@6&*i09+$a#r40mcswi58mta5h6yvh^_+ypw4j=*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
APP_NAME = CONF['site_name']

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_ticket.apps.AppWebsiteConfig',
    'import_export',
    'toexcel',
]
IMPORT_EXPORT_USE_TRANSACTIONS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DjangoProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DjangoProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, "media", APP_NAME)
MEDIA_URL = "/media/%s/" % APP_NAME
SIMPLEUI_DEFAULT_THEME = 'orange.css'


if DEBUG is True:
    STATIC_URL = '/static/courier/'
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static', 'courier'),)
else:
    STATIC_URL = '/static/courier/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')


SIMPLEUI_HOME_INFO = False      # 服务器信息
SIMPLEUI_HOME_QUICK = True      # 快速操作
SIMPLEUI_HOME_ACTION = False    # 最近动作
SIMPLEUI_STATIC_OFFLINE = True  # 离线模式
SIMPLEUI_LOADING = False        # 关闭loading遮罩层
SIMPLEUI_LOGIN_PARTICLES = False    # 关闭登录页粒子动画


SIMPLEUI_CONFIG = {
    'system_keep': False,        # 是否保留admin 菜单
    # 'menu_display': ['模板管理', '底部菜单栏管理'],    # 侧边栏显示内容
    'menus': [
        {
            'name': 'OP工单',
            'icon': 'fa fa-map-signs',
            'models': [
                {
                    'name': '工单',
                    'url': ' /courier/admin/app_ticket/ticket',
                    'icon': 'el-icon-tickets'
                },
                {
                    'name': '创建工单模板',
                    'url': ' /courier/admin/app_ticket/tickettype',
                    'icon': 'fa fa-desktop'
                },
                {
                    'name': '统计',
                    'url': '/courier/ticket/summary.html',
                    'icon': 'el-icon-s-data'
                }
            ]
        },
        {
            'name': '认证和授权',
            'icon': 'fa fa-eye',
            'models': [
                {
                    'name': '用户管理',
                    'url': '/courier/admin/auth/user/',
                    'icon': 'fa fa-desktop'
                },
                {
                    'name': '用户组管理',
                    'url': '/courier/admin/auth/group/',
                    'icon': 'fa fa-desktop'
                },
            ]
        },
    ]
}
