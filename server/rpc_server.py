import json
import uuid
import pika
from common.rpc_utils import createConnectionAndChannel, sendReply, ackMessage

class InternalClient:
    def __init__(self):
        self.connection, self.channel = createConnectionAndChannel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body.decode())

    def call_service(self, queue_target, valores):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        
        payload = json.dumps({"valores": valores})
        
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_target,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=payload.encode()
        )
        
        while self.response is None:
            self.connection.process_data_events()
        
        return self.response.get("resultado")


internal_client = InternalClient()

def onMessage(ch, method, props, body):
    data = json.loads(body.decode())
    
    operacao = data.get("operacao") 
    valores = data.get("valores")
    
    print(f" [Server Principal] {operacao} com valores {valores}")
    
    resultado_final = 0
    
    if operacao == 'soma':

        resultado_final = internal_client.call_service('somaQueue', valores)
    elif operacao == 'multiplica':
        resultado_final = internal_client.call_service('multiplicaQueue', valores)
    else:
        resultado_final = "Erro: Operação desconhecida"

    print(f" [Server Principal] Resultado obtido do serviço: {resultado_final}")

    sendReply(ch, props, resultado_final)
    ackMessage(ch, method)

if __name__ == "__main__":
    connection, channel = createConnectionAndChannel()
    queueName = "mainServerQueue"
    
    channel.queue_declare(queue=queueName)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queueName, on_message_callback=onMessage)
    
    print(f" [Server Principal] Aguardando requisições na fila '{queueName}'...")
    channel.start_consuming()