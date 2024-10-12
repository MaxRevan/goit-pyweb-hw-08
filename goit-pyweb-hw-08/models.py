from dotenv import load_dotenv
import os
from mongoengine import (
    connect,
    Document,
    StringField,
    ListField,
    ReferenceField
)


load_dotenv()

connect(
    db="max",
    host=f"mongodb+srv://gladkovnissan:{os.getenv('DB_PASSWORD')}@cluster0.v0zgt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
    



class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)
