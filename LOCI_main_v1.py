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
        # while len(self._x1Data) < 832: ## TEMPORARY For now just for 0x01, when 0x02 is going to be read it is to be changed to be continuous
        read = self.ser.read(1664)
        ## Check whether there is data being read
        ## Upon receival, immediately extract the correct hex values
        for i in range(0, len(binascii.hexlify(read).decode()), 4):
            self._x1Data.append(binascii.hexlify(read).decode()[i: i+4])
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()
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

        ###################################################
        ### TEST PHASE, NOT YET GETTING DESIRED OUTCOME ###
        ###################################################
        counting = 0
        self.ser.write(b'\x02')
        while(counting < 20):
            read = self.ser.read(903)
            ## Upon receival, immediately extract the correct hex values
            for i in range(2, len(binascii.hexlify(read).decode()), 4):
                self._x2Data.append(binascii.hexlify(read).decode()[i: i+4])
        #     self._frameData = tc.pixel_value_calculation(self._x2Data, self._frameData, deviceParams).getFrameData()
            # print(self._x2Data)
            self._x2Data.clear()
            counting+=1
        # print(test)
        # print(test1)
        # print(deviceParams)

if __name__ == '__main__':
    b = Base() 
    b.main()