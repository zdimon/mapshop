db_index=True




sudo apt-get install uwsgi nginx uwsgi-plugin-python
sudo ln -s $1/setup/nginx/mshop.conf /etc/nginx/sites-enabled/
sudo ln -s $1/config/uwsgi/mshop.ini /etc/uwsgi/apps-enabled/
sudo service nginx restart
sudo service uwsgi restart




server {
    listen      80;
    server_name usadbacms.local;
    access_log  /var/log/nginx/usadbacms.log;
    location / {
           uwsgi_pass      unix:///tmp/usadbacms.sock;
            include         uwsgi_params;
            client_max_body_size 200M;
    }
    location /static {
        alias /home/zarik/web/django_projects/cms_ve/cms_usadba/static/;
    }
}

[uwsgi]
thread=3
master          = true
processes       = 2
module = cms_usadba.wsgi
chdir = /home/zarik/web/django_projects/cms_ve/cms_usadba
socket          = /tmp/usadbacms.sock
logto = /var/log/uwsgi/usadbacms.log
vacuum          = true
max-requests = 5000
buffer-size=32768
chmod-socket = 777
plugins=python
home            = /home/zarik/web/django_projects/cms_ve




#! /usr/bin/env python
import os
import tornado.httpserver
import tornado.ioloop
import tornado.wsgi
import sys
import django.core.handlers.wsgi
from config.settings import BASE_DIR
sys.path.append(BASE_DIR)
def main():
        os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
        application = django.core.handlers.wsgi.WSGIHandler()
        container = tornado.wsgi.WSGIContainer(application)
        http_server = tornado.httpserver.HTTPServer(container)
        http_server.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
                main()




pip install supervisor


[program:courses_celeryd]
command=/home/zdimon/co_ve/co/manage.py celeryd
directory=/home/zdimon/co_ve/co
environment=PATH="/home/zdimon/co_ve/bin"
user=zdimon
autostart=true
autorestart=true


[program:courses_webserver]
command=/home/zdimon/co_ve/co/manage.py runserver 0.0.0.0:8888
directory=/home/zdimon/co_ve/co
environment=PATH="/home/zdimon/co_ve/bin"
user=zdimon
autostart=true
autorestart=true





Перевод базы
Установка пакета
pip install django-modeltranslation

Добавляем пакет в INSTALLED_APPS

Создаем файл translation.py

--------------------

from modeltranslation.translator import translator, TranslationOptions
from news.models import News

class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'desc', 'content')

translator.register(News, NewsTranslationOptions)

------------------

Наследуем админку
from modeltranslation.admin import TranslationAdmin

class NewsAdmin(TranslationAdmin):
    ......
    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }





http://habrahabr.ru/post/74165/

https://realpython.com/blog/python/adding-social-authentication-to-django/


