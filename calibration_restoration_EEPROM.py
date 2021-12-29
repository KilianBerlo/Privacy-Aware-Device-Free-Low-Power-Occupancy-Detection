## Everything is rounded to integers, if any floating points are deemed necessary please make changes
ROWS = 24
COLS = 32

class calibration_restoration_EEPROM:
    def __init__(self, mlxData):
        self._mlxData = mlxData
    
    def extractVDDParams(self):
        kVdd = (int(self._mlxData[51], 16) & 65280) / pow(2,8)
        if kVdd > 127:
            kVdd = kVdd - 256
        kVdd *= 32
        
        vdd25 = int(self._mlxData[51], 16) & 255
        vdd25 = (vdd25 - 256) * 32 - 8192

        return kVdd, vdd25

    def extractPTATParams(self):
        kVPTAT = (int(self._mlxData[50], 16) & 64512) / pow(2,10)
        if kVPTAT > 31: 
            kVPTAT -= 64
        kVPTAT /= pow(2,12)

        kTPTAT = int(self._mlxData[50], 16) & 1023
        if kTPTAT > 511:
            kTPTAT -= 1024
        kTPTAT >>= 3

        vPTAT25 = int(self._mlxData[49], 16)
        
        alphaPTAT = ((int(self._mlxData[16], 16) & 61440) / pow(2,14)) + 8

        return kVPTAT, kTPTAT, vPTAT25, alphaPTAT

    def extractGainCoef(self):
        gain = (int(self._mlxData[48], 16))
        if gain > 32767:
            gain -= 65536
        
        return gain

    def extractTGCCoef(self):
        tgc = int(self._mlxData[60], 16) & 255
        if tgc > 127:
            tgc -= 256
        tgc >>= 5

        return tgc

    def extractResConCoef(self):
        resolution = (int(self._mlxData[56], 16) & 12288) / pow(2,12)

        return resolution
    
    def extractKsTaCoef(self):
        ksTa = (int(self._mlxData[60], 16) & 65280) / pow(2,8)
        if ksTa > 127:
            ksTa -= 256
        ksTa /= pow(2,13)

        return ksTa

    def extractKsToCoef(self):
        ksToScale = (int(self._mlxData[63], 16) & 15) + 8

        ksTo = []
        ksTo.append(int(self._mlxData[61], 16) & 255)
        ksTo.append((int(self._mlxData[61], 16) & 65280) / pow(2,8))
        ksTo.append(int(self._mlxData[62], 16) & 255)
        ksTo.append((int(self._mlxData[62], 16) & 255) / pow(2,8))
        for i in range(4):
            if ksTo[i] > 127:
                ksTo[i] -= 256
            ksTo[i] /= pow(2,ksToScale)
        return ksTo

    def extractCornerTemps(self):
        step = ((int(self._mlxData[63], 16) & 12288) / pow(2,12)) * 10

        ct = []
        ct.append(-40) # ct1
        ct.append(0) #ct2
        ct.append(((int(self._mlxData[63], 16) & 240) / pow(2,4)) * step) #ct3
        ct.append(((int(self._mlxData[63], 16) & 3840) / pow(2,8)) * step + ct[2]) #ct4

        return ct
    
    def extractPixSens(self):
        aRef = int(self._mlxData[33], 16)
        aScale = ((int(self._mlxData[32], 16) & 61440) / pow(2,12)) + 30
        accScaleRow = (int(self._mlxData[32], 16) & 3840) / pow(2,8)
        accScaleCol = (int(self._mlxData[32], 16) & 240) / pow(2,4)
        accScaleRem = int(self._mlxData[32], 16) & 15

        accRow = []
        for i in range(ROWS>>2): # Range from 0 to 5 since six EEPROM words contain all the data about the bit values of each ACCrow (table 9 and 10 from datasheet)
            accRow.append(int(self._mlxData[34 + i], 16) & 15)
            accRow.append((int(self._mlxData[34 + i], 16) & 240) / pow(2,4))
            accRow.append((int(self._mlxData[34 + i], 16) & 3840) / pow(2,8))
            accRow.append((int(self._mlxData[34 + i], 16) & 61440) / pow(2,12))
        for i in range(ROWS):
            if accRow[i] > 7:
                accRow[i] -= 16
        
        accCol = []
        for j in range(COLS>>2): # Range from 0 to 7 since eight EEPROM words contain all the data about the bit values of each ACCrow (table 9 and 10 from datasheet)
            accCol.append(int(self._mlxData[40 + j], 16) & 15)
            accCol.append((int(self._mlxData[40 + j], 16) & 240) / pow(2,4))
            accCol.append((int(self._mlxData[40 + j], 16) & 3840) / pow(2,8))
            accCol.append((int(self._mlxData[40 + j], 16) & 61440) / pow(2,12))
        for j in range(COLS):
            if accCol[j] > 7:
                accCol[j] -= 16

        alpha = [] # Calculate the sensitivity for each pixel in the IR array
        for i in range(ROWS):
            for j in range(COLS):
                l = 32 * i + j
                alpha.append((int(self._mlxData[64 + l], 16) & 1008) / pow(2,4))
                if alpha[l] > 31:
                    alpha[l] -= 64
                alpha[l] = (aRef + (accRow[i] * pow(2,accScaleRow)) + (accCol[j] * pow(2,accScaleCol)) + (alpha[l] * pow(2,accScaleRem))) / pow(2,aScale)

        return alpha

    def extractPixOff(self):
        oavg = int(self._mlxData[17], 16)
        if oavg > 32767:
            oavg -= 65536
        occScaleRow = (int(self._mlxData[16], 16) & 3840) / pow(2,8)
        occScaleCol = (int(self._mlxData[16], 16) & 240) / pow(2,4)
        occScaleRem = int(self._mlxData[16], 16) & 15

        occRow = []
        for i in range(ROWS>>2): # Range from 0 to 5 since six EEPROM words contain all the data about the bit values of each ACCrow (table 9 and 10 from datasheet)
            occRow.append(int(self._mlxData[18 + i], 16) & 15)
            occRow.append((int(self._mlxData[18 + i], 16) & 240) / pow(2,4))
            occRow.append((int(self._mlxData[18 + i], 16) & 3840) / pow(2,8))
            occRow.append((int(self._mlxData[18 + i], 16) & 61440) / pow(2,12))
        for i in range(ROWS):
            if occRow[i] > 7:
                occRow[i] -= 16

        occCol = []
        for j in range(COLS>>2): # Range from 0 to 7 since eight EEPROM words contain all the data about the bit values of each ACCrow (table 9 and 10 from datasheet)
            occCol.append(int(self._mlxData[24 + j], 16) & 15)
            occCol.append((int(self._mlxData[24 + j], 16) & 240) / pow(2,4))
            occCol.append((int(self._mlxData[24 + j], 16) & 3840) / pow(2,8))
            occCol.append((int(self._mlxData[24 + j], 16) & 61440) / pow(2,12))
        for j in range(COLS):
            if occCol[j] > 7:
                occCol[j] -= 16

        offset = [] # Calculate the sensitivity for each pixel in the IR array
        for i in range(ROWS):
            for j in range(COLS):
                l = 32 * i + j
                offset.append((int(self._mlxData[64 + l], 16) & 64512) / pow(2,10))
                if offset[l] > 31:
                    offset[l] -= 64
                offset[l] = oavg + (occRow[i] * pow(2, occScaleRow)) + (occCol[j] * pow(2, occScaleCol)) + (offset[l] * pow(2, occScaleRem))

        return offset

    def extractKtaCoef(self):
        pass

    def extractKvCoef(self):
        pass