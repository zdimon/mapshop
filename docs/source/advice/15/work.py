CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
            '172.19.26.240:11211',
            '172.19.26.242:11211',
        ]
    }
}





CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}

python manage.py createcachetable




CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}



from django.views.decorators.cache import cache_page

@cache_page(60 * 15)
def my_view(request):

By default, the default cache will be used, but you can specify any cache you want
@cache_page(60 * 15, cache="special_cache")
def my_view(request):


Specifying per-view cache in the URLconf¶



from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^foo/([0-9]{1,2})/$', cache_page(60 * 15)(my_view)),
]



Template fragment caching


{% load cache %}
{% cache 500 sidebar %}
    .. sidebar ..
{% endcache %}

Sometimes you might want to cache multiple copies of a fragment depending on some dynamic data that appears inside the fragment. For example, you might want a separate cached copy of the sidebar used in the previous example for every user of your site.

{% load cache %}
{% cache 500 sidebar request.user.username %}
    .. sidebar for logged in user ..
{% endcache %}



The low-level cache API
from django.core.cache import cache

cache.set('my_key', 'hello, world!', 30)
cache.get('my_key')


>>> cache.set('add_key', 'Initial value')
>>> cache.add('add_key', 'New value')
>>> cache.get('add_key')
'Initial value'


>>> cache.set('a', 1)
>>> cache.set('b', 2)
>>> cache.set('c', 3)
>>> cache.get_many(['a', 'b', 'c'])
{'a': 1, 'b': 2, 'c': 3}


>>> cache.set_many({'a': 1, 'b': 2, 'c': 3})
>>> cache.get_many(['a', 'b', 'c'])


cache.delete('a')


LANGUAGES = (
    ('hy', _('Armenian')),
    ('ru', _('Russian')),
    ('en', _('English')),
)


{% load i18n %}
{% get_current_language as LANGUAGE_CODE %}  

                    {% if LANGUAGE_CODE == 'ru' %}
                        <li>
                            <a href="{% url 'main.views.change_language' %}?language=hy&next={{request.get_full_path}}">
                               <img src="{% static "ar.png" %}" title="{% trans 'Armenian' %}" />
                            </a>
                         </li><li>
                            <a href="{% url 'main.views.change_language' %}?language=en&next={{request.get_full_path}}">
                               <img src="{% static "uk.png" %}" title="{% trans 'English' %}" />
                            </a>                           
                        </li>
                    {% endif %}
                    {% if LANGUAGE_CODE == 'hy' %}
                      <li>
                            <a href="{% url 'main.views.change_language' %}?language=ru&next={{request.get_full_path}}">
                               <img src="{% static "ru.png" %}" title="{% trans 'Russian' %}" />
                            </a>
                       </li><li>
                            <a href="{% url 'main.views.change_language' %}?language=en&next={{request.get_full_path}}">
                               <img src="{% static "uk.png" %}" title="{% trans 'English' %}" />
                            </a>
                      </li>
                    {% endif %}
                    {% if LANGUAGE_CODE == 'en' %}
                        <li>
                           <a href="{% url 'main.views.change_language' %}?language=ru&next={{request.get_full_path}}">
                               <img src="{% static "ru.png" %}" title="{% trans 'Russian' %}" />
                           </a>
                        </li><li>
                            <a href="{% url 'main.views.change_language' %}?language=hy&next={{request.get_full_path}}">
                               <img src="{% static "ar.png" %}" title="{% trans 'Armenian' %}" />
                            </a>
                       </li>
                    {% endif %}    


from django.utils.translation import check_for_language
from django.conf import settings

def change_language(request):
    _next = request.REQUEST.get('next', None)
    if not _next:
        _next = request.META.get('HTTP_REFERER', None)

    if not _next:
        _next = '/'

    # если уже есть языковой префикс URL, надо убрать его
    #settings.LANGUAGES = settings.LANGUAGES 
    for supported_language in settings.LANGUAGES:
        prefix = '/%s/' % supported_language[0]
        if _next.startswith(prefix):
            _next = _next[len(prefix):]
            break

    language = request.REQUEST.get(u'language', None)
    #if language and check_for_language(language):
    if _next == '/':
        response = HttpResponseRedirect('/')
    else:
        response = HttpResponseRedirect('/%s/%s' % (language, _next))

    if hasattr(request, 'session'):
        request.session['django_language'] = language
    else:
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)

    translation.activate(language)
    return response


























