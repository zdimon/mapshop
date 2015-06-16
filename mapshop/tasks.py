# -*- coding: utf-8 -*-
from celery import task

@task(name='test_task')
def test_task(product):
    print 'task started! with %s !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!' % product
