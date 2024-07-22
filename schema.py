import graphene
from models import db, Flower as FlowerModel, Order as OrderModel

class FlowerType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    image_url = graphene.String()
    length = graphene.Float()
    price = graphene.Float()

class OrderType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    address = graphene.String()
    flower_type = graphene.String()
    message = graphene.String()
    user_id = graphene.Int()

class Query(graphene.ObjectType):
    all_flowers = graphene.List(FlowerType)
    all_orders = graphene.List(OrderType)

    def resolve_all_flowers(self, info):
        return FlowerModel.query.all()

    def resolve_all_orders(self, info):
        return OrderModel.query.all()

class CreateFlower(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        image_url = graphene.String(required=True)
        length = graphene.Float(required=True)
        price = graphene.Float(required=True)

    flower = graphene.Field(FlowerType)

    def mutate(self, info, name, image_url, length, price):
        flower = FlowerModel(name=name, image_url=image_url, length=length, price=price)
        db.session.add(flower)
        db.session.commit()
        return CreateFlower(flower=flower)
    
class DeleteFlower(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        flower = FlowerModel.query.get(id)
        if flower:
            db.session.delete(flower)
            db.session.commit()
            return DeleteFlower(success=True)
        return DeleteFlower(success=False)
    
class UpdateFlower(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        length = graphene.Float()
        price = graphene.Float()

    flower = graphene.Field(FlowerType)

    def mutate(self, info, id, name=None, length=None, price=None):
        flower = FlowerModel.query.get(id)
        if not flower:
            return UpdateFlower(flower=None)

        if name is not None:
            flower.name = name
        if length is not None:
            flower.length = length
        if price is not None:
            flower.price = price

        db.session.commit()
        return UpdateFlower(flower=flower)

class Mutation(graphene.ObjectType):
    create_flower = CreateFlower.Field()
    delete_flower = DeleteFlower.Field()
    update_flower = UpdateFlower.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)