import graphene
from graphene_django import DjangoObjectType  # used to change Django object into a format that is readable by GraphQL
from game.models import Game
from developer.models import Developer


class DeveloperType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    class Meta:
        model = Developer
        fields = ("id", "username", "full_name", "age")


# Retrieveal işlemler

class Query(graphene.ObjectType):
    list_developer = graphene.List(DeveloperType)
    read_developer = graphene.Field(DeveloperType, id=graphene.Int())

    def resolve_list_developer(root, info):
        # We can easily optimize query count in the resolve method
        return Developer.objects.all()

    def resolve_read_developer(root, info, id):
        # get data where id in the database = id queried from the frontend
        return Developer.objects.get(id=id)


# Create işlemleri
class DeveloperMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        full_name = graphene.String()
        age = graphene.Int()

    developer = graphene.Field(DeveloperType)  # define the class we are getting the fields from

    @classmethod
    def mutate(cls, root, info, username, full_name, age):
        # function that will save the data
        developer = Developer(username=username, full_name=full_name, age=age)  # accepts all fields
        developer.save()
        return DeveloperMutation(developer=developer)


class Mutation(graphene.ObjectType):
    # keywords that will be used to do the mutation in the frontend
    create_developer = DeveloperMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
