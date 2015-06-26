.pypirc
-------------------------
[distutils]
index-servers =
    pypi

[pypi]
username:login
password:password


setup.py
-----------------------------------------------
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(name='django-mapshop',
      version='0.3',
      description='Internet shop with geographic points',
      long_description=readme,
      url='http://github.com/storborg/funniest',
      author='Dmitry Zharikov',
      author_email='zdimon77@gmail.com',
      license='MIT',
      packages=find_packages(exclude=["config"]),
      include_package_data=True,
      zip_safe=False) 


python setup.py register

python setup.py sdist upload

# Pager


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def listing(request):
    contact_list = Contacts.objects.all()
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render_to_response('list.html', {"contacts": contacts})



<div class="pagination">
    <span class="step-links">
        {% if product_list.has_previous %}
            <a href="?page={{ product_list.previous_page_number }}">Назад</a>
        {% endif %}

        <span class="current">
            Page {{ product_list.number }} of {{ product_list.paginator.num_pages }}.
        </span>

        {% if product_list.has_next %}
            <a href="?page={{ product_list.next_page_number }}">Вперед</a>
        {% endif %}
    </span>
</div>






# gen views

Идея проста — есть некоторый часто используемый функционал (например, отображение объекта/списка объектов из БД, передача контекста в шаблон, и т.п.), который используется очень часто. Чтобы не приходилось писать однообразный код, подобные view описаны прямо в коде фреймворка. Для того, чтобы использовать их, нужно сообщить только специфические параметры, вроде типа объекта или имени шаблона, в который передавать контекст.


from django.views.generic import DetailView, ListView
from books.models import Publisher

class PublisherDetailView(DetailView):
    model = Publisher



urlpatterns = patterns('',
    (r'^publishers/$', PublisherDetailView.as_view()),
)

url(r'^$', TestimonialsListView.as_view(template_name='list.html'), name='testimonials_list'),



class RecipesView(ListView):
    queryset = Recipe.objects.all().order_by('-id')
    template_name = 'recipes_list.html'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(RecipesView, self).get_context_data(**kwargs)
        try:
            from mshop.models import SeoPages
            seo =  SeoPages.objects.get(alias='recipes')
            context['seo'] = seo
        except:
            pass
        return context

    def get_queryset(self):
        return QS





class TestimonialsCreateView(CreateView): # форма добавления
    .......

    def post(self, request, *args, **kwargs):
        from django.contrib import messages
        messages.success(request, "Спасибо. Ваше сообщение сохранено и появится после проверки Администрацией.")
        return super(TestimonialsCreateView, self).post(self, request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        kwargs['slides'] = Slider.objects.all()
        return super(IndexView, self).get_context_data(**kwargs)



class LoginView(TemplateView):
    template_name = 'index.html'
    error_messages = {
        'wrong_login': _(
            u'Неверный логин или пароль'),
        'inactive_user': _(
            u'Аккаунт не активирован'),
        'not_customer': _(
            u'У пользователя нет профиля потребителя, '
            u'воспользуйтесь административным интерфесом для входа'),
    }

    def error_response(self, error_message):
        context = self.get_context_data()
        context['error'] = self.error_messages[error_message]
        return super(LoginView, self).render_to_response(context)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username,
                            password=password,
                            user_type='CUSTOMER')

        if not user:
            return self.error_response('wrong_login')

        if not user.is_active:
            return self.error_response('inactive_user')

        try:
            user.partner
            login(request, user)
            return redirect(reverse('partner_admin:index'))
        except ObjectDoesNotExist:
            pass

        try:
            user.customer
        except ObjectDoesNotExist:
            return self.error_response('not_customer')

        login(request, user)
        next_url = (request.GET.get('next', None) or settings.LOGIN_REDIRECT_URL) + '#/'
        return redirect(next_url)


























  {% if  is_paginated %}
    {% if  page_obj.has_previous %}
      <a href="?page={{ page_obj.previous_page_number }}">назад</a> |
    {% endif %}
    страница {{ page_obj.number }} из {{ page_obj.paginator.num_pages }}
    {% if  page_obj.has_next %}|
      <a href="?page={{ page_obj.next_page_number }}">вперед</a>
    {% endif %}
  {% endif %}





#продвинутый пагинатор


{% extends "base.html" %}
{% load simplepaginator %}

 {% block base_content %}

<h2>List</h2>
  <div>

      {% for i in object_list %}

           <div class="col-sm-6" style="height: 190px; border-bottom: 1px dotted #c0c0c0">
              <h3> {{ i.title }}</h3>
              <p> {{ i.content|truncatewords_html:20 }}</p>
              <p><a class="btn btn-default" href="{{ i.get_absolute_url }}" role="button">Подробно &raquo;</a></p>
            </div><!--/span-->


    {% endfor %}

  </div>

     {% if is_paginated %}
       {% simplepaginator %}
    {% endif %}


 {% endblock %}

--------------------------




В любом приложении создаем пакет templatags.
Добавляем файл simplepaginator.py

--------------------------------------
from django import template

register = template.Library()

def simplepaginator(context, adjacent_pages=2):

    page_numbers = [n for n in \
                    range(context["page_obj"].number - adjacent_pages, context["page_obj"].number + adjacent_pages + 1) \
                    if n > 0 and n <= context["paginator"].num_pages]

    return {
        "page_obj": context["page_obj"],
        "paginator" : context["paginator"],
        "page_numbers" : page_numbers
    }

register.inclusion_tag("simplepaginator.html", takes_context=True)(simplepaginator)

-----------------------------



Создаем в каталоге этого приложения внутри каталога templates шаблон simplepaginator.html

    <div class="pagination">
        <span class="step-links">
            {% if page_obj.has_previous %}
                <a href="?page={{ page_obj.previous_page_number }}">previous</a>
            {% endif %}


            {% for num in page_numbers %}
              {% ifequal num page_obj.number %}
                <span class="paginate-current" title="Current Page">{{ page_obj.number }}</span>
              {% else %}
                <span class="paginate-link"><a href="?page={{ num }}" title="Page {{ num }}">{{ num }}</a></span>
              {% endifequal %}
            {% endfor %}



            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">next</a>
            {% endif %}
        </span>
    </div>














