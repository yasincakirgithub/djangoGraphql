import graphene
from graphene_django import DjangoObjectType
from game.models import Game
from developer.models import Developer

from graphql_auth.schema import UserQuery
from graphql_auth import mutations
from graphql_jwt.decorators import login_required


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()


class DeveloperType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    class Meta:
        model = Developer
        fields = ("id", "username", "full_name", "age")


# List
class Query(UserQuery,graphene.ObjectType):
    list_developer = graphene.List(DeveloperType)
    read_developer = graphene.Field(DeveloperType, id=graphene.Int())

    def resolve_list_developer(root, info):
        # We can easily optimize query count in the resolve method
        return Developer.objects.all()

    def resolve_read_developer(root, info, id):
        # get data where id in the database = id queried from the frontend
        return Developer.objects.get(id=id)


# Create
class DeveloperCreateMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        full_name = graphene.String()
        age = graphene.Int()

    developer = graphene.Field(DeveloperType)  # define the class we are getting the fields from

    @classmethod
    @login_required
    def mutate(cls, root, info, username, full_name, age):
        developer = Developer(username=username, full_name=full_name, age=age)  # accepts all fields
        developer.save()
        return DeveloperCreateMutation(developer=developer)


# Update
class DeveloperUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        username = graphene.String()
        full_name = graphene.String()
        age = graphene.Int()

    developer = graphene.Field(DeveloperType)

    @classmethod
    @login_required
    def mutate(cls, root, info, username, full_name, age, id):
        developer = Developer.objects.get(id=id)
        developer.username = username
        developer.full_name = full_name
        developer.age = age
        developer.save()
        return DeveloperUpdateMutation(developer=developer)


# Delete
class DeveloperDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        developer = Developer.objects.get(id=id)
        developer.delete()
        return DeveloperDeleteMutation(ok=True)


class Mutation(AuthMutation, graphene.ObjectType):
    create_developer = DeveloperCreateMutation.Field()
    update_developer = DeveloperUpdateMutation.Field()
    delete_developer = DeveloperDeleteMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
