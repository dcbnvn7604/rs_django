from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.apps import apps


def create_group_editor(sender, verbosity=2, **kargs):
    if sender.name != 'entry':
        return
    if verbosity >= 2:
        print('Create group "editor"')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    editor_group = Group.objects.create(name='editor')
    permision = Permission.objects.get(codename="add_entry")
    editor_group.permissions.add(permision)
    permision = Permission.objects.get(codename="change_entry")
    editor_group.permissions.add(permision)
    permision = Permission.objects.get(codename="delete_entry")
    editor_group.permissions.add(permision)


class EntryConfig(AppConfig):
    name = 'entry'

    def ready(self):
        post_migrate.connect(create_group_editor)
