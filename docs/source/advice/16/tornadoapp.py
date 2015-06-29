# -*- coding: utf-8 -*-
"""
    Simple sockjs-tornado chat application. By default will listen on port 8080.
"""
import tornado.ioloop
import tornado.web
import time
import sockjs.tornado
import brukva
c = brukva.Client()
c.connect()
from chat.models import ChatConnections, ChatRoom, ChatConnection2Room, ChatMessage, ChatInvitations
from users.models import Profile
from django.contrib.auth.models import User
from registration.models import RegistrationProfile
import json
from config.settings import MEDIA_ROOT, PROJECT_PATH
import logging
logger = logging.getLogger(__name__)

class ChatConnection(sockjs.tornado.SockJSConnection):
    """Chat connection implementation"""
    # Class level variable

    chanels = {}
    debug = True
    participants = set()

    def __init__(self,*args):
        super(ChatConnection, self).__init__(*args)
        self.client = brukva.Client()
        self.client.connect()
        self.debug = 'false'


    def on_open(self, info):
        # Send that someone joined
        message = {"act":"someone_joined","content":'Someone joined'}
        self.broadcast(self.participants, json.dumps(message))
        self.participants.add(self)

    def redis_message(self,result):
        message = json.loads(result.body)
        logger.debug('get message from redis')
        self.send(json.dumps(message))

    def subscribe(self,room):
        self.client.subscribe(room)
        self.client.listen(self.redis_message)


    def on_message(self, message):
        logger.debug(message)
        # if subscribing on chanel
        #import pdb; pdb.set_trace()
        message = json.loads(message)
        if message['act']=='open_connect':
            pass


        elif message['act']=='set_current_apponent': # current apponent for clearing page after disconnectiing
            #mes = u'Sorry, but all users are busy now.'
            #c.publish(message['caller_token'],json.dumps({"message": mes,"act":"get_free_user", "status": '1'}))
       

    def on_close(self):
        pass





class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.write("Hello, world")

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # 1. Create chat router
    ChatRouter = sockjs.tornado.SockJSRouter(ChatConnection, '/chatws')
    #ChatRouterws = sockjs.tornado.SockJSRouter(ChatConnection, '/chatws')
    #ChatRouter = sockjs.tornado.So(ChatConnection, '/chatws')

    # 2. Create Tornado application
    app = tornado.web.Application(
            [
             (r"/", IndexHandler),
            ] + ChatRouter.urls +  ChatRouterws.urls
    )

    # 3. Make Tornado app listen on port 55555
    app.listen(55555)

    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
