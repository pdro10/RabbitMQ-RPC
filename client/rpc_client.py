import pika
import json
import uuid
from common.rpc_utils import createConnectionAndChannel

class RpcClient:
    def __init__(self):
        self.connection, self.channel = createConnectionAndChannel()
        
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.onResponse,
            auto_ack=True
        )
        self.response = None
        self.corr_id = None

    def onResponse(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            data = json.loads(body.decode())
            self.response = data.get("resultado")

    def call(self, operacao, valores):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        
        msg = {
            "operacao": operacao,
            "valores": valores
        }

        print(f" [Client] Solicitando '{operacao}' com {valores}...")
        
        self.channel.basic_publish(
            exchange='',
            routing_key='mainServerQueue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(msg).encode()
        )
        
        while self.response is None:
            self.connection.process_data_events()
            
        return self.response

def obterNumeros():
    listaNumeros = []
    print("\n--- Digite os números  (digite t e confirme para sair)") 
    
    contador = 1
    while True:
        entrada = input(f"Digite o {contador}º número: ")
        
        if entrada.strip() == "t" or entrada.strip() == "T":
            if len(listaNumeros) == 0:
                print("Você precisa digitar pelo menos um número!")
                continue
            break
        
        try:
            numero = float(entrada)
            listaNumeros.append(numero)
            contador += 1
        except ValueError:
            print("Isso não é um número válido. Tente novamente.")
            
    return listaNumeros

if __name__ == "__main__":
    client = RpcClient()

    while True:
        print("\n=== MENU ===")
        print("1. Somar")
        print("2. Multiplicar")
        print("s. Sair")
        opc = input("Escolha uma opção: ")
        
        if opc == 's' or opc == "S":
            print("Saindo...")
            break
        
        if opc not in ['1', '2']:
            print("Opção inválida.")
            continue

        valores = obterNumeros()
        
        if opc == '1':
            res = client.call("soma", valores)
            print(f" --> Resultado da Soma: {res}")
        elif opc == '2':
            res = client.call("multiplica", valores)
            print(f" --> Resultado da Multiplicação: {res}")