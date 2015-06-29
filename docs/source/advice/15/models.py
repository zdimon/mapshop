# -*- coding: utf-8 -*-
from celery.worker.strategy import default
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from registration.signals import user_registered
from photos.models import Photos
from django.utils.html import mark_safe
from sorl.thumbnail import get_thumbnail
from datetime import date
from django.utils.translation import ungettext
from django_countries.fields import CountryField
from easy_thumbnails.files import get_thumbnailer
from django.db.models import permalink
from django.core.urlresolvers import reverse
from users.mixins import BodymetrikaMixin, AboutMixin

class UserManager(models.Manager):
    def published(self):
        return super(UserManager, self).get_query_set().filter(pub=True)


class Hobbies(models.Model):
    name = models.CharField(verbose_name=_(u'Hobbies'),max_length=250, blank=False)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = _(u'hobby')
        verbose_name_plural = _(u'Hobbies')
        ordering = ['name']





class Profile(User,BodymetrikaMixin, AboutMixin):
    GENDER = (
                ('male', _('male')),
                ('female',_('female'))
             )

    birthday = models.DateField(verbose_name=_(u'Birthday'), blank=True)
    nickname = models.CharField(verbose_name=_(u'Nickname'),max_length=250, blank=True)
    about_me = models.TextField(verbose_name=_(u'About me'), blank=True)
    gender = models.CharField(verbose_name=_('Gender'),
                                 choices=GENDER,
                                 default='male',
                                 max_length=6)
    country = CountryField(verbose_name=_(u'Country'), blank=True)
    pub = models.BooleanField(verbose_name=_(u'Enabled?'), default=False)
    is_online = models.BooleanField(verbose_name=_(u'Is online?'), default=False)
    hobbies = models.ManyToManyField(Hobbies,verbose_name=_(u'Hobbies'), blank=True)
    sign = models.CharField(verbose_name=_('Sign'),max_length=250, blank=True)
    slug = models.CharField(verbose_name=_('Slug'),max_length=250, blank=True)
    owner = models.ForeignKey('self',blank=True, default=False,  null=True)
    account = models.IntegerField(default=0, verbose_name=_('Account'))
    objects = UserManager()
    @permalink
    def get_absolute_url(self):
       return 'profile_show', (), {'slug': self.slug}

    @property
    def about_me_short(self):
        return ' '.join(self.about_me.split(' ')[0:20])+'...'

    @property
    def online(self):
        if(self.is_online):
            return  mark_safe('<span class="green2 tmiddle"><i class="fa fa-smile-o "></i> online</span>')
        else:
            return  mark_safe('<span class="red tmiddle"><i class="fa fa-frown-o"></i> offline</span>')

    @property
    def call_to_chat_link(self):
        if(self.is_online):
            #return 'dddd'
            return '<a rel='+self.sign+' href="#" >'+_('Call to video chat')+'</a>'

    @property
    def full_name(self):
        return ' '.join([self.first_name,self.last_name])

    @property
    def thumbnailsmall_url(self):
        try:
            p = Photos.objects.filter(user=self, is_main=True).get()
            path = p.thumbnailsmall_url
        except:
            if self.gender == 'male':
                path = '/static/images/no_avatar_man_80.jpg'
            else:
                path = '/static/images/no_avatar_woman_80.jpg'
        return path

    @property
    def thumbnailsmall(self):
            return mark_safe(u'<img class="avatar img-circle img-responsive" src="%s" />' % self.thumbnailsmall_url)

    @property
    def thumbnail(self):
        try:
            p = Photos.objects.filter(user=self, is_main=True).get()
            return p.thumbnail
        except:
            if self.gender == 'male':
                path = '/static/images/no_avatar_man_150.jpg'
            else:
                path = '/static/images/no_avatar_woman_150.jpg'
            return mark_safe(u'<img src="%s" />' % path)

    @property
    def thumbnailbig(self):
        try:
            p = Photos.objects.filter(user=self, is_main=True).get()
            return p.thumbnailbig
        except:
            if self.gender == 'male':
                path = '/static/images/no_avatar_man_300.jpg'
            else:
                path = '/static/images/no_avatar_woman_300.jpg'
            return mark_safe(u'<img src="%s" />' % path)

    @property
    def gender_icon(self):
        if self.gender == 'male':
            return mark_safe(u'<i class="fa fa-male"></i>')
        else:
            return mark_safe(u'<i class="fa fa-female"></i>')

    @property
    def age(self):
        today = date.today()
        if self.birthday:
            try:
                birthday = self.birthday.replace(year=today.year)
            except ValueError: # raised when birth date is February 29 and the current year is not a leap year
                birthday = self.birthday.replace(year=today.year, day=self.birthday.day-1)
            if birthday > today:
                b = today.year - self.birthday.year - 1
            else:
                b = today.year - self.birthday.year
        return '%s %s' % (b ,ungettext(u'y.o.', u'y.o.', b))

    @property
    def zodiac(self):
        zodiacs = [(120, _('Sagittarius')), (218, _('Capricorn')), (320, _('Aquarius')), (420, _('Pisces')), (521, _('Aries')),
           (621, _('Taurus')), (722, _('Gemini')), (823, _('Cancer')), (923, _('Leo')), (1023, _('Virgio')),
           (1122, _('Libra')), (1222, _('Scorpio')), (1231, _('Sagittarius'))]
        date = self.birthday
        date_number = int("".join((str(date.month), '%02d' % date.day)))
        for z in zodiacs:
            if date_number < z[0]:
                return z[1]

    def set_sign(self):
        from time import gmtime, strftime
        t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        import hashlib
        hash_object = hashlib.md5(t)
        self.sign = hash_object.hexdigest()

    def set_slug(self):
        from pytils.translit import translify
        n = ''
        if(self.first_name):
            n = n + translify(self.first_name)
        if(self.last_name):
            n = n +'-'+ translify(self.last_name)
        st = str(self.id)+'-'+n
        self.slug = st
        #import pdb; pdb.set_trace()
        self.save()

#def user_registered_callback(sender, user, request, **kwargs):
    #p = Profile()
    #p.user_ptr = user
    #p.nickname = str(request.POST["nickname"])
    #p.gender = str(request.POST["gender"])
    #p.birthday = str(request.POST["birthday_year"])+'-'+str(request.POST["birthday_month"])+'-'+str(request.POST["birthday_day"])
    #p.save()
    #user.profile.birthday = str(request.POST["birthday_year"])+'-'+str(request.POST["birthday_month"])+'-'+str(request.POST["birthday_day"])
    #user.profile.save()
#user_registered.connect(user_registered_callback)
