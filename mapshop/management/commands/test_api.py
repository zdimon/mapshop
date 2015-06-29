# -*- coding: utf-8 -*-
import logging
from optparse import make_option
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from mapshop.models import Category, Product, ProductImages, Kiosk , Order, Client
from django.core.files import File
from random import randint
import csv
from django.contrib.auth.models import User
from mapshop.management.commands.utils import *
from termcolor import colored
import json
import requests
#logger = logging.getLogger(__name__)


    
    
    

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-a', dest='action',
                    default="edit_product", help="Journal id"),
        
        )

    def handle(self, *args, **options):
        print colored('start test API', 'green', attrs=['reverse', 'blink'])
        action = options["action"]
        if action=='edit_product':
            print colored('REQUEST: edit product', 'green')
            product = Product.objects.get(pk=1)
            if product.ammount==0:
                av = '1'
            else:
                av = '0'
            data = {'product_id': '1', 'ammount': av}
            mess = '****request to change availability of %s to None' % product
            url = 'http://localhost:8008/api/product/edit'
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            responce = requests.post(url, data=json.dumps(data), headers=headers).content
            print colored(responce, 'white')
            print colored('stop test API', 'red', attrs=['reverse', 'blink'])

            data = {'product_id': '1', 'ammount': '2'}
            mess = '****request to to bye '
            url = 'http://localhost:8008/api/product/bye'
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            responce = requests.post(url, data=json.dumps(data), headers=headers).content
            print colored(responce, 'white')
        if action=='create_user':
            data = {'email': 'zdimon77@gmail.com'}
            print colored('REQUEST: user create %s' % data, 'green')
            url = 'http://localhost:8008/api/create/user'
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            responce = requests.post(url, data=json.dumps(data), headers=headers).content
            print colored(responce, 'white')
        if action=='rest_api_create_category':
            data = {'name': 'New category'}
            url = 'http://localhost:8008/restapi/categories'
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            responce = requests.post(url, data=json.dumps(data), headers=headers).content
            print colored(responce, 'white')


       
