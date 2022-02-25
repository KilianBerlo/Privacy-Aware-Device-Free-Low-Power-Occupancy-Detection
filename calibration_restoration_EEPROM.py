## Almost all parameters are extracted according to the instructions in chapter 11 of the MLX90640-Datasheet-Melexis: 
## https://www.mouser.com/datasheet/2/734/MLX90640-Datasheet-Melexis-1324357.pdf

import math as m

class calibration_restoration_EEPROM:
    """
    Class that restores the calibration data of the EEPROM to usable values
    """
    def __init__(self, mlxData, rows, cols):
        """
        Constructor for the class restoring the calibration data of the EEPROM to usable values
        
        Parameters:
            mlxData (np.array): Uncalibrated EEPROM Hex data obtained in the read_EEPROM() function of the Base() class
            rows (int): The number of rows of a frame from the sensor
            cols (int): The number of collumns of a frame from the sensor
        """        
        self._mlxData = mlxData
        self._rows = rows
        self._cols = cols
    

    def extractVDDParams(self):
        """
        Function to calculate the VDD parameters of the sensor
        
        Returns:
            kVdd (float): Kvdd parameter
            vdd25 (int): VDD25 parameter
        """  
        kVdd = (self._mlxData[51] & 65280) / 256
        if kVdd > 127:
            kVdd = kVdd - 256
        kVdd *= 32
        
        vdd25 = self._mlxData[51] & 255
        vdd25 = (vdd25 - 256) * 32 - 8192

        return kVdd, vdd25


    def extractPTATParams(self):
        """
        Function to calculate the PTAT (Proportional To Absolute Temperature) parameters of the sensor
        
        Returns:
            kVPTAT (float): kVPTAT parameter
            kTPTAT (float): kTPTAT parameter
            vPTAT25 (int): vPTAT25 parameter
            alphaPTAT (float): alphaPTAT parameter
        """  
        kVPTAT = (self._mlxData[50] & 64512) / 1024
        if kVPTAT > 31: 
            kVPTAT -= 64
        kVPTAT /= 4096

        kTPTAT = self._mlxData[50] & 1023
        if kTPTAT > 511:
            kTPTAT -= 1024
        kTPTAT /= 8

        vPTAT25 = self._mlxData[49]
        
        alphaPTAT = ((self._mlxData[16] & 61440) / 16384) + 8

        return kVPTAT, kTPTAT, vPTAT25, alphaPTAT


    def extractGainCoef(self):
        """
        Function to calculate the gain coefficient of the sensor
        
        Returns:
            gain (int): gain coefficient
        """  
        gain = (self._mlxData[48])
        if gain > 32767:
            gain -= 65536
        
        return gain


    def extractTGCCoef(self):
        """
        Function to calculate the TGC coefficient of the sensor
        
        Returns:
            tgc (float): TGC coefficient
        """  
        tgc = self._mlxData[60] & 255
        if tgc > 127:
            tgc -= 256
        tgc /= 32

        return tgc


    def extractResConCoef(self):
        """
        Function to calculate the resolution control coefficient of the sensor
        
        Returns:
            resolution (float): resolution control coefficient
        """  
        resolution = (self._mlxData[56] & 12288) / 4096

        return resolution
    

    def extractKsTaCoef(self):
        """
        Function to calculate the KsTa coefficient of the sensor
        
        Returns:
            ksTa (float): KsTa coefficient
        """  
        ksTa = (self._mlxData[60] & 65280) / 256
        if ksTa > 127:
            ksTa -= 256
        ksTa /= 8192

        return ksTa


    def extractKsToCoef(self):
        """
        Function to calculate the KsTo coefficient of the sensor
        
        Returns:
            ksTo (list): List of the KsTo coeffiecients needed for the sensitivity correction for each temperature range
        """  
        ksToScale = (self._mlxData[63] & 15) + 8

        ksTo = []
        ksTo.append(self._mlxData[61] & 255)
        ksTo.append((self._mlxData[61] & 65280) / 256)
        ksTo.append(self._mlxData[62] & 255)
        ksTo.append((self._mlxData[62] & 65280) / 256)

        for i in range(4):
            if ksTo[i] > 127:
                ksTo[i] -= 256
            ksTo[i] /= pow(2, ksToScale)
            
        return ksTo


    def extractCornerTemps(self):
        """
        Function to calculate the corner temperatures of the frame of the sensor
        
        Returns:
            ct (list): List of the corner temperature values of each pixel
        """  
        step = ((self._mlxData[63] & 12288) / 4096) * 10

        ct = []
        ct.append(-40) ## corner 1 temperature
        ct.append(0) ## corner 2 temperature
        ct.append(((self._mlxData[63] & 240) / 16) * step) ## corner 3 temperature
        ct.append(((self._mlxData[63] & 3840) / 256) * step + ct[2]) ## corner 4 temperature

        return ct
    

    def extractPixSens(self):
        """
        Function to calculate the sensitivity (alpha) of each pixel in the frame of the sensor
        
        Returns:
            alpha (list): List of the sensitivity value of each pixel
        """  
        aRef = self._mlxData[33]
        aScale = ((self._mlxData[32] & 61440) / 4096) + 30
        accScaleRow = (self._mlxData[32] & 3840) / 256
        accScaleCol = (self._mlxData[32] & 240) / 16
        accScaleRem = self._mlxData[32] & 15

        accRow = []
        ## Range from 0 to 5 since six EEPROM words contain all the data about the bit values of each ACCrow (table 9 and 10 from datasheet)
        for i in range(self._rows>>2): 
            accRow.append(self._mlxData[34 + i] & 15)
            accRow.append((self._mlxData[34 + i] & 240) / 16)
            accRow.append((self._mlxData[34 + i] & 3840) / 256)
            accRow.append((self._mlxData[34 + i] & 61440) / 4096)
        for i in range(self._rows):
            if accRow[i] > 7:
                accRow[i] -= 16

        accCol = []
        ## Range from 0 to 7 since eight EEPROM words contain all the data about the bit values of each ACCrow (table 9 and 10 from datasheet)
        for j in range(self._cols>>2): 
            accCol.append(self._mlxData[40 + j] & 15)
            accCol.append((self._mlxData[40 + j] & 240) / 16)
            accCol.append((self._mlxData[40 + j] & 3840) / 256)
            accCol.append((self._mlxData[40 + j] & 61440) / 4096)
        for j in range(self._cols):
            if accCol[j] > 7:
                accCol[j] -= 16

        alpha = [] 
        for i in range(self._rows):
            for j in range(self._cols):
                l = 32 * i + j
                alpha.append((self._mlxData[64 + l] & 1008) / 16)
                if alpha[l] > 31:
                    alpha[l] -= 64
                alpha[l] = (aRef + (accRow[i] * pow(2, accScaleRow)) + (accCol[j] * pow(2, accScaleCol)) + (alpha[l] * pow(2, accScaleRem))) / pow(2, aScale)

        return alpha
 

    def extractPixOff(self):
        """
        Function to calculate the offset of each pixel in the frame of the sensor
        
        Returns:
            offset (list): List of the offset value of each pixel
        """  
        oavg = self._mlxData[17]
        if oavg > 32767:
            oavg -= 65536
        occScaleRow = (self._mlxData[16] & 3840) / 256
        occScaleCol = (self._mlxData[16] & 240) / 16
        occScaleRem = self._mlxData[16] & 15

        occRow = []
        ## Range from 0 to 5 since six EEPROM words contain all the data about the bit values of each ACCrow (table 9 and 10 from datasheet)
        for i in range(self._rows>>2): 
            occRow.append(self._mlxData[18 + i] & 15)
            occRow.append((self._mlxData[18 + i] & 240) / 16)
            occRow.append((self._mlxData[18 + i] & 3840) / 256)
            occRow.append((self._mlxData[18 + i] & 61440) / 4096)
        for i in range(self._rows):
            if occRow[i] > 7:
                occRow[i] -= 16

        occCol = []
        ## Range from 0 to 7 since eight EEPROM words contain all the data about the bit values of each ACCrow (table 9 and 10 from datasheet)
        for j in range(self._cols>>2): 
            occCol.append(self._mlxData[24 + j] & 15)
            occCol.append((self._mlxData[24 + j] & 240) / 16)
            occCol.append((self._mlxData[24 + j] & 3840) / 256)
            occCol.append((self._mlxData[24 + j] & 61440) / 4096)
        for j in range(self._cols):
            if occCol[j] > 7:
                occCol[j] -= 16

        offset = []
        for i in range(self._rows):
            for j in range(self._cols):
                l = self._cols * i + j
                offset.append((self._mlxData[64 + l] & 64512) / 1024)
                if offset[l] > 31:
                    offset[l] -= 64
                offset[l] = oavg + (occRow[i] * pow(2, occScaleRow)) + (occCol[j] * pow(2, occScaleCol)) + (offset[l] * pow(2, occScaleRem))

        return offset


    def extractKtaCoef(self):
        """
        Function to calculate the Kta coefficient of each pixel in the frame of the sensor
        
        Returns:
            kTa (list): List of the kTa coefficient of each pixel
        """  
        kTa = []
        kTaRC = []

        kTas1 = ((self._mlxData[56] & 240) / 16) + 8
        kTas2 = self._mlxData[56] & 15

        kTaRC.append((self._mlxData[54] & 65280) / 256)
        if kTaRC[0] > 127:
            kTaRC[0] -= 256
        kTaRC.append((self._mlxData[55] & 65280) / 256)
        if kTaRC[1] > 127:
            kTaRC[1] -= 256
        kTaRC.append(self._mlxData[54] & 255)
        if kTaRC[2] > 127:
            kTaRC[2] -= 256
        kTaRC.append(self._mlxData[55] & 255)
        if kTaRC[3] > 127:
            kTaRC[3] -= 256
        
        for i in range(self._rows):
            for j in range(self._cols):
                l = self._cols * i + j
                split = 2 * (m.floor((l+1) / 32) - m.floor((l+1) / 64) * 2) + ((l+1) % 2)

                kTa.append((self._mlxData[64 + l] & 14) / 2)
                if kTa[l] > 3:
                    kTa[l] -= 8

                kTa[l] = round((kTaRC[split] + (kTa[l] * pow(2, kTas2))) / pow(2, kTas1), 6)
                
        return kTa


    def extractKvCoef(self):
        """
        Function to calculate the Kv coefficient of each pixel in the frame of the sensor
        
        Returns:
            kV (list): List of the Kv coefficient of each pixel
        """  
        kV = []
        kVT = []

        kVScale = (self._mlxData[56] & 3840) / 256

        kVT.append((self._mlxData[52] & 61440) / 4096)
        if kVT[0] > 7:
            kVT[0] -= 16
        kVT.append((self._mlxData[52] & 240) / 16)
        if kVT[1] > 7:
            kVT[1] -= 16
        kVT.append((self._mlxData[52] & 3840) / 256)
        if kVT[2] > 7:
            kVT[2] -= 16
        kVT.append(self._mlxData[52] & 15)
        if kVT[3] > 7:
            kVT[3] -= 16

        for i in range(self._rows):
            for j in range(self._cols):
                l = self._cols * i + j
                split = 2 * (m.floor((l+1) / 32) - m.floor((l+1) / 64) * 2) + ((l+1) % 2)
                
                kV.append(kVT[split] / pow(2, kVScale))
                
        return kV
    

    def extractComPixSens(self):
        """
        Function to calculate the compensation pixel sensitivity (alpha) of both subpages in the frame of the sensor
        
        Returns:
            offsetCPSub0 (int): Compensation pixel sensivity of subpage 0
            offsetCPSub1 (int): Compensation pixel sensivity of subpage 1
        """  
        aScaleCP = ((self._mlxData[31] & 61440) / 4096) + 27
        cpP1P0Ratio = (self._mlxData[57] & 64512) / 1024
        if cpP1P0Ratio > 31:
            cpP1P0Ratio -= 64
        
        alphaCPSub0 = (self._mlxData[57] & 1023) / pow(2, aScaleCP)
        alphaCPSub1 = alphaCPSub0 * (1 + (cpP1P0Ratio / 128))
        
        return alphaCPSub0, alphaCPSub1


    def extractComPixOff(self):
        """
        Function to calculate the compensation pixel offset of both subpages in the frame of the sensor
        
        Returns:
            offsetCPSub0 (int): Compensation pixel offset of subpage 0
            offsetCPSub1 (int): Compensation pixel offset of subpage 1
        """  
        offsetCPSub0 = self._mlxData[58] & 1023
        if offsetCPSub0 > 511:
            offsetCPSub0 -= 1024
        offsetCPSub1 = (self._mlxData[58] & 64512) / 1024
        if offsetCPSub1 > 31:
            offsetCPSub1 -= 64
        offsetCPSub1 += offsetCPSub0

        return offsetCPSub0, offsetCPSub1


    def extractKtaComPixCoef(self):
        """
        Function to calculate the Kta compensation pixel of the sensor
        
        Returns:
            kTaCP (float): Kta compensation pixel
        """  
        kTas1 = ((self._mlxData[56] & 240) / 16) + 8
        kTaCP = self._mlxData[59] & 255
        if kTaCP > 127:
            kTaCP -= 256
        kTaCP /= pow(2, kTas1)

        return kTaCP


    def extractKvComPixCoef(self):
        """
        Function to calculate the Kv compensation pixel of the sensor
        
        Returns:
            kVCP (float): Kv compensation pixel
        """  
        kVScale = (self._mlxData[56] & 3840) / 256
        kVCP = (self._mlxData[59] & 65280) / 256
        if kVCP > 127:
            kVCP -= 256
        kVCP /= pow(2, kVScale)

        return kVCP


    def extractCalMode(self):
        """
        Function to calculate the calibration mode of the sensor
        
        Returns:
            calMode (int): Number associated with the calibration settings of the sensor
        """  
        calMode = (self._mlxData[10] & 2048) / 16
        calMode = int(calMode) ^ 128

        return calMode


    def extractChessCorrCoef(self):
        """
        Function to calculate the correlation coefficients for the chess reading pattern of the sensor
        
        Returns:
            ilChessC1 (float): Parameter used for the calculation of pixel temperatures in the chess reading pattern
            ilChessC2 (float): Parameter used for the calculation of pixel temperatures in the chess reading pattern
            ilChessC3 (float): Parameter used for the calculation of pixel temperatures in the chess reading pattern
        """  
        ilChessC1 = self._mlxData[53] & 63
        if ilChessC1 > 31:
            ilChessC1 -= 64
        ilChessC1 /= 16

        ilChessC2 = (self._mlxData[53] & 1984) / 64
        if ilChessC2 > 15:
            ilChessC2 -= 32
        ilChessC2 /= 2

        ilChessC3 = (self._mlxData[53] & 63488) / 2048
        if ilChessC3 > 15:
            ilChessC3 -= 32
        ilChessC3 /= 8

        return ilChessC1, ilChessC2, ilChessC3
    

    def extractDeviatingPix(self): 
        """
        Function to calculate the number of deviating and broken pixels in the frame of the sensor
        
        Returns:
            brokenPix (list): List of broken pixels
            outlierPix (list): List of outlier pixels
            warning (int): Warning number associated with specific error
        """  
        pixCnt = 0
        brokenPixCnt = 0
        outlierPixCnt = 0
        warn = 0
        warning = 0
        brokenPix = [65535] * 5
        outlierPix = [65535] * 5

        while pixCnt < 768 and brokenPixCnt < 5 and outlierPixCnt < 5:
            if self._mlxData[pixCnt + 64] == 0:
                brokenPix[brokenPixCnt] = pixCnt
                brokenPixCnt += 1
            elif (self._mlxData[53] & 1) == 0:
                outlierPix[outlierPixCnt] = pixCnt
                outlierPixCnt += 1
            pixCnt += 1
        
        if brokenPixCnt > 5:
            warn = -3
        elif outlierPixCnt > 5:
            warn = -4
        elif (brokenPixCnt + outlierPixCnt) > 5:
            warn = -5
        else:
            for i in range(brokenPixCnt):
                for j in range(i+1,brokenPixCnt):
                    warn = self._checkAdjacentPix(brokenPix[i],brokenPix[j])
                    if not (warn == 0):
                        warning = warn
            for i in range(outlierPixCnt):
                for j in range(i+1,outlierPixCnt):
                    warn = self._checkAdjacentPix(outlierPix[i],outlierPix[j])
                    if not (warn == 0):
                        warning = warn 
            for i in range(brokenPixCnt):
                for j in range(outlierPixCnt):
                    warn = self._checkAdjacentPix(brokenPix[i],outlierPix[j])
                    if not (warn == 0):
                        warning = warn

        return brokenPix, outlierPix, warning


    def _checkAdjacentPix(self, pix1, pix2):
        """
        Function that aids in the detection of deviating and broken pixels

        Parameters:
            pix1 (int): Pixel used for comparison
            pix2 (int): Second pixel, to be compared with the pix1
        
        Returns:
            result (int): Gives a warning if the difference between the pixels is between certain ranges
        """  
        pixPosDif = pix1 - pix2
        if (pixPosDif > -34 and pixPosDif < -30) or (pixPosDif > -2 and pixPosDif < 2) or (pixPosDif > 30 and pixPosDif < 34):
            result = -6
        else:
            result = 0
        
        return result