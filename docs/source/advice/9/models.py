from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from easy_thumbnails.files import get_thumbnailer
from image_cropping import ImageCropField, ImageRatioField
from django.utils.safestring import mark_safe
from main.models import UserProfile
from ckeditor.fields import RichTextField
import pytils

class Course(models.Model):
    name = models.CharField(max_length=250, blank=True, verbose_name=_(u'Name'))
    desc = models.TextField(blank=True, verbose_name=_(u'Description'))
    requirements = models.TextField(blank=True, verbose_name=_(u'Requirements'))
    owner = models.ForeignKey(User, verbose_name=_(u'Owner'))
    image = models.ImageField(blank=True, verbose_name=_(u'Image'), upload_to='course_images', null = True)
    cropping = ImageRatioField('image', '200x200', size_warning=True)
    is_active = models.BooleanField(verbose_name=_('Is main?'), default=False)
    name_slug = models.CharField(verbose_name='Name slug',max_length=250, blank=True)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
       return reverse("course_detail", kwargs={"slug": self.name_slug})
    @property
    def thumb(self):
        try:
            thumbnail_url = get_thumbnailer(self.image).get_thumbnail({
                'size': (100, 100),
                'box': self.cropping,
                'crop': True,
                'detail': True,
            }).url
            return mark_safe(u'<img src="%s" />' % thumbnail_url)
        except:
            return 'no image'
    def save(self, **kwargs):
        if not self.id:
            self.name_slug = pytils.translit.slugify(self.name)
        return super(Course, self).save(**kwargs)


class Lesson(models.Model):
    name = models.CharField(max_length=250, blank=True, verbose_name=_(u'Name'))
    desc = models.TextField(blank=True, verbose_name=_(u'Description'))
    is_active = models.BooleanField(verbose_name=_('Is main?'), default=False)
    is_camera_on = models.BooleanField(verbose_name=_('Is camera on?'), default=False)
    start_at = models.DateTimeField(blank = True, null = True)
    owner = models.ForeignKey(User, verbose_name=_(u'Owner'))
    image = models.ImageField(blank=True, verbose_name=_(u'Image'), upload_to='lessons_images', null = True)
    cropping = ImageRatioField('image', '100x100', size_warning=True)
    course = models.ForeignKey(Course, verbose_name=_(u'Course'), blank=True, null = True)
    is_runing = models.BooleanField(verbose_name=_('Is runing?'), default=False)
    @property
    def thumb(self):
        try:
            thumbnail_url = get_thumbnailer(self.image).get_thumbnail({
                'size': (50, 50),
                'box': self.cropping,
                'crop': True,
                'detail': True,
            }).url
            return mark_safe(u'<img src="%s" />' % thumbnail_url)
        except:
            return 'no image'
    def __unicode__(self):
        return self.name
    def get_absolute_url_for_student(self):
       return reverse("lesson_for_student", kwargs={"id": self.pk})
    def get_absolute_url_for_owner(self):
       return reverse("lesson_for_owner", kwargs={"id": self.pk})
    def clear(self):
        Images.objects.filter(lesson=self).delete()
        ChatMessages.objects.filter(lesson=self).delete()
        Event.objects.filter(lesson=self).delete()
        Users2Lesson.objects.filter(lesson=self).delete()
            

class Topic(models.Model):
    name = models.CharField(max_length=250, blank=True, verbose_name=_(u'Name'))
    lesson = models.ForeignKey(Lesson, verbose_name=_(u'Lesson'))
    def __unicode__(self):
        return self.name

class Event(models.Model):
    TP = (
                ('text_add', _(u'Text adding')),
                ('text_replace', _(u'Text replacing')),
                ('image_file', _(u'Image file')),
                ('image_url', _(u'Image url')),
                ('clear', _(u'Clear')),
          )
    tp = models.CharField(verbose_name=_(u'Type of event'),
                                 choices=TP,
                                 default='text_add',
                                 max_length=15,
                                 db_index=True)
    image_file = models.ImageField(upload_to='event_image', verbose_name=_('Image file'), blank=True)
    image_url = models.CharField(max_length=250, blank=True, verbose_name=_(u'Image url'))
    text = models.TextField(blank=True, verbose_name=_(u'Text'))
    lesson = models.ForeignKey(Lesson, verbose_name=_(u'Topic'))
    created = models.DateTimeField(auto_now_add = True, auto_now = True, blank = True, null = True)
    sorting = models.IntegerField(blank=True, null = True)
    text_size = models.CharField(max_length=50, blank=True, verbose_name=_(u'Text size'))
    text_color = models.CharField(max_length=50, blank=True, verbose_name=_(u'Text color'))
    text_align = models.CharField(max_length=50, blank=True, verbose_name=_(u'Text align'))
    @property
    def li_item(self):
        ret = '''
                <li id="event_%s"> 
                <a data-id="%s" onclick="return false" href="#" class="delete_event"><span class="glyphicon glyphicon-remove"> </span></a> 
                  %s
                <a data-id="%s" onclick="return false" href="#" class="move_event_to_incubator"><span class="glyphicon glyphicon-arrow-right"> </span></a>
                </li>               
                ''' % (self.id, self.id, self.__unicode__(), self.id)
        return mark_safe(ret)
    @property
    def thumb(self):
            return mark_safe(u'<img width="200" src="%s" />' % self.text)
    def __unicode__(self):
        if (self.tp=='image_file'):
            return self.thumb    
        else:
            return self.text
    def save(self, **kwargs):
        if not self.id:
            try:
                self.sorting = Event.objects.all().order_by('-id')[0:1][0].id+1
            except:
                self.sorting = 1
        return super(Event, self).save(**kwargs)

class Images(models.Model):
    image = models.ImageField(blank=True, verbose_name=_(u'Image'), upload_to='course_images')
    cropping = ImageRatioField('image', '100x100', size_warning=True)
    lesson = models.ForeignKey(Lesson)
    created = models.DateTimeField(auto_now_add = True, auto_now = True, blank = True, null = True)
    publish = models.CharField(max_length=5, blank=True, verbose_name=_(u'Auto publish'))
    def __unicode__(self):
        thumbnail_url = get_thumbnailer(self.image).get_thumbnail({
            'size': (50, 50),
            'box': self.cropping,
            'crop': True,
            'detail': True,
        }).url
        return mark_safe(u'<img src="%s" />' % thumbnail_url)
    @property
    def link(self):
        thumbnail_url = get_thumbnailer(self.image).get_thumbnail({
            'size': (50, 50),
            'box': self.cropping,
            'crop': True,
            'detail': True,
        }).url
        return mark_safe(u'<a id="uploaded_image_%s" class="uploaded_image" data-replace="yes" href="#" data-filename="%s"><img src="%s" /></a>' % (self.id, '/media/'+str(self.image), thumbnail_url))


class Users2Lesson(models.Model):
    lesson = models.ForeignKey(Lesson)
    user = models.ForeignKey(UserProfile)

class Users2Course(models.Model):
    course = models.ForeignKey(Course)
    user = models.ForeignKey(UserProfile)


class Subscriber2Lesson(models.Model):
    lesson = models.ForeignKey(Lesson)
    user = models.ForeignKey(UserProfile)

class ChatMessages(models.Model):
    user = models.ForeignKey(UserProfile)
    text = models.TextField(blank=True, verbose_name=_(u'Text'))
    lesson = models.ForeignKey(Lesson, verbose_name=_(u'Lesson'))
    created = models.DateTimeField(auto_now_add = True, auto_now = True, blank = True, null = True)



class Incubator(models.Model):
    TP = (
                ('text_add', _(u'Text adding')),
                ('text_replace', _(u'Text replacing')),
                ('image_file', _(u'Image file')),
                ('image_url', _(u'Image url')),
                ('clear', _(u'Clear')),
          )
    tp = models.CharField(verbose_name=_(u'Type of event'),
                                 choices=TP,
                                 default='text_add',
                                 max_length=15,
                                 db_index=True)
    image_file = models.ImageField(upload_to='event_image', verbose_name=_('Image file'), blank=True)
    image_url = models.CharField(max_length=250, blank=True, verbose_name=_(u'Image url'))
    text = models.TextField(blank=True, verbose_name=_(u'Text'))
    lesson = models.ForeignKey(Lesson, verbose_name=_(u'Topic'))
    created = models.DateTimeField(auto_now_add = True, auto_now = True, blank = True, null = True)
    sorting = models.IntegerField(blank=True, null = True)
    text_size = models.CharField(max_length=50, blank=True, verbose_name=_(u'Text size'))
    text_color = models.CharField(max_length=50, blank=True, verbose_name=_(u'Text color'))
    text_align = models.CharField(max_length=50, blank=True, verbose_name=_(u'Text align'))
    @property
    def li_item(self):
        ret = '''
                <li id="incubator_%s"> 
                <a data-id="%s" onclick="return false" href="#" class="move_incubator_to_event"><span class="glyphicon glyphicon-arrow-left"> </span></a>
                  %s
                <a data-id="%s" onclick="return false" href="#" class="delete_incubator"><span class="glyphicon glyphicon-remove"> </span></a> 
                </li>               
                ''' % (self.id, self.id, self.__unicode__(), self.id)
        return mark_safe(ret)
    @property
    def thumb(self):
            return mark_safe(u'<img width="200" src="%s" />' % self.text)
    def __unicode__(self):
        if (self.tp=='image_file'):
            return self.thumb    
        else:
            return self.text
    def save(self, **kwargs):
        if not self.id:
            try:
                self.sorting = Incubator.objects.all().order_by('-id')[0:1][0].id+1
            except:
                self.sorting = 1
        return super(Incubator, self).save(**kwargs)


