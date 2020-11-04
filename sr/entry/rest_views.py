from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from entry.models import Entry
from entry.serializers import EntrySerializer


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.GET.get('q', ''):
            self.queryset = self.queryset.search(request.GET.get('q'))
        return super().list(request, *args, **kwargs)

    @method_decorator(permission_required('entry.add_entry', raise_exception=True))
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    @method_decorator(permission_required('entry.change_entry', raise_exception=True))
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    @method_decorator(permission_required('entry.delete_entry', raise_exception=True))
    def destroy(self, *args, **kwargs):
        return super().destroy(*args, **kwargs)
