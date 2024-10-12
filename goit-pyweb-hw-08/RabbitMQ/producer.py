import pika
from faker import Faker
from models_2 import Contact, connect_to_mongodb


fake = Faker()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

def create_contacts(n):
    contacts = []
    for _ in range(n):
        contact = Contact(fullname=fake.name(), email=fake.email())
        contact.save()
        contacts.append(contact)
        print(f"Created contact {contact.fullname} with id {contact.id}")
        send_to_queue(contact.id)
    return contacts

def send_to_queue(contact_id):
    channel.basic_publish(
        exchange='',
        routing_key='email_queue',
        body=str(contact_id)
    )
    print(f"Sent contact {contact_id} to the queue")
    
    
connect_to_mongodb()
    
create_contacts(10)  

connection.close()