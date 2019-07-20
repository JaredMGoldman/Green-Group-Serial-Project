# import serial

# print(1)
# ser = serial.Serial(
#     port='/dev/cu.usbserial-AM00HUNS',
#     baudrate=9600,
#     parity=serial.PARITY_EVEN,
#     stopbits=serial.STOPBITS_ONE,
#     bytesize=serial.EIGHTBITS
# )
# print(2)
# ser.isOpen()
# myString = 'PU R <cr>'
# b = myString.encode('ascii')
# ser.write(b)
# print(3)
# ret = ser.read(4)
# ret = ret.decode('ascii')
# print(4)

# print(ret)

op = 1 % 30
po = 30 % 1


print(op)
print(po)