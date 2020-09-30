from django.urls import path

from entry.views import EntryListView, EntryCreateView


app_name = 'entry'


urlpatterns = [
    path('', EntryListView.as_view(), name='list'),
    path('create', EntryCreateView.as_view(), name='create'),
]