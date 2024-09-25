package com.atvMod1_PIX.Produtor;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.core.TopicExchange;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Scanner;

@SpringBootApplication
public class ProdutorApplication {
    static final String exchangeName = "topic-exchange";
	private Scanner sc = new Scanner(System.in);
	private String producerName;
	private String originBank;

	@Autowired
	private RabbitTemplate rabbitTemplate;

	@Bean
	TopicExchange exchange() {
		return new TopicExchange(exchangeName, false, true);
	}

	public ProdutorApplication() {
		System.out.println("Informe seu nome:");
		producerName = sc.nextLine();

		System.out.println("Informe seu banco:");
		originBank = sc.nextLine();
	}

	private void sendPix() {
		System.out.println("Informe o banco de destino:");
		String destinationBank = sc.nextLine();

		System.out.println("Informe o nome do destinatário:");
		String consumerName = sc.nextLine();

		System.out.println("Informe o valor:");
		float amount = sc.nextFloat();
		sc.nextLine();  // consume the leftover newline

		LocalDateTime timestamp = LocalDateTime.now();
		DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

		String message = String.format("[%s] Tópico (%s) - (%s): Recebido R$ %.2f via PIX de %s - Tópico (%s).",
				timestamp.format(formatter), destinationBank, consumerName, amount, producerName, originBank);

		String routingKey = "pix." + destinationBank.toLowerCase() + "." + consumerName.toLowerCase();

		rabbitTemplate.convertAndSend(exchangeName, routingKey, message);
	}


	public static void main(String[] args) {
		// Let Spring handle the instantiation and dependency injection
		SpringApplication.run(ProdutorApplication.class, args).getBean(ProdutorApplication.class).start();
	}

	public void start() {
		while (true) {
			System.out.println("Deseja enviar um PIX? (s/n)");
			if (!sc.nextLine().equalsIgnoreCase("s")) {
				break;
			}
			sendPix();
		}
	}
}