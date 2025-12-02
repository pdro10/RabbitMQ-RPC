import json 
from common.rpc_utils import createConnectionAndChannel, sendReply, ackMessage

def soma(valores):
    return sum(valores)


def onMessage(ch, method, props, body):
    data = json.loads(body.decode())
    valores = data.get("valores")
    result = soma(valores)
    sendReply(ch, props, result)
    ackMessage(ch, method)

if __name__ == "__main__":

    connection, channel =  createConnectionAndChannel()
    queueName = "somaQueue"
    channel.queue_declare(queue=queueName)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queueName, on_message_callback = onMessage)
    channel.start_consuming()
