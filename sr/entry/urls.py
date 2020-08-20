from django.urls import path

from entry.views import EntryListView


urlpatterns = [
    path('', EntryListView.as_view(), name='list'),
]