import serial
import binascii
import calibration_restoration_EEPROM as cre
import temperature_calculation as tc

class Base():
    def __init__(self):
        ## The received data is put in a list
        self._x1Data = [] 
        self._x2Data = [] 
        self._calData = {} 
        self._frameData = [0 for a in range(835)] ## frame data is double the page data since two times page data is analysed to complete one (both subpages)

        ## Configure the serial connection (the port might differ per machine)
        self.ser = serial.Serial(port='/dev/ttyUSB0',baudrate=256000,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)

    def read_EEPROM(self):
        self.ser.write(b'\x01')          
        while len(self._x1Data) < 832: ## TEMPORARY For now just for 0x01, when 0x02 is going to be read it is to be changed to be continuous
            read = self.ser.read(self.ser.inWaiting())
            ## Check whether there is data being read
            if read != b'':
                ## Upon receival, immediately extract the correct hex values
                for i in range(0, len(binascii.hexlify(read).decode()), 4):
                    self._x1Data.append(binascii.hexlify(read).decode()[i: i+4])
        return self._x1Data

    def MLX90640_ExtractParameters(self, eepromData):
        ## Check whether the devicedata is correct
        deviceSelect = int(self._x1Data[10], 16) & 64
        if deviceSelect == 0:
            error = 0
        else:
            error = -7

        ## Results of the calibration restoration of the EEPROM data
        if error == 0:
            self._calData['kVdd'], self._calData['vdd25'] = eepromData.extractVDDParams()
            self._calData['kvPTAT'], self._calData['ktPTAT'], self._calData['vPTAT25'], self._calData['alphaPTAT'] = eepromData.extractPTATParams()
            self._calData['gainEE'] = eepromData.extractGainCoef()
            self._calData['tgc'] = eepromData.extractTGCCoef()
            self._calData['resolutionEE'] = eepromData.extractResConCoef()
            self._calData['KsTa'] = eepromData.extractKsTaCoef()
            self._calData['KsTo'] = eepromData.extractKsToCoef()
            self._calData['ct'] = eepromData.extractCornerTemps()
            self._calData['alpha'] = eepromData.extractPixSens()
            self._calData['offset'] = eepromData.extractPixOff()
            self._calData['kta'] = eepromData.extractKtaCoef()
            self._calData['kv'] = eepromData.extractKvCoef()
            self._calData['cpAlpha'] = eepromData.extractComPixSens()
            self._calData['cpOffset'] = eepromData.extractComPixOff()
            self._calData['cpKv'] = eepromData.extractKvComPixCoef()
            self._calData['cpKta'] = eepromData.extractKtaComPixCoef()
            self._calData['calibrationModeEE'] = eepromData.extractCalMode()
            self._calData['ilChessC'] = eepromData.extractChessCorrCoef()
            dev_val = eepromData.extractDeviatingPix()
            self._calData['brokenPixels'] = dev_val[0]
            self._calData['outlierPixels'] = dev_val[1]
            self._calData['warning'] = dev_val[2]
            return self._calData
        else:
            return 1

    def main(self):   
        deviceParams = self.MLX90640_ExtractParameters(cre.calibration_restoration_EEPROM(self.read_EEPROM()))
        ### TODO: In the main.c file it looks like the data is already ordered in the right pixel format (so after one another and not chess), is this correct or should it still be done here as well?
        # self.ser.write(b'\x02')
        # counting = 0
        # while(counting < 2):
        #     while len(self._x2Data) < 451:
        #         read = self.ser.read(self.ser.inWaiting())
        #         ## Check whether there is data being read
        #         if read != b'':
        #             ## Upon receival, immediately extract the correct hex values
        #             for i in range(0, len(binascii.hexlify(read).decode()), 4):
        #                 self._x2Data.append(binascii.hexlify(read).decode()[i: i+4])
        #     self._frameData = tc.pixel_value_calculation(self._x2Data, self._frameData, deviceParams).getFrameData()
        #     self._x2Data.clear()
        #     print(self._frameData)
        #     counting+=1
        print(deviceParams)
        
            # print(self._frameData)
#         ## DO calculations on the 902 bytes of data 
#         ## Collect the next 902 bytes of data
#         ## Keep doing this process till the connection has to be closed


if __name__ == '__main__':
    b = Base() 
    b.main()