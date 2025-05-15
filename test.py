from low_level import *
import time
descr = open_connection('/dev/ttyAMA0', 921600)
if descr == -1:
    print("OPEN error")
    exit()

for i in range(254):
    #print(i)
    ret = Ping(descr, i)
    print(ret)
    if ret == -1:
        print("Ping error")
        close_connection(descr)
        exit()
    if ret != 0:
        print("Return Ping", ret)


print(Write(descr, 4, 32, [0xff, 0x0]))
print(Write(descr, 15, 32, [0xff, 0x0]))
print(Write(descr, 4, 30, [0x0, 0x0]))
print(Write(descr, 15, 30, [0x0, 0x0]))




close_connection(descr)