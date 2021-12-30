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
        eepromData = cre.calibration_restoration_EEPROM(self.ser.getListing())
        print(eepromData.extractVDDParams())
        print(eepromData.extractPTATParams()) ## Ask Sujay for missing code in matlab, why and how to access ram?
        print(eepromData.extractGainCoef()) 
        print(eepromData.extractTGCCoef()) 
        print(eepromData.extractResConCoef()) 
        print(eepromData.extractKsTaCoef())
        print(eepromData.extractKsToCoef())
        print(eepromData.extractCornerTemps())
        print(eepromData.extractPixSens())
        print(eepromData.extractPixOff()) ## Ask Sujay whether results are okay even though they're way higher than in max 10^2 (10^4) 
        print(eepromData.extractKtaCoef())
        print(eepromData.extractKvCoef())
        print(eepromData.extractComPixSens())
        print(eepromData.extractComPixOff()) # Ask Sujay whether results are okay given that these differ from pixoff more than in example
        print(eepromData.extractKvComPixCoef())
        print(eepromData.extractKtaComPixCoef())
        print(eepromData.extractChessCorrCoef())
        print(eepromData.extractDeviatingPix()) # Ask Sujay how he found the way to calculate these deviating pixels since the data sheet doesn't show

if __name__ == '__main__':
    b = Base() 
    b.main()