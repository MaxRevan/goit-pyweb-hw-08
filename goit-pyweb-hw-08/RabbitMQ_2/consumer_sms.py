import pika
from models_3 import Contact, connect_to_mongodb

connect_to_mongodb()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


def send_sms(contact):
    print(f"Sending SMS to {contact.fullname} at {contact.email}...")

def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects.get(id=contact_id)
    
    send_sms(contact)
    
    contact.message_sent = True
    contact.save()
    print(f"SMS sent to {contact.fullname}. Message sent status updated.")

channel.queue_declare(queue='sms_queue')
channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')

channel.start_consuming()