from mongoengine import Document
from mongoengine.fields import(StringField,ListField,ReferenceField, IntField,ListField ,ObjectId)
class User(Document):
    meta = {'collection': 'user'}
    firstName = StringField(required=True)
    lastName = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
class nlpService(Document):
    text = StringField(required=True)
    result = ListField(StringField())

class Article(Document):
    meta = {'collection': 'article'}
    id = ObjectId()
    text = StringField(required=True)
    textstate = IntField()
    username=StringField(required=True)
    comments = ListField(StringField())
    state = ListField(IntField())
