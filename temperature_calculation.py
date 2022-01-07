import math as m
import struct

EMISSIVITY = 32
TA_SHIFT = 8

class temperature_calculation:
    def __init__(self, ser, deviceParams):
        self._pageData = []
        self._frameData = [0 for a in range(835)]
        self._tempData = []
        self._deviceParams = deviceParams
        self.ser = ser
        self._ADC = 0

    def getFrameData(self):
        self._pageData.clear()
        # read = self.ser.read(902)
        read = self.ser.read_until(b'\r\n')
        index = 384

        ## Upon receival, immediately extract the correct hex values
        for i in range(0, len(read) - 4, 2):
            self._pageData.append((struct.unpack('<H', read[i:i+2])[0])) 

        self._ADC = self._pageData[450]
        
        if self._pageData[449] == 0:
            for i in range(384):
                location = (i * 2) + (m.floor(i / 16) % 2)
                self._frameData[location] = self._pageData[i]
        else:
            for i in range(384):
                location = (i * 2) + 1 - (m.floor(i / 16) % 2)
                self._frameData[location] = self._pageData[i]
        for i in range(768, 835):
            self._frameData[i] = self._pageData[index]
            index += 1

    def getVDD(self):
        vdd = self._frameData[810]
        if vdd > 32767:
            vdd -= 65536

        resRAM = (self._frameData[832] & 3072) / 1024
        resCor = pow(2, self._deviceParams['resolutionEE']) / m.pow(2, resRAM)
        vdd = ((resCor * vdd - self._deviceParams['vdd25']) / self._deviceParams['kVdd']) + 3.3

        return vdd

    def getTa(self):
        vdd = self.getVDD()
        ptat = self._frameData[800]
        if ptat > 32767:
            ptat -= 65536

        ptatArt = self._frameData[768]
        if ptatArt > 32767:
            ptatArt -= 65536

        ptatArt += (ptat * self._deviceParams['alphaPTAT'])
        ptatArt = (ptat / ptatArt) * 262144

        ta = (ptatArt / (1 + self._deviceParams['kvPTAT'] * (vdd - 3.3))) - self._deviceParams['vPTAT25']
        ta = (ta / self._deviceParams['ktPTAT']) + 25

        return ta
    
    def getGain(self):
        gain = self._frameData[778]
        if gain > 32767:
            gain -= 65536
        
        gain = self._deviceParams['gainEE'] / gain

        return gain

    def getIRDataCP(self, gain, ta, vdd, mode): 
        ## Compensate the gain of the CP pixel
        irDataCP0 = self._frameData[776]
        if irDataCP0 > 32767:
            irDataCP0 -= 65536
        
        irDataCP1 = self._frameData[808]
        if irDataCP1 > 32767:
            irDataCP1 -= 65536
        
        irDataCP0 *= gain
        irDataCP1 *= gain

        ## Compensate the offset, Ta and VDD of the CP pixels
        irDataCP0 = irDataCP0 - self._deviceParams['cpOffset'][0] * (1 + self._deviceParams['cpKta'] * (ta - 25)) * (1 + self._deviceParams['cpKv'] * (vdd - 3.3))
        if mode == self._deviceParams['calibrationModeEE']:
            irDataCP1 = irDataCP1 - self._deviceParams['cpOffset'][1] * (1 + self._deviceParams['cpKta'] * (ta - 25)) * (1 + self._deviceParams['cpKv'] * (vdd - 3.3))
        else:
            irDataCP1 = irDataCP1 - (self._deviceParams['cpOffset'][1] + self._deviceParams['ilChessC'][0]) * (1 + self._deviceParams['cpKta'] * (ta - 25)) * (1 + self._deviceParams['cpKv'] * (vdd - 3.3))
        
        return [irDataCP0, irDataCP1]

    def getPixData(self):        
        for i in range(2):
            self.getFrameData()
            subPage = self._frameData[833]
            vdd = self.getVDD()
            ta = self.getTa()
            ## Reflected temperature based on the sensor ambient temperature
            tr = ta - TA_SHIFT
            taTr = m.pow((tr + 273.15), 4) - (m.pow((tr + 273.15), 4) - m.pow((ta + 273.15), 4)) / EMISSIVITY

            ## Sensitivity correction coefficients for each temperature range
            alphaCorrR = []
            alphaCorrR.append(1 / (1 + self._deviceParams['KsTo'][0] * 40))
            alphaCorrR.append(1)
            alphaCorrR.append(1 + self._deviceParams['KsTo'][2] * self._deviceParams['ct'][2])
            alphaCorrR.append(alphaCorrR[2] * (1 + self._deviceParams['KsTo'][3] * (self._deviceParams['ct'][3] - self._deviceParams['ct'][2])))

            gain = self.getGain()
            mode = (self._frameData[832] & 4096) / 32
            irDataCP = self.getIRDataCP(gain, ta, vdd, mode)
            
            for p in range(768):
                ilPattern = m.floor(p / 32) - m.floor(p / 64) * 2
                chessPattern = ilPattern ^ (p - (m.floor(p / 2)) * 2)
                conversionPattern = (m.floor((p + 2) / 4) - m.floor((p + 3) / 4) + m.floor((p + 1) / 4) - m.floor(p / 4)) * (1 - 2 * ilPattern)
                if mode == 0:
                    pattern = ilPattern
                else:
                    pattern = chessPattern    
                if pattern == subPage:
                    ## Calculate the gain compensation on each pixel
                    irData = self._frameData[p]
                    if irData > 32767:
                        irData -= 65536
                    irData = irData * gain

                    ## Calculate the IR data compensation with offset, VDD and Ta
                    irData = irData - self._deviceParams['offset'][p] * (1 + self._deviceParams['kta'][p] * (ta - 25)) * (1 + self._deviceParams['kv'][p] * (vdd - 3.3))

                    #irData = irData - app.structVar.offset(pixelNumber)*(1 + app.structVar.kta(pixelNumber)*(Ta - 25))*(1 + app.structVar.kv(pixelNumber)*(vdd - 3.3));

                    if not (mode == self._deviceParams['calibrationModeEE']):
                        irData = irData + self._deviceParams['ilChessC'][2] * (2 * ilPattern - 1) - self._deviceParams['ilChessC'][1] * conversionPattern
                    ## IR data emmisivity data compensation 
                    irData /= EMISSIVITY 
                    irData = irData - self._deviceParams['tgc'] * irDataCP[subPage] 
                    ## Normalizing to sensitivity
                    alphaCompensated = (self._deviceParams['alpha'][p] - self._deviceParams['tgc'] * self._deviceParams['cpAlpha'][subPage]) * (1 + self._deviceParams['KsTa'] * (ta - 25))
                    
                    sx = m.pow(alphaCompensated, 3) * (irData + alphaCompensated * taTr)
                    sx = self._deviceParams['KsTo'][1] * m.sqrt(m.sqrt(sx))
                    to = m.sqrt(irData / (alphaCompensated * (1 - self._deviceParams['KsTo'][1] * 273.15) + sx) + taTr)
                    to = m.sqrt(to) - 273.15
                    ## Determine the range we are in
                    if to < self._deviceParams['ct'][1]:
                        r = 0
                    elif to < self._deviceParams['ct'][2]:
                        r = 1
                    elif to < self._deviceParams['ct'][3]:
                        r = 2
                    else:
                        r = 3

                    ## Extended To range calculation
                    to = m.sqrt(m.sqrt(irData / (alphaCompensated * alphaCorrR[r] * (1 + self._deviceParams['KsTo'][r] * (to - self._deviceParams['ct'][r]))) + taTr)) - 273.15
                    self._tempData.append(to)
        
        return self._tempData