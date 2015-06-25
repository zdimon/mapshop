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



  {% if  is_paginated %}
    {% if  page_obj.has_previous %}
      <a href="?page={{ page_obj.previous_page_number }}">назад</a> |
    {% endif %}
    страница {{ page_obj.number }} из {{ page_obj.paginator.num_pages }}
    {% if  page_obj.has_next %}|
      <a href="?page={{ page_obj.next_page_number }}">вперед</a>
    {% endif %}
  {% endif %}







# gen views

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




