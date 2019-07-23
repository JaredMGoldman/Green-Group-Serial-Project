import serial



class SerialController:
        
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/tty.usbserial-AM00HUNS',
            baudrate=9600,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS, 
            timeout = 10
        )
        self.CARRAIGE_RETURN = '\r'
        self.CARRAIGE_RETURN = self.CARRAIGE_RETURN.encode()

    def default(self):
        # Make default pressure units 1000 Pa
        setter = 'PU 24 \r'
        setter = setter.encode('utf-8')
        getter = 'PU R \r'
        getter = getter.encode('utf-8')
        self.ser.write(setter)
        self.ser.write(getter)
        self.ser.read_until(self.CARRAIGE_RETURN)

        # Make default flow rate units 1000 SCCM
        for i in range (1,9):
            setter = ('RA ' + str(i) + ' 6 \r')
            setter = setter.encode('utf-8')
            getter = ('RA ' + str(i) + ' R \r')
            getter = getter.encode('utf-8')
            self.ser.write(setter)
            self.ser.write(getter)
            self.ser.read_until(self.CARRAIGE_RETURN)

    
    def pressureSendAndReceive(self, setpoint):
        setpoint = self.format(setpoint)
        setter = ('PS ' + setpoint + ' \r')
        setter = setter.encode()
        getter0 = 'PS R \r'
        getter0 = getter0.encode()
        self.ser.write(setter)
        self.ser.write(getter0)
        out = self.ser.read_until(self.CARRAIGE_RETURN)
        out = int(out)
        out = out * 0.1
        return out
        
        # return self.receivePressure()         For testing purposes


    def flowSendAndReceive(self, setpoint, port):
        setpoint = self.format(setpoint)
        setter = ('FS ' + str(port) + ' ' + str(setpoint) + ' \r')
        setter = setter.encode()
        getter0 = ('FS ' + str(port) + ' R \r')
        getter0 = getter0.encode()
        self.ser.write(setter)
        self.ser.write(getter0)
        out = self.ser.read_until(self.CARRAIGE_RETURN)
        out = int(out)
        out = out * 0.1
        return out
        
        # return self.receiveFlow(port)         For testing purposes
        

    def receivePressure(self):
        getter = 'PR \r'
        getter = getter.encode()
        self.ser.read_until(self.CARRAIGE_RETURN)
        self.ser.write(getter)
        out = self.ser.read_until(self.CARRAIGE_RETURN)
        out = int(out)
        out = out * 0.1
        return out

    def receiveFlow(self, port):
        getter = ('FL ' + str(port) + ' \r')
        getter = getter.encode()
        self.ser.write(getter)
        out = self.ser.read_until(self.CARRAIGE_RETURN)
        out = int(out)
        out = out * 0.1
        return out

    def openPort(self, port):
        command = ('ON ' + str(port) + ' \r')
        command = command.encode()
        status = ('ST ' + str(port) + ' \r')
        status = status.encode()
        self.ser.write(command)
        self.ser.write(status)
        self.ser.read_until(self.CARRAIGE_RETURN)

    def close(self):
        for i in range(1,9):
            command = ('OF ' + str (i) +  ' \r')
            command = command.encode()
            self.ser.write(command)
        self.ser.close()

    def format(self, setpoint):
        setpoint = int(setpoint * 10.0)
        setpoint = str(setpoint)
        setpoint = setpoint.zfill(4)
        return setpoint