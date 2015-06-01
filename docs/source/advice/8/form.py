from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)



from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import NameForm

def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        #form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            o = form.save()
            return HttpResponseRedirect('/thanks/')
    else:
        form = NameForm()
    return render(request, 'name.html', {'form': form})



<form action="/your-name/" method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Submit" />
</form>



subject = form.cleaned_data['subject']



There are other output options though for the <label>/<input> pairs:

{{ form.as_table }} will render them as table cells wrapped in <tr> tags
{{ form.as_p }} will render them wrapped in <p> tags
{{ form.as_ul }} will render them wrapped in <li> tags


<div class="fieldWrapper">
    {{ form.subject.errors }}
    {{ form.subject.label_tag }}
    {{ form.subject }}
</div>


{% if form.subject.errors %}
    <ol>
    {% for error in form.subject.errors %}
        <li><strong>{{ error|escape }}</strong></li>
    {% endfor %}
    </ol>
{% endif %}



{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
    </div>
{% endfor %}


{% include "form_snippet.html" with form=comment_form %}


{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
    </div>
{% endfor %}




from django.forms import ModelForm
from myapp.models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['pub_date', 'headline', 'content', 'reporter']
        exclude = ('body',)





article = Article.objects.get(pk=1)
form = ArticleForm(instance=article)








