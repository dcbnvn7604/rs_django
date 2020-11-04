from django.db import models
from django.contrib.auth.models import User


class EntryQuerySet(models.QuerySet):
    def search(self, criteria):
        return self.filter(models.Q(title__contains=criteria) | models.Q(content__contains=criteria))


class EntryManager(models.Manager):
    def get_queryset(self):
        return EntryQuerySet(self.model, using=self._db)


class Entry(models.Model):
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = EntryManager()
