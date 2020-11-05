import graphene

from entry.schema import Query as EntryQuery


class Query(EntryQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
