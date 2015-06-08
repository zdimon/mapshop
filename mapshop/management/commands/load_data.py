# -*- coding: utf-8 -*-
import logging
from optparse import make_option
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from mapshop.models import Category, Product, ProductImages, Kiosk 
from django.core.files import File
from random import randint
import csv

#logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        print 'start'
        Kiosk.objects.all().delete()
        ProductImages.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        l = [ 'food','slippers']
        
        for i in l:
            o = Category()
            o.name = i
            o.save()
            cnt = 0
            for n in range(10):
                cnt = cnt  + 1 
                p = Product()
                p.category = o
                p.price = n
                p.rate = randint(0,90)
                p.name = 'Product %s' % n
                p.save()
                for im in range(3):
                    path = 'fixture/test.jpg'
                    #import pdb; pdb.set_trace()
                    name = 'test.jpg' 
                    f = open(path, 'r')
                    file = File(f)
                    im = ProductImages()
                    im.product = p
                    im.image.save(name,file)
                    im.save()
                    print 'process with image %s' % im
                print 'process with %s' % n
	input_file = open("kiosk.csv", "rb")
	rdr = csv.DictReader(input_file, delimiter=';', fieldnames=['mnemonic', 'name', 'address','latitude','longitude'])
	for rec in rdr:
		try:
			k = Kiosk()
                        k.mnemonic = rec['mnemonic']
			k.name = rec['name']
			k.address = rec['address']
			k.latitude = rec['latitude']
			k.longitude = rec['longitude']
	                path = 'media/kiosk.jpg'
			#import pdb; pdb.set_trace()
			name = 'kiosk.jpg'
			print 'Test Hi'
			f = open(path, 'r')
			file = File(f)
			k.foto.save(name,file)
			k.save()
		except:
			print 'Error'
	input_file.close()
        print 'done'

'''
import tempfile
from django.core import files
lf = tempfile.NamedTemporaryFile()
for block in open('path','r'):
    if not block:
        break
    lf.write(block)
j.cover.save(file_name, files.File(lf))

'''

       
