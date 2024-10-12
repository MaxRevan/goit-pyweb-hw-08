import mongoengine as me
from dotenv import load_dotenv
import os

dotenv_path = '../.env'
load_dotenv(dotenv_path)

def connect_to_mongodb():
    me.connect(
        db="max3", 
        host=f"mongodb+srv://gladkovnissan:{os.getenv('DB_PASSWORD')}@cluster0.v0zgt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )

class Contact(me.Document):
    fullname = me.StringField(required=True)
    email = me.EmailField(required=True)
    phone = me.StringField()
    delivery_method = me.StringField(choices=['email', 'sms'], required=True)
    sent = me.BooleanField(default=False)

    def __str__(self):
        return f"{self.fullname} <{self.email}>"
