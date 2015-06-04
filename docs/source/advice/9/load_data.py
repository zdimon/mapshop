# -*- coding: utf-8 -*-
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from mixer.backend.django import mixer
from users.models import Profile
from photos.models import Photos
from config.settings import FIXTURE_DIRS
from django.core.files import File
from django.contrib.flatpages.models import FlatPage
from flatblocks.models import FlatBlock
from django.contrib.sites.models import Site
from django.db import connection
from django.contrib.auth.models import Group, Permission
from slider.models import Slider


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        cursor = connection.cursor()
        from users.models import Profile
        print 'start'
        # create group for partner
        cursor.execute("TRUNCATE TABLE auth_group_permissions CASCADE;")
        cursor.execute("TRUNCATE TABLE auth_group CASCADE;")
        cursor.execute("ALTER SEQUENCE auth_group_permissions_id_seq RESTART;")
        cursor.execute("ALTER SEQUENCE auth_permission_id_seq RESTART;")
        #import pdb; pdb.set_trace()
        d = Group()
        d.name = 'Partner'
        d.save()
        add_user = Permission.objects.get(codename='add_profile')
        change_user = Permission.objects.get(codename='change_profile')
        create_user = Permission.objects.get(codename='delete_profile')
        d.permissions.add(add_user)
        d.permissions.add(change_user)
        d.permissions.add(create_user)
        add_photos = Permission.objects.get(codename='add_photos')
        change_photos = Permission.objects.get(codename='change_photos')
        create_photos = Permission.objects.get(codename='delete_photos')
        d.permissions.add(add_photos)
        d.permissions.add(change_photos)
        d.permissions.add(create_photos)
        Profile.objects.all().delete()
        Photos.objects.all().delete()
        cursor.execute("ALTER SEQUENCE auth_user_id_seq RESTART;")
        cursor.execute("TRUNCATE TABLE auth_user CASCADE;")

        print 'add agency'
        ag = Profile()
        ag.gender = 'male'
        ag.username = 'agency'
        ag.set_password('1q2w3e')
        ag.is_staff = True
        ag.is_superuser = False
        ag.birthday = '2000-01-01'
        ag.save()
        d.user_set.add(ag)

        a = Profile()
        a.username = 'anonimouse'
        a.set_password('1q2w3e')
        a.first_name = 'anonimouse'
        a.last_name = ''
        a.is_staff = True
        a.is_superuser = True
        a.birthday = '2000-01-01'
        a.gender = 'male'
        #a.partner = a
        a.save()

        print 'add admin'
        p = Profile()
        p.username = 'admin'
        p.set_password('1q2w3e')
        p.birthday = '2000-01-01'
        p.gender = 'male'
        p.is_staff = True
        p.is_superuser = True
        p.save()


        #d.user_set.add(ag)

        print 'deleting'
        for i in range(1,11):
            user = mixer.blend(Profile, gender='female', password='111', owner=a)
            #import pdb; pdb.set_trace()
            user.set_password('111')
            if i == 1:
                user.username = 'olga'
                user.first_name = 'olga'
                user.owner = ag
            if i == 2:
                user.username = 'lena'
                user.first_name = 'lena'
                user.owner = ag
            if i == 3:
                user.username = 'sveta'
                user.first_name = 'sveta'
                user.owner = ag
            user.pub = True
            user.save()
            user.set_slug()
            for pi in range(1,4):
                path = FIXTURE_DIRS[0]+'/images/w%(var1)s_%(var2)s.jpg' % {'var1':str(i), 'var2':str(pi)}
                #import pdb; pdb.set_trace()
                name = 'w%(var1)s_%(var2)s.jpg' % {'var1':str(i), 'var2':str(pi)}
                f = open(path, 'r')
                file = File(f)
                im = Photos()
                im.user = user
                if pi==1:
                    im.is_main = True
                else:
                    im.is_main = False
                im.image.save(name,file)
                im.pub = True
                im.save()
            print 'created %s' % user.full_name

        for i in range(1,9):
            user = mixer.blend(Profile, gender='male', password='111', owner=a)
            #import pdb; pdb.set_trace()
            user.set_password('111')
            if i == 1:
                user.username = 'oleg'
                user.first_name = 'oleg'
                user.owner = ag
            user.pub = True
            user.save()
            user.set_slug()
            path = FIXTURE_DIRS[0]+'/images/m%(var1)s.jpg' % {'var1':str(i)}
            #import pdb; pdb.set_trace()
            name = 'm%(var1)s.jpg' % {'var1':str(i)}
            f = open(path, 'r')
            file = File(f)
            im = Photos()
            im.user = user
            im.is_main = True
            im.image.save(name,file)
            im.pub = True
            im.save()
            print 'created %s' % str(i)
        print 'load site'
        Site.objects.all().delete()
        cursor.execute("ALTER SEQUENCE django_site_id_seq RESTART;")
        s = Site()
        s.name = 'mirbu.com'
        s.save()

        print 'load flatpages...'
        FlatPage.objects.all().delete()
        s = Site.objects.get(pk=1)

        p = FlatPage()
        p.url = '/home/'
        p.title = 'home'
        p.title_en = 'Home'
        p.title_ru = 'Домашняя страница'
        p.content = 'home home'
        p.content_ru = u'главная страница'
        p.content_en = u'home page'
        p.template_name = 'main/pages.html'
        p.save()
        p.sites.add(s)


        p = FlatPage()
        p.url = '/about/'
        p.title = 'About us'
        p.title_en = 'About us'
        p.title_ru = 'О нас'
        p.content = 'home home'
        p.content_ru = 'содержимое сожержимое содержимое сожержимое содержимое сожержимое содержимое сожержимое содержимое сожержимое содержимое сожержимое '
        p.content_en = 'content content content content content content content content content content content content content content content content content '
        p.template_name = 'main/pages.html'
        p.save()
        p.sites.add(s)


        p = FlatPage()
        p.url = '/terms/'
        p.title = 'Terms'
        p.title_en = 'terms'
        p.title_ru = 'Правила'
        p.content = 'home home'
        p.content_ru = 'содержимое сожержимое содержимое сожержимое содержимое сожержимое содержимое сожержимое содержимое сожержимое содержимое сожержимое '
        p.content_en = 'content content content content content content content content content content content content content content content content content '
        p.template_name = 'main/pages.html'
        p.save()
        p.sites.add(s)
        #logger.error("Start process")
        #import time
        #for p in Profile.objects.all():
        #    p.set_sign()
        #    p.save()
        #    print u'make - '+p.sign
        #    time.sleep(2)
        #logger.error("Stop process")

        FlatBlock.objects.all().delete()
        fb = FlatBlock()
        fb.header = 'Our Contacts'
        fb.slug = 'contact.info'
        fb.content = '<address> <strong>Loop, Inc.</strong><br> 795 Park Ave, Suite 120 <br>San Francisco, CA 94107 <br><abbr title="Phone">P:</abbr>(234) 145-1810</address>'
        fb.save()

        fb = FlatBlock()
        fb.slug = 'contact.text'
        fb.header = 'Contact Form'
        fb.content = 'Contact information information information information information information information information information '
        fb.save()

        print 'load slider'
        Slider.objects.all().delete()
        s = Slider()
        path = FIXTURE_DIRS[0]+'/images/1.png'
        name = 'slider1.jpg'
        f = open(path, 'r')
        file = File(f)
        s.image.save(name,file)
        s.pub = True
        s.title = 'New brend site'
        s.description = 'description description description description '
        s.save()

        s = Slider()
        path = FIXTURE_DIRS[0]+'/images/2.png'
        name = 'slider2.jpg'
        f = open(path, 'r')
        file = File(f)
        s.pub = True
        s.image.save(name,file)
        s.title = 'New brend site'
        s.description = 'description description description description '
        s.save()

        s = Slider()
        path = FIXTURE_DIRS[0]+'/images/3.png'
        name = 'slider3.jpg'
        f = open(path, 'r')
        file = File(f)
        s.pub = True
        s.image.save(name,file)
        s.title = 'New brend site'
        s.description = 'description description description description '
        s.save()

        print 'load news'
        from news.models import News
        News.objects.all().delete()
        n = News()
        path = FIXTURE_DIRS[0]+'/images/w4_1.jpg'
        name = 'w4_1.jpg'
        f = open(path, 'r')
        file = File(f)
        n.title = 'News 1'
        n.content = 'Lorem ipsum dolor sit amet, dolore eiusmod quis tempor incididunt ut et dolore Ut veniam unde nostrudlaboris. Sed unde omnis iste natus error sit voluptatem.'
        n.image.save(name,file)
        n.save()

        n = News()
        path = FIXTURE_DIRS[0]+'/images/w4_2.jpg'
        name = 'w4_2.jpg'
        f = open(path, 'r')
        file = File(f)
        n.title = 'News 2'
        n.content = 'Lorem ipsum dolor sit amet, dolore eiusmod quis tempor incididunt ut et dolore Ut veniam unde nostrudlaboris. Sed unde omnis iste natus error sit voluptatem.'
        n.image.save(name,file)
        n.save()

        n = News()
        path = FIXTURE_DIRS[0]+'/images/w4_3.jpg'
        name = 'w4_3.jpg'
        f = open(path, 'r')
        file = File(f)
        n.title = 'News 3'
        n.content = 'Lorem ipsum dolor sit amet, dolore eiusmod quis tempor incididunt ut et dolore Ut veniam unde nostrudlaboris. Sed unde omnis iste natus error sit voluptatem.'
        n.image.save(name,file)
        n.save()

        print "add services"
        from account.models import Services
        Services.objects.all().delete()

        s = Services()
        s.name = 'Send message'
        s.name_ru = 'Послать сообщение'
        s.alias = 'send_message'
        s.price = 1
        s.save()

        s = Services()
        s.name = 'Read message'
        s.name_ru = 'Прочитать сообщение'
        s.alias = 'read_message'
        s.price = 2
        s.save()

        s = Services()
        s.name = '1 min of chating'
        s.name_ru = '1 минута чата'
        s.alias = 'chat'
        s.price = 1
        s.save()
