import graphene

from entry.schema import Query as EntryQuery, Mutation as EntryMutation


class Query(EntryQuery, graphene.ObjectType):
    pass


class Mutation(EntryMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
