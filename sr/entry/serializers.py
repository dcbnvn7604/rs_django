from rest_framework import serializers

from entry.models import Entry


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['title', 'content']
