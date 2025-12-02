# Sistema de Cálculo Distribuído (RPC via RabbitMQ)

Este pacote fornece uma implementação básica de um sistema de Chamada de Procedimento Remoto (RPC) utilizando **Python** e **RabbitMQ**. O projeto demonstra uma arquitetura onde um servidor central orquestra operações matemáticas delegando-as para *workers* (serviços) específicos.

## Funcionalidades (O que foi implementado)

* **Arquitetura RPC:** Implementação sobre o protocolo AMQP 0-9-1.
* **Microserviços:** Workers independentes para Soma e Multiplicação.
* **Orquestrador:** Servidor central que roteia requisições e agrega respostas.
* **Interface CLI:** Cliente interativo para entrada de dados do usuário.
* **Comunicação Assíncrona:** Uso de filas e *correlation_ids* para gestão de mensagens.

## Dependências Necessárias

* **Python 3.8+**
* **RabbitMQ Server** (Rodando na porta padrão)
* **Pika** (Biblioteca cliente RabbitMQ)

## Quick Start

### 1. Clonar e Instalar Dependências

Certifique-se de estar na raiz do projeto.

```bash
# Clone o repositório (exemplo)
git clone [https://github.com/SEU_USER/SEU_REPO.git]
cd SEU_REPO

# Instale a lib pika
pip install pika

2. Como Executar

Abra 4 terminais na pasta raiz do projeto e execute os comandos na ordem abaixo.

    Nota: python -m para garantir que os imports absolutos funcionem corretamente.

Terminal 1 (Worker de Soma):
Bash

python3 -m services.service_soma

Terminal 2 (Worker de Multiplicação):
Bash

python3 -m services.service_multiplica

Terminal 3 (Servidor Principal/Orquestrador):
Bash

python3 -m server.rpc_server

Terminal 4 (Cliente/Interface):
Bash

python3 -m client.rpc_client

Fluxo Esperado de Funcionamento

    Cliente envia operação e números para a fila mainServerQueue.

    Servidor Principal recebe a mensagem, decide qual serviço chamar e encaminha para somaQueue ou multiplicaQueue.

    Serviço (Worker) consome a fila específica, processa o cálculo e devolve o resultado para o Servidor.

    Servidor Principal devolve o resultado final para a fila de callback do Cliente.

Exemplos de Saída

No Terminal do Cliente:

=== MENU ===
1. Somar
2. Multiplicar
Escolha uma opção: 2

--- Digite os números (digite t e confirme para sair)
Digite o 1º número: 10
Digite o 2º número: 5
Digite o 3º número: t
 [Client] Solicitando 'multiplica' com [10.0, 5.0]...
 --> Resultado da Multiplicação: 50.0

No Terminal do Servidor:
 
 [Server Principal] Aguardando requisições na fila 'mainServerQueue'...
 [Server Principal] multiplica com valores [10.0, 5.0]
 [Server Principal] Resultado obtido do serviço: 50.0


Exemplo 2: Soma
Cliente:

=== MENU ===
1. Somar
2. Multiplicar
Escolha uma opção: 1

--- Digite os números (digite t e confirme para sair)
Digite o 1º número: 20
Digite o 2º número: 30.5
Digite o 3º número: t
 [Client] Solicitando 'soma' com [20.0, 30.5]...
 --> Resultado da Soma: 50.5

Servidor Principal:

 [Server Principal] Aguardando requisições na fila 'mainServerQueue'...
 [Server Principal] multiplica com valores [10.0, 5.0]
 [Server Principal] Resultado obtido do serviço: 50.0
 [Server Principal] soma com valores [20.0, 30.5]
 [Server Principal] Resultado obtido do serviço: 50.5
