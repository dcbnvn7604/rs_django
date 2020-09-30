from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from entry.models import Entry
from entry.forms import EntryForm


@method_decorator(login_required, name='dispatch')
class EntryListView(ListView):
    model = Entry
    template_name = 'entry/list.html'


@method_decorator(login_required, name='dispatch')
class EntryCreateView(CreateView):
    form_class = EntryForm
    model = Entry

    def get_success_url(self):
        return reverse('entry:list')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.set_user(request.user)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
