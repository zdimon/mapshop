# -*- coding: utf-8 -*-
import logging
from optparse import make_option
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from blog.models import BlogCategory


#logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        print 'start'
        #BlogCategory.objects.all().delete()
        l [= 'food','slippers']
        for i in l:
            o = Category()
            o.name = 
            o.save()
            p = Product()
            p.category = o
            p.save() etc

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

        for i,d in insertedPks:
            print i,d
        
        
        

        print 'Done' 
