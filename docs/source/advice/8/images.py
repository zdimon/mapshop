sorl-thumbnail==11.12
django-image-cropping==1.0.0
easy-thumbnails==2.1


from image_cropping import ImageCropField, ImageRatioField
from easy_thumbnails.files import get_thumbnailer


cropping = ImageRatioField('image', '200x200', size_warning=True)
image = models.ImageField(blank=True, verbose_name=_(u'Image'), upload_to='course_images', null = True)


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


from image_cropping import ImageCroppingMixin


class NewsImagesInline(ImageCroppingMixin,admin.TabularInline):
    model = Images
    verbose_name_plural = u'Изображения'


    inlines = [
        NewsImagesInline,
    ]
