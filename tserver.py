import os
import tornado.httpserver
import tornado.ioloop
import tornado.wsgi
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
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

