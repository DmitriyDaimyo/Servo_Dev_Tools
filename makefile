CC=/home/domino/education/project/arm-gnu/bin/arm-none-eabi-gcc
OBJDUMP=/home/domino/education/project/arm-gnu/bin/arm-none-eabi-objdump
MACH=cortex-m4
OPENOCD=/home/domino/education/project/xpack-openocd-0.12.0-3/bin/openocd
GDB=arm-none-eabi-gdb

CFLAGS= -c -mcpu=$(MACH) -mthumb -std=gnu11 -Wall -O0 -I/home/domino/education/project/code/inlcude/ -I/home/domino/education/project/code/stm32f4-discovery-lib-master/cmsis/ -I/home/domino/education/project/code/stm32f4-discovery-lib-master/stm32/
LINKFLAGS= -nostdlib -T stm32_ls.ld -Wl,-Map=final.map
OBJDUMP_FLAGS= -h

all:main.o stm32_startup_own.o clock.o


	
main.o:main.c
	$(CC) $(CFLAGS) $^ -o $@ 

clock.o:clock.c
	$(CC) $(CFLAGS) $^ -o $@ 

stm32_startup_own.o: stm32_startup_own.c
	$(CC) $(CFLAGS) $^ -o $@ 

final.elf: clock.o main.o stm32_startup_own.o 
	$(CC) $(LINKFLAGS) $^ -o $@
	
objdump_elf: final.elf
	$(OBJDUMP) $(OBJDUMP_FLAGS) $^
clean:
	rm -rf *.o *.elf
	
load:
	$(OPENOCD) -f /home/domino/education/project/xpack-openocd-0.12.0-3/openocd/scripts/board/stm32f4discovery.cfg

gdb:
	$(GDB)
