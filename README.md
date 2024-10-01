# Sistema de Validação de Transações Bancárias

Esse sistema foi desenvolvido para a disciplina de Fundamentos de Computação Corrente, Paralela e Distribuída (FCCPD), fundamentando-se em um sistema de envio e recebimento de mensagens com interação com o usuário que disponibiliza acesso, por meio de comandos de linha, a todas as operações possíveis de serem realizadas.

## Equipe

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/anabxalves">
        <img src="https://avatars.githubusercontent.com/u/108446826?v=4" width="200px;" alt="Foto Ana"/><br>
        <sub>
          <b>Ana Beatriz Alves</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/alwolmer">
        <img src="https://avatars.githubusercontent.com/u/108356950?v=4" width="200px;" alt="Foto Arthur"/><br>
        <sub>
          <b>Arthur Wolmer</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Caiobadv">
        <img src="https://avatars.githubusercontent.com/u/117755420?v=4" width="200px;" alt="Foto Caio"/><br>
        <sub>
          <b>Caio Barreto</b>
        </sub>
      </a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/diegopluna">
        <img src="https://avatars.githubusercontent.com/u/111078608?v=4" width="200px;" alt="Foto Diego"/><br>
        <sub>
          <b>Diego Peter</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/virnaamaral">
        <img src="https://avatars.githubusercontent.com/u/116957619?v=4" width="200px;" alt="Foto Virna"/><br>
        <sub>
          <b>Virna Amaral</b>
        </sub>
      </a>
    </td>
  </tr>
</table>
<br>

## Contexto do Sistema

O projeto desenvolve um sistema de notificação para validação de pagamentos via Pix. Nele, quando um cliente realiza um pagamento, o sistema enviará uma mensagem para o cliente e empresa destinatária, informando a confirmação da transação. Ao mesmo tempo, um backend de auditoria, representado pelo BACEN, registrará todas as transações para monitoramento e controle.

## Execução

Para executar nosso sistema, siga as instruções e orientações abaixo:

1. **Criar Ambiente Virtual**
>- MacOS/Linux: `python3 -m venv venv`
>- Windows: `python -m venv venv`

2. **Ativar ambiente virtual**
>No diretório da pasta "venv" (criado acima):
>- MacOS/Linux: `source venv/bin/activate`
>- Windows: `venv/Scripts/activate`

3. **Clonar repositório**
>Com o ambiente "venv" ativado:
>- `git clone https://github.com/anabxalves/atvMod1_PIX`

4. Ajustar servidor AMPQ, no Cloud MQP e RabbitMQ, ajuste o link no arquivo `consumidor.py`, no local indicado:
<p align="center">
  <img src="https://private-user-images.githubusercontent.com/108446826/371925192-55051108-fe1f-4ae2-b499-13c56d75fa06.jpeg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Mjc2NjQyNzksIm5iZiI6MTcyNzY2Mzk3OSwicGF0aCI6Ii8xMDg0NDY4MjYvMzcxOTI1MTkyLTU1MDUxMTA4LWZlMWYtNGFlMi1iNDk5LTEzYzU2ZDc1ZmEwNi5qcGVnP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI0MDkzMCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDA5MzBUMDIzOTM5WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9N2M2MmNlNDRkMjhiYjcxZmVjYmQ3MzU4OTA2NjY5Zjk0YjY3MDc1NzRkOGYwYjdhZjA5NTAyMjEzZmMxNzY1YyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.HYoxARBp5o2fbzXU3cw2ugBSEkYZ-xU1RACjLfyKrM8" width="800"/>
</p>

5. Para quantidade de Produtores desejada, deve-se rodar o arquivo `ProdutorApplication.java`, em que cada instância será um produtor diferente. Realizando isso, no início de cada execução, será questionado o `nome` e `banco` de quem está enviando a transação, para posteriormente questionar o destinatário, seu banco e o valor da transação.
> Ressalta-se que é aqui que o roteamento é definido, pelo destinatário e banco para qual será enviado o PIX.

6. Para a quantidade de Consumidores desejada, deve-se instanciar o arquivo `consumidor.py`. Ao iniciar a execução, o Menu ofertará 3 opções de consumidor, sendo eles Auditoria BACEN, Banco e Destinatário, todos acima especificados.
> A depender do consumidor selecionado, as mensagens estarão sendo direcionadas conforme:
>- A Auditoria BACEN não somente receberá todas as menagens enviadas por todos os Produtores, como também é o responsável por printar todo o histórico de transações presente no log `consumer_log.txt`. A mensagem será roteada utilizando a chave `pix.#`.
>- O Banco receberá todas as transações que foram encaminhadas a sua instituição, sendo roteada com a chave `pix.{bank_name}.#`.
>- Já o Destinatário receberá apenas as transações que foram encaminhadas para ele, por meio do roteamento com chave `pix.{bank_name}.{consumer_name}`.

7. Ainda é possível conferir as transações realizadas durante as execuções no arquivo `consumer_log.txt`.

## Composição da Mensagem

As mensagens recebidas pelos Consumidores é composta da seguinte sintaxe:
> [TIMESTAMP] Tópico (Banco Destino) - (Nome Consumidor): Recebeu R$ (valor transação), via PIX, de (nome Produtor) - Tópico (Banco Origem).

## Tipo de Exchange Utilizado

O tipo de Exchange selecionado para rotear as mensagens em nosso sistema foi, conforme dito acima, o tipo **Topic**, criado usando a classe `TopicExchange` do Spring AMQP e configurado com o nome `"topic-exchange"`, marcado como não durável e autoexcluível (sendo removido quando não utilizado).
> Ressalta-se que o Topic Exchange é um mecanismo de roteamento que direciona as mensagens para as filas com base em chaves de roteamento específicas, permitindo utilizar padrões onde a chave de roteamento pode conter caracteres como `*` (que substitui uma única palavra) e `#` (que substitui zero ou mais palavras). Dessa forma, as filas que têm uma chave compatível com a chave de roteamento da mensagem recebem essa mensagem, permitindo ao nosso sistema a flexibilidade de roteamento com base em combinações de padrões, escutando todas as mensagens PIX.

## Linguagens Utilizadas e Arquivos

O sistema foi desenvolvido utilizando linguagens diferentes na implementação do Produtor e do Consumidor de mensagens, em que este foi desenvolvido em Python e aquele em Java.

### `consumidor.py`

Este código, desenvolvido em **Python** implementa um consumidor RabbitMQ que processa transações PIX, grava logs dessas transações e permite realizar auditoria ao imprimir o histórico das mensagens. Dependendo da escolha do usuário, o sistema pode monitorar todas as transações, ou focar apenas em mensagens de um banco ou destinatário específico.

#### Funções e Métodos

- `callback(ch, method, properties, body)`
> Essa função é chamada sempre que uma mensagem é recebida da fila, com o objetivo de processar a mensagem, tentando decodificar-la do formato JSON para um dicionário Python. Depois, monta uma string que contém informações do PIX recebido, como remetente, destinatário, valor, e bancos envolvidos: Se a mensagem for válida, essa string é gravada no arquivo de log e também impressa no console; Se houver um erro na decodificação da mensagem (JSON inválido), ele imprime o erro.

- `write_to_log(message)`
> Essa função grava as mensagens recebidas no arquivo `consumer_log.txt`: cada mensagem é adicionada no final do arquivo, mantendo o histórico de todas as mensagens processadas.

- `print_auditoria_log()`
> Essa função lê o conteúdo do arquivo de log `consumer_log.txt` e imprime todas as mensagens armazenadas, funcionando como uma auditoria das transações processadas e, se o arquivo não existir ou estiver vazio, a função informa isso.

- `define_queue_and_routing_keys()`
> Essa função coleta as informações do usuário para determinar qual fila será utilizada e quais chaves de roteamento serão configuradas para essa fila, apresentando um menu que permite ao usuário escolher o tipo de função que ele deseja realizar. Com base na escolha, essa função retorna o nome da fila e as chaves de roteamento adequadas, sendo elas:
>- **Auditoria BACEN**: Pode apenas imprimir o log ou escutar todas as mensagens PIX.
>- **Banco**: Permite configurar a fila para receber mensagens apenas de um banco específico.
>- **Destinatário**: Recebe mensagens para um destinatário específico em um banco específico.

- `main()`
> Essa é a função principal que conecta o programa ao servidor RabbitMQ via o protocolo AMQP, configurando a conexão com o servidor RabbitMQ e declarando um exchange do tipo topic, para depois chamar a função `define_queue_and_routing_keys()` para determinar o nome da fila e as chaves de roteamento, declarar a fila no RabbitMQ e fazer o binding da fila com o exchange utilizando as chaves de roteamento definidas, para, ao fim, começar a consumir as mensagens da fila, processando-as com a função `callback`.

### `ProdutorApplication.java`

Este código, desenvolvido em **Java**, representa um produtor de mensagens que envia dados sobre transações PIX para o RabbitMQ, solicitando ao usuário detalhes como banco de origem, banco de destino, nome do destinatário e valor da transação, montando uma mensagem JSON com esses dados, e a enviando para um exchange do tipo **Topic**, que, então, roteia a mensagem para a fila adequada, de acordo com a chave de roteamento.

#### Funções e Métodos

- `exchangeName`
> Essa variável armazena o nome do exchange (canal de troca) que será utilizado para enviar mensagens ao RabbitMQ.

- `sc`
> É o Scanner que captura a entrada do usuário a partir do terminal para coletar os dados necessários.

- `producerName e originBank`
> Armazenam o nome do produtor (usuário que está enviando o PIX) e o banco de origem, solicitados quando o programa é iniciado.

- `@Bean TopicExchange exchange()`
> Essa função configura o exchange do tipo tópico no RabbitMQ, definindo como as mensagens são roteadas entre as filas.

- Construtor `ProdutorApplication()`
> No construtor, o programa solicita ao usuário que insira o nome do produtor e o banco de origem, que são armazenadas nas variáveis `producerName` e `originBank`.

- `sendPix()`
> Essa função é responsável por coletar os detalhes de uma transação PIX e enviá-la para o RabbitMQ, solicitando ao usuário as informações do banco de destino, nome do destinatário e o valor da transação.
<br> Em seguida, obtém o timestamp atual e formata-o como uma string, criando um mapa contendo todos os detalhes da transação PIX (banco de origem, banco de destino, nome do destinatário, nome do produtor, valor da transação e timestamp), e, ainda, usando do `ObjectMapper`, converte a mensagem para o formato JSON.
<br> Por fim, monta a chave de roteamento no formato `"pix.<banco_destino>.<nome_destinatário>"`, permitindo que a mensagem seja roteada corretamente no RabbitMQ, baseado no banco de destino e no nome do destinatário, usando o RabbitTemplate para enviar a mensagem JSON para o exchange configurado, utilizando a chave de roteamento.

- `start()`
> Esse método entra em um loop infinito, onde pergunta ao usuário se ele deseja enviar um PIX: se o usuário responder "s", a função `sendPix()` é chamada para realizar a operação de envio de uma nova transação; e caso o usuário responda qualquer outra coisa, o loop é interrompido e o programa termina.

- `main()`
> No método main, o Spring Boot inicializa a aplicação e invoca o método `start()` para iniciar o loop principal da aplicação.

## Informações adicionais sobre o Sistema

- É possível executar várias instâncias de um mesmo “tipo” de consumidor, em que todas as cópias, com os mesmos Identificadores, recebem as mesmas mensagens;

- É possível executar vários produtores de mensagens;

- Além dos consumidores das mensagens, existe um backend de auditoria que recebe todas as mensagens enviadas (apenas exibe TODAS as mensagens para esse consumidor), guardando-os em um log `consumidor_log.txt`;

- O programa apresenta um “menu” de opções, contendo as opções de escolha de: produtor ou consumidor ou auditoria;
