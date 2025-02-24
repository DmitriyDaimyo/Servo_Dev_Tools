# Servo Dev Tools

## Introduction
Servo Dev Tools is a toolkit designed for programming Dynamixel servomotors. It enables developers to work with Dynamixel motors in Python without worrying about low-level communication details.

The project is built around the **STM32F407** microcontroller, which serves as a bridge between a **Raspberry Pi 5** and Dynamixel servomotors.

## Features
- **High-Level Python Interface**: Control Dynamixel servomotors without handling low-level communication.
- **STM32 Firmware**: A firmware implementation for STM32F407 to manage the communication between Raspberry Pi and servomotors.
- **Support for Multiple Commands**: Provides an interface for basic Dynamixel commands.

## Hardware Requirements
- **STM32F407** microcontroller
- **Raspberry Pi 5**
- **Dynamixel servomotors**


## Usage
### Python Module
Use the `low_level.py` module to send commands to Dynamixel servos:
```python
from low_level import *

descr = open_connection('/dev/ttyUSB0', 921600)


for i in range(254):
    ret = Ping(descr, i)

    if ret == -1:
        print("Ping error")
        close_connection(descr)
        exit()
    if ret != None:
        print(ret)
```

### Firmware Compilation
The STM32 firmware consists of the following files:
- `main.c` - Main firmware logic
- `clock.c`, `clock.h` - Clock configurations
- `stm32_startup_own.c` - Startup file
- `stm32_ls.ld` - Linker script
- `Makefile` - Build system



## Contact
For any questions or issues, feel free to open an issue or reach out at [dima.gusev.0232@gmail.com].

