import datetime
from enum import Enum

from mongoengine import Document, StringField, DateTimeField, IntField, EmbeddedDocument, ListField, \
    EmbeddedDocumentField, ReferenceField, Decimal128Field, EmbeddedDocumentListField, EnumField


class User(Document):
    username = StringField()
    email = StringField()
    password = StringField()
    role = StringField(default='user')
    createdAt = DateTimeField(default=datetime.datetime.now)
    updatedAt = DateTimeField(default=datetime.datetime.now)

class Brand(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(required=False)
    createdAt  = DateTimeField(default=datetime.datetime.now)
    updatedAt = DateTimeField(default=datetime.datetime.now)

class Category(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(required=False)
    createdAt  = DateTimeField(default=datetime.datetime.now)
    updatedAt = DateTimeField(default=datetime.datetime.now)

    meta = {
        'collection': 'category',
    }

class Slider(Document):
    title = StringField(max_length=100, required=True)
    description = StringField(required=False)
    link = StringField(required=True)
    img = StringField(required=False)
    order = IntField()
    status = IntField()
    createdAt = DateTimeField(default=datetime.datetime.now)
    updatedAt = DateTimeField(default=datetime.datetime.now)

class ProductImage(EmbeddedDocument):
    path = StringField(required=True)
    is_thumbnail = IntField(default=0)

class Product(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(required=False)
    price = Decimal128Field(required=True)
    quantity = IntField(default=1)
    brand = ReferenceField(Brand, required=True)
    category = ReferenceField(Category, required=True)
    images = ListField(EmbeddedDocumentField(ProductImage))
    status = IntField(default=1)
    createdAt = DateTimeField(default=datetime.datetime.now)
    updatedAt = DateTimeField(default=datetime.datetime.now)

class Cart(Document):
    user = ReferenceField(User)
    product = ReferenceField(Product)
    quantity = IntField(default=1)
    price = Decimal128Field(required=True)
    createdAt = DateTimeField(default=datetime.datetime.now)
    updatedAt = DateTimeField(default=datetime.datetime.now)

class OrderInfo(EmbeddedDocument):
    first_name = StringField(max_length=100, required=True)
    last_name = StringField(max_length=100, required=True)
    email = StringField(required=True)
    phone = StringField(required=True)
    address = StringField(required=True)
    additional_address = StringField(required=False)
    shipping_notes = StringField(required=False,max_length=500)

class OrderProductList(EmbeddedDocument):
    product = ReferenceField(Product)
    price = Decimal128Field(required=True)
    quantity = IntField(default=1)

class OrderStatus(Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    DELIVERED = "delivered"

class Order(Document):
    user = ReferenceField(User)
    product_list = EmbeddedDocumentListField(OrderProductList,required=True)
    info = EmbeddedDocumentField(OrderInfo, required=True)
    status = EnumField(OrderStatus, default=OrderStatus.PENDING)
    createdAt = DateTimeField(default=datetime.datetime.now)
    updatedAt = DateTimeField(default=datetime.datetime.now)