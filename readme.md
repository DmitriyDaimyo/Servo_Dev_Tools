stm32 is configured with 2 uarts:
    -UART4: half-duplex uses pin PC10, connected to dynamixel. Comunicates with dynamixel (1000000)
    -USART2: full-duplex uses pins PA2 as transmitter and PA3 as receiver. Transfers status packet received from dynamixel via PA2 (115200)





FIRMWARE UPDATE gdb commands

1) target remote localhost:3333
2) monitor reset halt
3) monitor flash write_image erase final.elf