from django.contrib import admin

from entry.models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    save_as = True
