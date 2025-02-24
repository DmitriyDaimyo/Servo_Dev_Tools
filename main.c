

#include"clock.h"
#include"../include/stdint.h"


void green_led_on(void)
{
	GPIOD->BSRRL |= (uint16_t)(0b1 << 12);	//output configuration (on)
}


void green_led_off(void)
{
	GPIOD->BSRRH |= (uint16_t)(0b1 << 12); //output configuration (off)
}




//UART4 is needed to establish connection between stm and dynamixel
//UART2 is needed to establish connection between computer and stm

void UART4_and_USART2_Configure(void){

	//1. Enable the UART CLOCK and GPIO CLOCK (APB1 AHB1)
	RCC->APB1ENR |= RCC_APB1ENR_UART4EN;
	RCC->APB1ENR |= RCC_APB1ENR_USART2EN;
	RCC->AHB1ENR |= RCC_AHB1ENR_GPIOCEN; //for UART4 pins	
	RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN; //for UART2 pins

	//2. Set GPIO mode for UART2
	GPIOA->MODER |= (2<<4);
	GPIOA->MODER |= (2<<6);
	GPIOA->PUPDR |= (1<<4);
	GPIOA->OSPEEDR |= (3<<4) | (3<<6);
	GPIOA->AFR[0] |= (7<<8);
	GPIOA->AFR[0] |= (7<<12);

	//2. Set GPIO mode for UART4
	GPIOC->MODER   |= (1<<21); //alternate function mode
	GPIOC->OTYPER  |= (0<<10); //push-pull
	GPIOC->PUPDR   |= (1<<20); //pull-up
	GPIOC->OSPEEDR |= (1<<20) | (1<<21); //very high speed
	GPIOC->AFR[1]  |= (1<<11); //UART4 choosen


	//3. Enable the USART by writing the UE bit in USART_CR1 register to 1
	UART4->CR1 |= USART_CR1_UE;
	USART2->CR1 |= USART_CR1_UE;

	//4. Select the desired baud rate using the USART_BRR register
	UART4->BRR = ((unsigned short)(10 << 0) | (unsigned short)(2 << 4));
	USART2->BRR = ((unsigned short)(14 << 0) | (unsigned short)(2 << 4));

	//5. Enable half-duplex for UART4
	UART4->CR3 |= (1<<3);

	//6. Enable the Transmitter/Receiver by Setting the TE and RE bits in UART_CR1 Register
	//UART4->CR1 |= (1<<2);
	UART4->CR1 &= ~(1<<3); //transmitter disabled
	UART4->CR1 |= (1<<2); //receiver enabled

	USART2->CR1 |= (1<<3); //transmitter enable for UART2
	USART2->CR1 |= (1<<2); //receiver enable for UART2
}



void UART4_SendChar(unsigned char c){

	while (!(UART4->SR & (1<<7))){			//while (!(UART4->SR & (1<<7))) when transfering data
		//green_led_on();						////while (!(UART4->SR & (1<<6))) when changing from transfering data to receiving
	};
	UART4->DR = c;

}

void USART2_SendChar(unsigned char c){

	while (!(USART2->SR & (1<<7))){			
							
	};
	USART2->DR = c;
	//green_led_on();	

}

char read_bufer[50];




//Send_instruction will automatically form cheksum field of packet but this field must be added to byte_num
int Send_instruction(char inst[], unsigned int byte_num){

	char status_bufer[256];

	//preparing line for transmitting instruction
	UART4->CR1 &= ~(1<<2); //receiver disabled
	UART4->CR1 |= (1<<3); //transmitter enabled

	//form and send packet
	unsigned char checksum = inst[2];
	for(int i = 0; i < inst[3]; i++){
		checksum += inst[i+3];
	}
	checksum  = ~(checksum);
	unsigned char checksum_from_packet = inst[byte_num-1];

	if (checksum_from_packet != checksum){
		return -1;
	}


	for(int i = 0; i < byte_num; i++){
		UART4_SendChar(inst[i]);
	}

	//wait until the transmitter is done
	while (!(UART4->SR & (1<<6))){

	}

	//preparing line for receiving data from dynamixel
	UART4->CR1 &= ~(1<<3); //transmitter disabled
	UART4->CR1 |= (1<<2); //receiver enabled

	//receiving bytes from dynamixel
	unsigned short status_length = 0;
	while(1){

		unsigned int timer = 0;
		unsigned short flag_no_data = 0;
		

		while (!(UART4->SR & (1<<5))){
			timer++;
			if(timer == 10300){
				flag_no_data = 1;
				break;
			}			
		}

		if (flag_no_data == 1){
			break;
		}

		status_bufer[status_length++] = UART4->DR;
	}

	//sending bytes to computer
	for (int i = 0; i < status_length; i++){
		USART2_SendChar(status_bufer[i]);
	}
	return 0;
}










void main(void)
{
	Clock_Config();
	
	UART4_and_USART2_Configure();
	
	RCC->AHB1ENR |= RCC_AHB1ENR_GPIODEN; 
	GPIOD->MODER |= (uint32_t)(0b1 << 24);	//green led
	GPIOD->PUPDR |= (uint32_t)(0b1 << 24);

	char get_instruction_buffer[255];
	unsigned char byte_counter = 0;
	unsigned char length;

	while (1)
	{
		while (!(USART2->SR & (1<<5))){
		}
		get_instruction_buffer[byte_counter++] = USART2->DR;

		if(byte_counter == 4){
			length = get_instruction_buffer[byte_counter-1];
		}

		if( (byte_counter > 4) && (byte_counter == (length + 4)) ){

			int status = Send_instruction(get_instruction_buffer, byte_counter);
			byte_counter = 0;
			length = 0;
		}
		
	}

}
	
