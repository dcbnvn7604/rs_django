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

    @method_decorator(permission_required('entry.add_entry', raise_exception=True))
    def create(self, *args, **kargs):
        return super().create(*args, **kargs)

    @method_decorator(permission_required('entry.change_entry', raise_exception=True))
    def update(self, *args, **kargs):
        return super().update(*args, **kargs)

    @method_decorator(permission_required('entry.delete_entry', raise_exception=True))
    def destroy(self, *args, **kargs):
        return super().destroy(*args, **kargs)
