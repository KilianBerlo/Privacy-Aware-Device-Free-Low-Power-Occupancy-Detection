import math as m

EMISSIVITY = 32

class pixel_value_calculation:
    def __init__(self, pageData, frameData, deviceParams):
        self._pageData = pageData
        self._frameData = frameData
        self._deviceParams = deviceParams
       
#     def extractADCValue(self):
#         return int(self._pageData[450], 16)

#     def getFrameData(self):
#         index = 384
#         if self._pageData[449] == 0:
#             for i in range(384):
#                 location = ((i - 1) * 2) + 1 + (m.floor((i - 1) / 16) % 2)
#                 self._frameData[location] = self._pageData[i]
#         else:
#             for i in range(384):
#                 location = ((i - 1) * 2) + 2 - (m.floor((i - 1) / 16) % 2)
#                 self._frameData[location] = self._pageData[i]
#         for i in range(767, 835):
#             self._frameData[i] = self._pageData[index]
#             index += 1

#         return self._frameData

    
### NOT YET TESTED GIVEN UNKNOWN FRAME DATA EXTRACTION ###

    def getVDD(self):
        vdd = self._frameData[810]
        if vdd > 32767:
            vdd -= 65536

        resRAM = (int(self._frameData[832], 16) & 3072) / pow(2,10)
        resCor = pow(2, self._deviceParams['calibrationModeEE']) / pow(2, resRAM)
        vdd = ((resCor * vdd - self._deviceParams['vdd25']) / self._deviceParams['kVdd']) + 3.3

        return vdd

    def getTa(self):
        vdd = self.getVDD
        ptat = self._frameData[800]
        if ptat > 32767:
            ptat -= 65536

        ptatArt = self._frameData[768]
        if ptatArt > 32767:
            ptatArt -= 65536

        ptatArt += (ptat * self._deviceParams['alphaPTAT'])
        ptatArt = (ptat / ptatArt) * pow(2, 18)

        ta = (ptatArt / (1 + self._deviceParams['kvPTAT'] * (vdd - 3.3))) - self._deviceParams['vPTAT25']
        ta = (ta / self._deviceParams['ktPTAT']) + 25

        return ta
    
    def getGain(self):
        gain = self._frameData(778)
        if gain > 32767:
            gain -= 65536
        
        gain = self._deviceParams['gainEE'] / gain

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
        subPage = self._frameData[833]
        vdd = self.getVDD()
        ta = self.getTa()
        gain = self.getGain()
        mode = (int(self._frameData[832], 16) & 4096) / pow(2,5)
        irDataCP = self.getIRDataCP(gain, ta, vdd, mode)

        for p in range(768):
            ilPattern = m.floor((p - 1) / 32) - m.floor((p - 1) / 64) * 2
            chessPattern = ilPattern ^ ((p - 1) - (m.floor((p - 1) / 2)) * 2)
            conversionPattern = (m.floor(((p - 1) + 2) / 4) - m.floor(((p - 1) + 3) / 4) + m.floor(((p - 1) + 1) / 4) - m.floor((p - 1) / 4)) * (1 - 2 * ilPattern)
            if mode == 0:
                pattern = ilPattern
            else:
                pattern = chessPattern
            if pattern == self._frameData[833]:
                ## Calculate the gain compensation on each pixel
                irData = self._frameData[p]
                if irData > 32767:
                    irData -= 65536
                
                irData = irData * gain

                ## Calculate the IR data compensation with offset, VDD and Ta
                irData = irData - self._deviceParams['offset'][p] * (1 + self._deviceParams['kta'][p] * (ta - 25)) * (1 + self._deviceParams['kv'][p] * (vdd - 3.3))
                if not (mode == self._deviceParams['calibrationModeEE']):
                    irData = irData + self._deviceParams['ilChessC'][2] * (2 * ilPattern - 1) - self._deviceParams['ilChessC'][1] * conversionPattern
                
                ## IR data emmisivity data compensation
                irData /= EMISSIVITY
                irData = irData - self._deviceParams['tgc'] * irDataCP[subPage]

                ## Normalizing to sensitivity
                alphaCompensated = (self._deviceParams['alpha'][p] - self._deviceParams['tgc'] * self._deviceParams['cpAlpha'][subPage]) * (1 + self._deviceParams['KsTa'] * (ta - 25))
                
                ############## TODO: In the matlab code alphaCompensated isn't raised to the power of 4 here, but in the datasheet it is, what should I do? ###################
                sx = pow(alphaCompensated, 3) * irData + pow(alphaCompensated, 4) ##???