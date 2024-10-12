import pika
from models_3 import Contact, connect_to_mongodb

connect_to_mongodb()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


def send_email(contact):
    print(f"Sending email to {contact.fullname} at {contact.email}...")

def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects.get(id=contact_id)
    
    send_email(contact)
    
    contact.message_sent = True
    contact.save()
    print(f"Email sent to {contact.fullname}. Message sent status updated.")

channel.queue_declare(queue='email_queue')
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')

channel.start_consuming()