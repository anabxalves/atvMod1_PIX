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
        write_to_log(log_message)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar a mensagem: {e}")

# Função para gravar a mensagem no arquivo log.txt
def write_to_log(message):
    log_file_path = 'consumer_log.txt'
    with open(log_file_path, 'a') as log_file:
        log_file.write(message + '\n')

# Função para ler e printar o arquivo de log
def print_auditoria_log():
    log_file_path = 'consumer_log.txt'
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            logs = log_file.readlines()
            if logs:
                print("### INÍCIO DO LOG DE AUDITORIA ###")
                for log in logs:
                    print(log.strip())
                print("### FIM DO LOG DE AUDITORIA ###")
            else:
                print("O arquivo de log está vazio.")
    else:
        print("O arquivo de log não foi encontrado.")

def main():
    url = 'amqps://vbiidqub:WB5wOr8lg7Aujc3ySCV0NdbLAWdIpcOC@prawn.rmq.cloudamqp.com/vbiidqub'
    connection_params = pika.URLParameters(url)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    # Declarando o exchange do tipo tópico
    channel.exchange_declare(exchange='topic-exchange', exchange_type='topic', auto_delete=True)

    # Configuração da fila e Routing Key com base na escolha do usuário
    queue_name, routing_keys = define_queue_and_routing_keys()

    if routing_keys:
        # Declarando a fila
        channel.queue_declare(queue=queue_name)

        # Ligando a fila ao exchange com as chaves de roteamento calculadas
        for routing_key in routing_keys:
            print(f"Ligando a fila {queue_name} ao exchange com a chave de roteamento: {routing_key}")
            channel.queue_bind(exchange='topic-exchange', queue=queue_name, routing_key=routing_key)

        # Consumindo as mensagens da fila
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        print(f" [*] Aguardando mensagens na fila {queue_name}. Para sair, pressione CTRL+C")
        channel.start_consuming()

def define_queue_and_routing_keys():
    routing_keys = []
    queue_name = ""

    # Menu para escolha
    print("Escolha sua função:")
    print("1. Auditoria BACEN")
    print("2. Banco (Receber mensagens apenas de bancos específicos)")
    print("3. Destinatário (Receber mensagens apenas para um destinatário específico)")

    escolha = input("Digite o número da sua escolha: ").strip()

    if escolha == '1':
        # Submenu da Auditoria BACEN
        print("Escolha a opção de auditoria:")
        print("1. Printar log de auditoria")
        print("2. Receber todas as mensagens")

        auditoria_escolha = input("Digite o número da sua escolha: ").strip()

        if auditoria_escolha == '1':
            print_auditoria_log()
            return "", []  # Não precisa configurar fila para apenas printar o log
        
        elif auditoria_escolha == '2':
            print("Escutando todas as mensagens PIX.")
            queue_name = 'auditoria_bacen'
            routing_keys.append('pix.#')

    elif escolha == '2':
        # Banco: Receber mensagens de bancos específicos (independentemente do destinatário)
        print("Informe o nome do banco:")
        bank_name = input().strip().lower()
        queue_name = f'banco_{bank_name}'
        routing_keys.append(f'pix.{bank_name}.#')

    elif escolha == '3':
        # Destinatário: Receber mensagens destinadas a um destinatário específico
        print("Informe o nome do banco:")
        bank_name = input().strip().lower()
        print("Informe o nome do destinatário:")
        consumer_name = input().strip().lower()
        queue_name = f'{bank_name}_{consumer_name}'
        routing_keys.append(f'pix.{bank_name}.{consumer_name}')
    
    else:
        print("Escolha inválida. Por padrão, escutando todas as mensagens.")
        queue_name = 'auditoria_bacen'
        routing_keys.append('pix.#')

    return queue_name, routing_keys

if __name__ == '__main__':
    main()
