import threading
import serial
import binascii
import calibration_restoration_EEPROM as cre

class recvData(threading.Thread):
    def __init__(self):
        super(recvData, self).__init__()

        self.listing = [] #the received data is put in a list

        #configure serial connection
        self.ser = serial.Serial(port='/dev/ttyUSB0',baudrate=256000,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)

    def run(self):              
        while len(self.listing) < 832: #temporary for now just for 0x01, when 0x02 is going to be read it is to be changed to be continuous
            read = self.ser.read(self.ser.inWaiting())
            if read != b'':
                for i in range(0, len(binascii.hexlify(read).decode()), 4):
                    self.listing.append(binascii.hexlify(read).decode()[i: i+4])
        self.ser.close()
        # print(self.listing)
    
    #Get values for 0x01 instruction of MLX
    def getListing(self):
        while len(self.listing) != 832:
            pass
        return self.listing

class Base():
    def __init__(self):
        self.ser = recvData() 
        self.ser.start() #run thread

    def main(self):
        self.ser.ser.write(b'\x01')
        eeprom_data = cre.calibration_restoration_EEPROM(self.ser.getListing())
        print(eeprom_data.extractVDDParams())
        print(eeprom_data.extractPTATParams()) ## Ask Sujay for missing code in matlab, why and how to access ram?
        print(eeprom_data.extractGainCoef()) 
        print(eeprom_data.extractTGCCoef()) 
        print(eeprom_data.extractResConCoef()) 
        print(eeprom_data.extractKsTaCoef())
        print(eeprom_data.extractKsToCoef()) ## Ask Sujay why the corner temperatures (ct) are also calculated under this function in matlab
        print(eeprom_data.extractCornerTemps())

if __name__ == '__main__':
    b = Base() 
    b.main()