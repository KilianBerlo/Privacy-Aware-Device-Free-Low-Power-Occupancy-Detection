from struct import calcsize
import serial
import binascii
import calibration_restoration_EEPROM as cre
import temperature_calculation as tc

class Base():
    def __init__(self):
        ## The received data is put in a list
        self._dataEE = []  
        self._calData = {} 

        ## Configure the serial connection (the port might differ per machine)
        self.ser = serial.Serial(port='/dev/ttyUSB0',baudrate=256000,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
        ## Cleaning the buffers to make sure there is nothing in it
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()

    def read_EEPROM(self):
        self.ser.write(b'\x01')          
        read = self.ser.read(1664)
        ## Upon receival, immediately extract the correct hex values
        for i in range(0, len(binascii.hexlify(read).decode()), 4):
            self._dataEE.append(binascii.hexlify(read).decode()[i: i+4])
        ## Cleaning the buffers to make sure there is nothing in it
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()
        return self._dataEE

    def MLX90640_ExtractParameters(self, eepromData):
        ## Check whether the devicedata is correct
        deviceSelect = int(self._dataEE[10], 16) & 64
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
        # print(deviceParams)
        count = 0
        self.ser.write(b'\x02')
        while count < 30:
            _dataTemp = tc.temperature_calculation(self.ser, deviceParams).getPixData()
            print(_dataTemp)
            count += 1

if __name__ == '__main__':
    b = Base() 
    b.main()