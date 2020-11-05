import graphene
from graphene_django import DjangoObjectType

from entry.models import Entry
from sr.decorators import graphql_login_required, graphql_permission_required


class EntryType(DjangoObjectType):
    class Meta:
        model = Entry
        fields = ("id", "title", "content")


class Query(graphene.ObjectType):
    entries = graphene.List(EntryType, q=graphene.String())

    @graphql_login_required
    def resolve_entries(root, info, q=None):
        if q:
            return Entry.objects.all().search(q)
        return Entry.objects.all()
