import serial



class SerialController:
        
    def __init__(self):
        self.__correctionKey = {
            "Actylene": 0.58, "Air": 1.00, "Ammonia": 0.73, 
            "Argon": 1.39, "Arsine": 0.67, "Boron Trichloride": 0.41, 
            "Bromine": 0.81, "Carbon Dioxide": 0.70, 
            "Carbon Monoxide": 1.00, "Carbon Tetrachloride": 0.31, 
            "Carbon Tetraflouride": 0.42, "Chlorine": 0.86, 
            "Chlorodifluoromethane": 0.46, "Chloropentafluoroethane": 0.24, 
            "Cyanogen": 0.61, "Deuterium": 1.00, "Diborane": 0.44, 
            "Dibromodifluoromethane": 0.19, "Dichlorodifluoromethane": 0.35, 
            "Dichlorofluoromethane": 0.42, "Dichloromethysilane": 0.25, 
            "Dichlorosilane": 0.40, "Dichlorotetrafluoroethane": 0.22, 
            "Difluoroethylene": 0.43, "Dimethylpropane": 0.22, 
            "Ethane": 0.50, "Fluorine": 0.98, "Fluoroform": 0.50, 
            "Freon - 11": 0.33, "Freon - 12": 0.35, "Freon - 13": 0.38, 
            "Freon - 14": 0.42, "Freon - 21": 0.42, "Freon - 22": 0.46, 
            "Freon - 23": 0.50, "Freon - 113": 0.20, "Freon - 114": 0.22, 
            "Freon - 115":0.24 , "Freon - 116":0.24, "Freon - C318":0.16, 
            "Freon - 1132A":0.43, "Helium":1.45, "Hexafluoroethane":0.24,
            "Hydrogen": 1.01, "Hydrogen Bromide":1.00, 
            "Hydrogen Chloride":1.00, "Hydrogen Fluoride":1.00, 
            "Isobutylene":0.29, "Krypton":1.54, "Methane":0.72, 
            "Methyl Fluoride":0.56, "Molybdenum Hexafluoride":0.21, 
            "Neon":1.46, "Nitric Oxide":0.99, "Nitrogen":1.00, 
            "Nitrogen Dioxide":0.74, "Nitrogen Trifluoride":0.48, 
            "Nitrous Oxide":0.71, "Octafluorocyclobutane":0.164, 
            "Oxygen":1.00, "Pentane":0.21, "Perfluoropropane":0.17, 
            "Phosgene":0.44, "Phosphine":0.76, "Propane":0.36, 
            "Propylene":0.41, "Silane":0.60, 
            "Silicon Tetrachloride": 0.28, "Silicon Tetrafluoride":0.04,
            "Sulfur Dioxide":0.69, "Sulfur Hexafluoride":0.26, 
            "Trichlorofluoromethane":0.33, "Trichlorosilane":0.33, 
            "Tungsten Hexafluoride":0.25, "Xenon":1.32}

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
        self.ser.write(setter)
        return self.receivePressure()         


    def flowSendAndReceive(self, setpoint, port):
        setpoint = self.format(setpoint)
        setter = ('FS ' + str(port) + ' ' + str(setpoint) + ' \r')
        setter = setter.encode()
        self.ser.write(setter)
        return self.receiveFlow(port)         
        

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

    def openPort(self, port, gas):
        command = ('ON ' + str(port) + ' \r')
        command = command.encode()
        cf = ('GC ' + str(port) + ' ' + str(int(self.__correctionKey[gas]*100)).zfill(3) + ' \r')
        cf = cf.encode()
        self.ser.write(cf)
        self.ser.write(command)


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