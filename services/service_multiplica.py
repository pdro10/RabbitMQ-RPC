from common.rpc_utils import createConnectionAndChannel, sendReply, ackMessage
from math import prod
import json

def multiplica(valores):
    return prod(valores)

def onMessage(ch, method, props, body):
    data = json.loads(body.decode())
    valores = data.get("valores")
    result = multiplica(valores)
    sendReply(ch, props, result)
    ackMessage(ch, method)


if __name__ == "__main__":
    connection, channel = createConnectionAndChannel()
    queueName = "multiplicaQueue"
    channel.queue_declare(queue=queueName)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queueName, on_message_callback= onMessage)
    channel.start_consuming()



