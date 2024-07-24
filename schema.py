import graphene  # Импорт библиотеки graphene для работы с GraphQL
from models import db, Flower as FlowerModel, Order as OrderModel  # Импорт моделей и базы данных из models

# Определение GraphQL типа для модели Flower
class FlowerType(graphene.ObjectType):
    id = graphene.Int()  # Идентификатор цветка
    name = graphene.String()  # Название цветка
    image_url = graphene.String()  # URL изображения цветка
    length = graphene.Float()  # Длина цветка
    price = graphene.Float()  # Цена цветка

# Определение GraphQL типа для модели Order
class OrderType(graphene.ObjectType):
    id = graphene.Int()  # Идентификатор заказа
    name = graphene.String()  # Имя получателя
    address = graphene.String()  # Адрес доставки
    flower_type = graphene.String()  # Тип цветов в заказе
    message = graphene.String()  # Сообщение к заказу
    user_id = graphene.Int()  # Идентификатор пользователя

# Определение запросов GraphQL
class Query(graphene.ObjectType):
    all_flowers = graphene.List(FlowerType)  # Запрос всех цветов
    all_orders = graphene.List(OrderType)  # Запрос всех заказов

    # Метод для разрешения запроса all_flowers
    def resolve_all_flowers(self, info):
        return FlowerModel.query.all()

    # Метод для разрешения запроса all_orders
    def resolve_all_orders(self, info):
        return OrderModel.query.all()

# Определение мутации для создания цветка
class CreateFlower(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)  # Аргумент: название цветка
        image_url = graphene.String(required=True)  # Аргумент: URL изображения
        length = graphene.Float(required=True)  # Аргумент: длина цветка
        price = graphene.Float(required=True)  # Аргумент: цена цветка

    flower = graphene.Field(FlowerType)  # Поле возвращаемого типа

    # Метод для создания цветка
    def mutate(self, info, name, image_url, length, price):
        flower = FlowerModel(name=name, image_url=image_url, length=length, price=price)
        db.session.add(flower)
        db.session.commit()
        return CreateFlower(flower=flower)

# Определение мутации для удаления цветка
class DeleteFlower(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)  # Аргумент: идентификатор цветка

    success = graphene.Boolean()  # Поле, указывающее на успешность операции

    # Метод для удаления цветка
    def mutate(self, info, id):
        flower = FlowerModel.query.get(id)
        if flower:
            db.session.delete(flower)
            db.session.commit()
            return DeleteFlower(success=True)
        return DeleteFlower(success=False)

# Определение мутации для обновления цветка
class UpdateFlower(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)  # Аргумент: идентификатор цветка
        name = graphene.String()  # Аргумент: название цветка
        length = graphene.Float()  # Аргумент: длина цветка
        price = graphene.Float()  # Аргумент: цена цветка

    flower = graphene.Field(FlowerType)  # Поле возвращаемого типа

    # Метод для обновления цветка
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

# Определение корневой мутации
class Mutation(graphene.ObjectType):
    create_flower = CreateFlower.Field()  # Мутация для создания цветка
    delete_flower = DeleteFlower.Field()  # Мутация для удаления цветка
    update_flower = UpdateFlower.Field()  # Мутация для обновления цветка

# Создание схемы GraphQL
schema = graphene.Schema(query=Query, mutation=Mutation)