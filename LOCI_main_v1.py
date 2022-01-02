import threading
import serial
import binascii
import calibration_restoration_EEPROM as cre

## TODO: TWO QUESTIONS AT extractDeviatingPix FUNCTION

class recvData(threading.Thread):
    def __init__(self):
        super(recvData, self).__init__()

        ## The received data is put in a list
        self.databuffer = [] 

        ## Configure the serial connection (the port might differ per machine)
        self.ser = serial.Serial(port='/dev/ttyUSB0',baudrate=256000,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)

    def run(self):    
        ## Write the 0x01 hex value to the sensor so it knows it can send EEPROM data
        self.ser.write(b'\x01')          
        while len(self.databuffer) < 832: ## TEMPORARY For now just for 0x01, when 0x02 is going to be read it is to be changed to be continuous
            read = self.ser.read(self.ser.inWaiting())
            ## Check whether there is data being read
            if read != b'':
                ## Upon receival, immediately extract the correct hex values
                for i in range(0, len(binascii.hexlify(read).decode()), 4):
                    self.databuffer.append(binascii.hexlify(read).decode()[i: i+4])
        ## TEMPORARY Close the connection after the 0x01 info is received
        self.ser.close()
    
    ## Get values for 0x01 instruction of MLX
    def getData(self):
        while len(self.databuffer) != 832:
            pass
        return self.databuffer

class Base():
    def __init__(self):
        ## Initialize a thread for receiving the data
        self.ser = recvData() 
        ## Run the data receival thread
        self.ser.start() 

    ## Check whether the devicedata is correct
    def _checkEEPROMValid(self, x1Data):
        deviceSelect = int(x1Data[10], 16) & 64
        if deviceSelect == 0:
            error = 0
        else:
            error = -7
        
        return error

    def main(self):
        ## Get the data to be used for the calibration restoration of the EEPROM data
        x1Data = self.ser.getData()
        print(x1Data)
        eepromData = cre.calibration_restoration_EEPROM(x1Data)
        error = self._checkEEPROMValid(x1Data)

        ## TEMPORARY Results of the calibration restoration of the EEPROM data (for checking whether the results are correct)
        if error == 0:
            print(eepromData.extractVDDParams())
            print(eepromData.extractPTATParams()) 
            print(eepromData.extractGainCoef()) 
            print(eepromData.extractTGCCoef()) 
            print(eepromData.extractResConCoef()) 
            print(eepromData.extractKsTaCoef())
            print(eepromData.extractKsToCoef())
            print(eepromData.extractCornerTemps())
            print(eepromData.extractPixSens())
            print(eepromData.extractPixOff()) 
            print(eepromData.extractKtaCoef())
            print(eepromData.extractKvCoef())
            print(eepromData.extractComPixSens())
            print(eepromData.extractComPixOff()) 
            print(eepromData.extractKvComPixCoef())
            print(eepromData.extractKtaComPixCoef())
            print(eepromData.extractChessCorrCoef())
            print(eepromData.extractDeviatingPix()) 

if __name__ == '__main__':
    b = Base() 
    b.main()