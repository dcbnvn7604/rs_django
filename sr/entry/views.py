from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse

from entry.models import Entry
from entry.forms import EntryForm


@method_decorator(login_required, name='dispatch')
class EntryListView(ListView):
    model = Entry
    template_name = 'entry/list.html'


@method_decorator([login_required, permission_required('entry.add_entry')], name='dispatch')
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


@method_decorator([login_required, permission_required('entry.change_entry')], name='dispatch')
class EntryUpdateView(UpdateView):
    form_class = EntryForm
    model = Entry
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('entry:list')


@method_decorator([login_required, permission_required('entry.delete_entry')], name='dispatch')
class EntryDeleteView(DeleteView):
    model = Entry
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('entry:list')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
