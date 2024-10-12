import pika
from faker import Faker
from models_3 import Contact, connect_to_mongodb


fake = Faker()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')

def create_contacts(n):
    contacts = []
    for _ in range(n):
        contact = Contact(
            fullname=fake.name(), 
            email=fake.email(),
            phone = fake.phone_number(),
            delivery_method = fake.random_element(elements=('email', 'sms'))
            )
        contact.save()
        contacts.append(contact)
        print(f"Created contact {contact.fullname} with id {contact.id}")
        send_to_queue(contact)
    return contacts

def send_to_queue(contact):
    if contact.delivery_method == 'email':
        channel.basic_publish(exchange='', routing_key='email_queue', body=str(contact.id))
        print(f"Sent contact {contact.id} to email queue")
    else:
        channel.basic_publish(exchange='', routing_key='sms_queue', body=str(contact.id))
        print(f"Sent contact {contact.id} to sms queue")

    
connect_to_mongodb()
    
create_contacts(10)  

connection.close()