from mongoengine.document import Document
from mongoengine.fields import StringField
from decouple import config

class Product(Document):
    title = StringField(max_length=20, required=True)
    description = StringField(max_length=100, required=True)