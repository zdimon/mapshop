from django.test import TestCase
from django.utils import simplejson
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from random import randint

@csrf_exempt
def create_user(request):
    indata = simplejson.loads(request.body)
#    try:
    user = User.objects.filter(email=indata['email'])
    try:
        u = user[0]
        print 'get user'
        out = {
            'status': 'existed',
            'user_id': u.id
        }
    except IndexError:
        print 'create user'
        password = randint(999,99999)
        user = User.objects.create(username=indata['email'], email=indata['email'], password=password)
        
        out = {
            'status': 'created',
            'user_id': user.id,
            'password': password
        }
    outdata = simplejson.dumps(out)
    return HttpResponse(outdata, mimetype='application/json')
