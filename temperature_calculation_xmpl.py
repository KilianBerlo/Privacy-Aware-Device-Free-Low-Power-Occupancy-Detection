import math as m
import numpy as np

EMISSIVITY = 0.95
TA_SHIFT = 8

class temperature_calculation_xmpl:
    def __init__(self, deviceParams):
        self._pageData = np.empty(451)
        self._frameData = np.zeros(835)
        self._tempData = np.zeros(768)
        self._deviceParams = deviceParams
        self._ADC = 0

    def getFrameData(self, nr):
        page0 = np.array([65429, 65401, 65383, 65380, 65364, 65363, 65353, 65356, 65355, 65356, 65352, 65360, 65363, 65371, 65375, 65406, 65397, 65377, 65355, 65356, 65345, 65339, 65330, 65334, 65334, 65335, 65326, 65337, 65333, 65351, 65353, 65379, 65405, 65387, 65371, 65365, 65360, 65351, 65343, 65344, 65381, 65350, 65338, 65345, 65348, 65355, 65364, 65381, 65380, 65371, 65352, 65345, 65327, 65330, 65317, 65327, 65364, 65328, 65315, 65320, 65321, 65335, 65342, 65352, 65398, 65385, 65364, 65360, 65347, 65339, 65329, 65342, 65391, 65355, 65331, 65330, 65337, 65348, 65358, 65371, 65370, 65361, 65341, 65339, 65317, 65313, 65309, 65346, 65355, 65335, 65302, 65309, 65311, 65329, 65337, 65342, 65385, 65372, 65358, 65348, 65332, 65324, 65312, 65371, 65365, 65370, 65320, 65322, 65333, 65348, 65353, 65366, 65364, 65350, 65331, 65325, 65304, 65303, 65290, 65356, 65332, 65353, 65295, 65301, 65306, 65322, 65324, 65336, 65381, 65366, 65352, 65337, 65325, 65316, 65305, 65366, 65354, 65367, 65315, 65315, 65334, 65338, 65346, 65360, 65355, 65345, 65322, 65316, 65299, 65290, 65287, 65351, 65330, 65342, 65283, 65292, 65299, 65316, 65322, 65331, 65382, 65365, 65347, 65336, 65322, 65308, 65302, 65340, 65366, 65372, 65306, 65309, 65318, 65332, 65341, 65359, 65356, 65342, 65320, 65313, 65292, 65287, 65277, 65353, 65337, 65316, 65281, 65287, 65290, 65309, 65322, 65335, 65377, 65366, 65344, 65338, 65322, 65306, 65298, 65319, 65360, 65338, 65301, 65305, 65318, 65337, 65346, 65362, 65353, 65342, 65318, 65310, 65296, 65286, 65273, 65316, 65333, 65289, 65274, 65291, 65295, 65315, 65320, 65333, 65369, 65362, 65343, 65331, 65323, 65314, 65306, 65310, 65339, 65317, 65294, 65314, 65321, 65337, 65348, 65366, 65349, 65336, 65315, 65309, 65297, 65294, 65282, 65299, 65308, 65283, 65278, 65302, 65308, 65320, 65326, 65337, 65373, 65366, 65351, 65342, 65339, 65323, 65317, 65318, 65331, 65333, 65328, 65338, 65347, 65351, 65358, 65369, 65350, 65344, 65329, 65326, 65306, 65295, 65285, 65304, 65297, 65309, 65295, 65308, 65316, 65334, 65334, 65343, 65367, 65363, 65345, 65336, 65326, 65316, 65311, 65312, 65317, 65318, 65316, 65321, 65336, 65345, 65354, 65369, 65345, 65338, 65321, 65318, 65299, 65297, 65285, 65293, 65287, 65292, 65288, 65303, 65304, 65320, 65329, 65340, 65365, 65360, 65348, 65337, 65327, 65322, 65313, 65312, 65317, 65319, 65321, 65328, 65333, 65342, 65354, 65369, 65345, 65341, 65320, 65315, 65303, 65295, 65290, 65292, 65293, 65295, 65290, 65305, 65308, 65324, 65331, 65343, 65367, 65364, 65351, 65346, 65334, 65326, 65322, 65320, 65320, 65322, 65326, 65333, 65336, 65346, 65354, 65365, 65340, 65333, 65321, 65315, 65301, 65296, 65289, 65292, 65284, 65295, 65289, 65300, 65307, 65318, 65323, 65336, 19347, 6605, 32767, 6605, 32767, 6604, 32767, 6604, 65445, 52901, 5960, 55241, 65525, 6, 0, 0, 6791, 1047, 636, 32767, 6791, 1048, 636, 32767, 3, 3, 3, 3, 3, 3, 3, 3, 1651, 32767, 6605, 32767, 6605, 32767, 6604, 32767, 65449, 62778, 53341, 55138, 4, 65531, 65534, 0, 252, 65, 10493, 62, 253, 65, 10493, 62, 3, 3, 3, 3, 3, 3, 3, 3, 6529, 0, 25782])
        page1 = np.array([65420, 65384, 65371, 65367, 65357, 65345, 65340, 65333, 65343, 65337, 65340, 65342, 65346, 65355, 65362, 65389, 65410, 65375, 65368, 65354, 65349, 65338, 65338, 65333, 65344, 65334, 65335, 65338, 65352, 65349, 65363, 65376, 65394, 65376, 65364, 65351, 65342, 65335, 65331, 65330, 65353, 65329, 65325, 65327, 65331, 65338, 65350, 65355, 65387, 65368, 65358, 65346, 65345, 65325, 65327, 65320, 65370, 65328, 65325, 65321, 65336, 65338, 65353, 65362, 65388, 65369, 65353, 65343, 65332, 65321, 65319, 65327, 65374, 65322, 65312, 65310, 65322, 65333, 65345, 65345, 65383, 65357, 65350, 65334, 65332, 65316, 65313, 65323, 65372, 65341, 65319, 65310, 65323, 65330, 65350, 65353, 65377, 65357, 65348, 65330, 65320, 65310, 65307, 65356, 65348, 65342, 65306, 65307, 65319, 65327, 65337, 65343, 65372, 65345, 65343, 65324, 65316, 65299, 65297, 65344, 65349, 65351, 65307, 65299, 65322, 65325, 65342, 65346, 65373, 65352, 65338, 65323, 65317, 65302, 65303, 65356, 65337, 65348, 65301, 65297, 65311, 65318, 65336, 65335, 65365, 65342, 65335, 65309, 65308, 65289, 65292, 65334, 65343, 65341, 65299, 65293, 65320, 65317, 65338, 65337, 65373, 65350, 65337, 65322, 65309, 65298, 65294, 65355, 65344, 65344, 65295, 65292, 65310, 65314, 65336, 65335, 65365, 65337, 65330, 65311, 65306, 65284, 65286, 65317, 65354, 65346, 65293, 65288, 65303, 65311, 65332, 65339, 65370, 65352, 65337, 65325, 65312, 65297, 65289, 65326, 65358, 65300, 65289, 65297, 65308, 65318, 65334, 65340, 65359, 65341, 65331, 65311, 65306, 65282, 65284, 65286, 65342, 65306, 65286, 65286, 65307, 65311, 65333, 65344, 65370, 65347, 65334, 65319, 65308, 65296, 65296, 65305, 65327, 65291, 65291, 65300, 65314, 65322, 65337, 65341, 65354, 65333, 65326, 65306, 65306, 65290, 65292, 65282, 65317, 65288, 65285, 65297, 65317, 65318, 65337, 65347, 65372, 65354, 65343, 65334, 65324, 65316, 65309, 65312, 65319, 65320, 65316, 65325, 65335, 65339, 65348, 65348, 65350, 65336, 65337, 65313, 65324, 65295, 65296, 65293, 65310, 65307, 65310, 65305, 65324, 65326, 65347, 65350, 65369, 65351, 65344, 65329, 65319, 65309, 65303, 65303, 65304, 65302, 65306, 65312, 65325, 65329, 65349, 65347, 65345, 65334, 65326, 65307, 65310, 65286, 65294, 65282, 65297, 65291, 65298, 65297, 65319, 65321, 65339, 65343, 65373, 65354, 65344, 65330, 65325, 65308, 65309, 65303, 65310, 65304, 65310, 65312, 65329, 65333, 65347, 65352, 65342, 65330, 65326, 65308, 65308, 65292, 65297, 65285, 65297, 65291, 65309, 65300, 65316, 65316, 65339, 65346, 65376, 65359, 65353, 65338, 65333, 65319, 65319, 65309, 65315, 65313, 65318, 65324, 65331, 65336, 65350, 65354, 65336, 65320, 65317, 65308, 65304, 65290, 65294, 65284, 65289, 65286, 65300, 65300, 65310, 65313, 65332, 65336, 19347, 6606, 32767, 6606, 32767, 6604, 32767, 6604, 65445, 52903, 5960, 55237, 65525, 7, 0, 65534, 6791, 1047, 636, 32767, 6791, 1047, 636, 32767, 3, 3, 3, 3, 3, 3, 3, 3, 1651, 32767, 6606, 32767, 6606, 32767, 6604, 32767, 65446, 62778, 53341, 55138, 3, 65531, 65532, 0, 255, 65, 10493, 62, 255, 65, 10493, 62, 3, 3, 3, 3, 3, 3, 3, 3, 6529, 1, 25622])
        if nr == 0:
            self._pageData = page0
        if nr == 1:
            self._pageData = page1
        index = 384

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
        
        self._frameData = self._frameData.astype(int)

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
        ta = ptatArt / (1 + self._deviceParams['kvPTAT'] * (vdd - 3.3)) - self._deviceParams['vPTAT25']
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
            self.getFrameData(i)

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
                    self._tempData[p] = to
        
        return self._tempData