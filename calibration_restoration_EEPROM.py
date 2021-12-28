## Everything is rounded to integers, if any floating points are deemed necessary please make changes

class calibration_restoration_EEPROM:
    def __init__(self, mlxData):
        self._mlxData = mlxData
    
    def extractVDDParams(self):
        kVdd = (int(self._mlxData[51], 16) & 65280) >> 8
        if kVdd > 127:
            kVdd = kVdd - 256
        kVdd *= 32
        
        vdd25 = int(self._mlxData[51], 16) & 255
        vdd25 = (vdd25 - 256) * 32 - 8192

        return kVdd, vdd25

    def extractPTATParams(self):
        kVPTAT = (int(self._mlxData[50], 16) & 64512) >> 10
        if kVPTAT > 31: 
            kVPTAT -= 64
        kVPTAT >>= 12

        kTPTAT = int(self._mlxData[50], 16) & 1023
        if kTPTAT > 511:
            kTPTAT -= 1024
        kTPTAT >>= 3

        vPTAT25 = int(self._mlxData[49], 16)
        
        alphaPTAT = ((int(self._mlxData[16], 16) & 61440) >> 14) + 8

        return kVPTAT, kTPTAT, vPTAT25, alphaPTAT

    def extractGainCoef(self):
        gain = (int(self._mlxData[48], 16))
        if gain > 32767:
            gain -= 65536
        
        return gain

    def extractTGCCoef(self):
        tgc = (int(self._mlxData[60], 16) & 255)
        if tgc > 127:
            tgc -= 256
        tgc >>= 5

        return tgc

    def extractResConCoef(self):
        resolution = (int(self._mlxData[56], 16) & 12288) >> 12

        return resolution
    
    def extractKsTaCoef(self):
        ksTa = (int(self._mlxData[60], 16) & 65280) >> 8
        if ksTa > 127:
            ksTa -= 256
        ksTa >>= 13

        return ksTa

    def extractKsToCoef(self):
        ksToScale = (int(self._mlxData[63], 16) & 15) + 8

        ksTo = []
        ksTo.append(int(self._mlxData[61], 16) & 255)
        ksTo.append((int(self._mlxData[61], 16) & 65280) >> 8)
        ksTo.append(int(self._mlxData[62], 16) & 255)
        ksTo.append((int(self._mlxData[62], 16) & 255) >> 8)
        for i in range(4):
            if ksTo[i] > 127:
                ksTo[i] -= 256
            ksTo[i] >>= ksToScale

        return ksTo

    def extractCornerTemps(self):
        step = ((int(self._mlxData[63], 16) & 12288) >> 12) * 10

        ct = []
        ct.append(-40) # ct1
        ct.append(0) #ct2
        ct.append(((int(self._mlxData[63], 16) & 240) >> 4) * step) #ct3
        ct.append(((int(self._mlxData[63], 16) & 3840) >> 8) * step + ct[2]) #ct4

        return ct
    
    
