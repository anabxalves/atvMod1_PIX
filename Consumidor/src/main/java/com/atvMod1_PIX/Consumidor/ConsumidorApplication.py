import pika
import json
import os

# Função para processar as mensagens recebidas
def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        log_message = (f"[{message['timestamp']}] {message['bank_dest']} - {message['consumer_name']}: "
                       f"Recebido R$ {message['amount']} via PIX de {message['producer_name']} - {message['bank_origin']}.")
        print(log_message)
        
        # Função para gravar a mensagem no arquivo log.txt
        write_to_log(log_message)
        
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar a mensagem: {e}")

# Função para gravar a mensagem no arquivo log.txt
def write_to_log(message):
    log_file_path = 'atvMod1_PIX/Consumidor/src/main/java/com/atvMod1_PIX/consumer_log.txt'
    # Abrir o arquivo em modo de adição ('a') para não sobrescrever o conteúdo
    with open(log_file_path, 'a') as log_file:
        log_file.write(message + '\n')  # Escreve a mensagem e adiciona uma nova linha

# Configurações do RabbitMQ com URL de conexão AMQPS
def main():
    # Passando a URL de conexão
    url = 'amqps://vbiidqub:WB5wOr8lg7Aujc3ySCV0NdbLAWdIpcOC@prawn.rmq.cloudamqp.com/vbiidqub'
    connection_params = pika.URLParameters(url)
    
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    # Declarando o exchange do tipo tópico
    channel.exchange_declare(exchange='topic-exchange', exchange_type='topic', auto_delete=True)

    # Declarando a fila
    channel.queue_declare(queue='PIX_notifications')

    # Ligando a fila ao exchange com uma chave de roteamento genérica para capturar todas as mensagens de PIX
    channel.queue_bind(exchange='topic-exchange', queue='PIX_notifications', routing_key='pix.#')

    # Consumindo as mensagens da fila
    channel.basic_consume(
        queue='PIX_notifications', 
        on_message_callback=callback, 
        auto_ack=True
    )

    print(" [*] Aguardando mensagens. Para sair, pressione CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    main()
