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



TORNADO
------------------------------------
#! /usr/bin/env python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import tornado.httpserver
import tornado.ioloop
import tornado.wsgi
import sys
import django.core.handlers.wsgi
#sys.path.append('/home/lawgon/') # path to your project ( if you have it in another dir).


def main():
     # path to your settings module
    application = django.core.handlers.wsgi.WSGIHandler()
    container = tornado.wsgi.WSGIContainer(application)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(8800)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
----------------------------------

DEBUG_TOOLBAR_PATCH_SETTINGS = False 



UNICORN

INSTALLED_APPS += ('gunicorn', )


gunicorn  config.wsgi:application –env DJANGO_SETTINGS_MODULE=config.settings -pid ./pshop.pid

./manage.py run_gunicorn --workers 10 --timeout 300 --bind 127.0.0.1:8080 --pid ./pshop.pid


gunicorn_django -b 127.0.0.1:8000 --settings=config.settings.dev --debug --log


[program:pressa_gunicorn]
command=/home/django/pressa_ve/bin/python /home/django/pressa_ve/pressa/manage.py run_gunicorn --workers 10 --timeout 300 --bind 127.0.0.1:8080 --pid /home/django/pressa_ve/var/run/gunicorn.pid
directory=/home/django/pressa_ve/pressa
environment=PATH="/home/django/pressa_ve/bin"
user=django
autostart=true
autorestart=true






Nginx
server {
    listen 80 ;
    server_name shop.mirbu.com;
    
    client_max_body_size   100m;

        location / {
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_pass http://localhost:8800;
        }

    location /static {
        alias /home/zdimon/pshop_ve/pshop/static;
    }
        
 location /media {
        alias /home/zdimon/pshop_ve/pshop/media;
     }
}





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


