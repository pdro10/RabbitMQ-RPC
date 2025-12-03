import pika
import json

def createConnectionAndChannel(host='localhost'):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    
    channel = connection.channel()

    return connection, channel

def sendReply(ch, props, result):
    response = json.dumps({"resultado" : result}).encode()

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties= pika.BasicProperties(correlation_id=props.correlation_id),
        body = (response)
)

def ackMessage(ch, method):
    ch.basic_ack(delivery_tag=method.delivery_tag)