# -*- coding: utf-8 -*-
from django.conf import settings
import re

class TemplateInjector(object):
    
    def process_request(self, request):
        request.supervar = 'my super var'
        return None


    def process_response(self, request, response):
        #return if admin
        if request.get_full_path().startswith('/admin'):
            return response
        #response.content = 'blabla'
        return response

