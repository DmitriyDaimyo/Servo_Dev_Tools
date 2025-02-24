import serial
import sys
import time



# INSTRUCTION TYPES ver 1
# 0x01 Ping
# 0x02 Read
# 0x03 Write
# 0x04 Reg_Write
# 0x05 Action
# 0x06 Factory Reset
# 0x08 Reboot
# 0x83 Sync_Write
# 0x92 Bulk_Read


def open_connection(file, baud):
    try:
        ser = serial.Serial(file, baud)
    except serial.SerialException as e:
        print(f"Error: {e}")
        return -1
    
    return ser


def close_connection(ser):
    ser.close()


def count_checksum(data: list):
    checksum_counted = 0
    counter = 0

    for bytes in data:
        if (counter > 1) and (counter < (data[3]+3)):      
            checksum_counted +=bytes
        counter+=1

    checksum_counted = (~(checksum_counted) & 0xff)
    return checksum_counted





def correct_checksum(data):
    checksum_from_pack = data[-1]

    if count_checksum(data) == checksum_from_pack:
        return 0
    else:
        return -1




#command parameter should contain proper data
#if exp_ret == 1 answer expected
def send_instruction(ser: serial.Serial, command: bytes, exp_ret: int):
    
    ser.write(command)
    ser.flush()

    if exp_ret == 1:
        time.sleep(0.01)
        data = []
        if ser.in_waiting > 0:
            while(True):
                newdata = ser.read(ser.in_waiting)
                for byte in newdata:
                    data.append(byte)

                if(ser.in_waiting == 0):
                    break


            check_pack = correct_checksum(data)
            if check_pack == -1:
                return -1
            
            return data
        else:
            return None
        
    else:
        return None






#COMMANDS
#Each command returns list of bytes if expected as answer from dynamixel 
#If no answer expected it returns 0
#If checksum of answer is not valid it returns -1





#Ping 
#returns 0 if no response
#returns packet if response received
#returns -1 if error occured
def Ping(ser, id: int):

    if id < 0 or id > 253:
        print("ERROR Ping: invalid id")
        return -1
    
    command = [0xff, 0xff, id, 0x2, 0x1, 0x0]

    command[-1] = count_checksum(command)

    byte_array = bytearray(command)

    answer = send_instruction(ser, byte_array, 1)

    if answer == -1:
        print("Checksum_error")
        return -1

    if answer == None: return 0
          
    else: return answer
    

#Read
#returns packet if response received
#returns -1 if error occured
def Read(ser, id: int, Starting_Address: int, Length_of_Data: int):

    if id < 0 or id > 253:
        print("ERROR Read: invalid id")
        return -1
    
    command = [0xff, 0xff, id, 0x04, 0x02, Starting_Address, Length_of_Data, 0x0]

    command[-1] = count_checksum(command)

    byte_array = bytearray(command)

    answer = send_instruction(ser, byte_array, 1)

    if answer == -1:
        print("Checksum_error")
        return -1
    
    else: return answer



#Write
#returns packet if response received
#returns -1 if error occured
#WARNING ACCORDING TO PROTOCOL THIS COMMAND CAN HAVE BROADCAST ID BUT IT IS NOT PERMITTED HERE
def Write(ser, id: int, Starting_Address: int, Data_List: list):

    if id < 0 or id > 253:
        print("ERROR Read: invalid id")
        return -1
    
    command = [0xff, 0xff, id, 0x3, 0x03, Starting_Address]

    for bytes in Data_List:
        command.append(bytes)
        command[3] += 1

    command.append(0x0)

    command[-1] = count_checksum(command)

    byte_array = bytearray(command)

    answer = send_instruction(ser, byte_array, 1)

    if answer == -1:
        print("Checksum_error")
        return -1
    
    else: return answer