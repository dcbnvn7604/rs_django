from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from entry.models import Entry


@method_decorator(login_required, name='dispatch')
class EntryListView(ListView):
    model = Entry
    template_name = 'entry/list.html'
