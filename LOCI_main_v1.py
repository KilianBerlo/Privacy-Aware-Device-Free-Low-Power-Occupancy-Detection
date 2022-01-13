import serial
import struct
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import calibration_restoration_EEPROM as cre
import temperature_calculation as tc
# # Examples
# import temperature_calculation_xmpl as tcx

ROWS = 24
COLS = 32

class Base():
    def __init__(self):
        ## The received data is put in a list
        self._dataEE = []  
        self._calData = {} 
        self._imData = np.empty([ROWS, COLS])

        ## Configure the serial connection (the port might differ per machine)
        self.ser = serial.Serial(port='/dev/ttyUSB0',baudrate=256000,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
        ## Cleaning the buffers to make sure there is nothing in it
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()

    def read_EEPROM(self):
        self.ser.write(b'\x01')          
        read = self.ser.read(1664)

        ## Upon receival, immediately extract the correct hex values
        for i in range(0, len(read), 2):
            self._dataEE.append((struct.unpack('<H', read[i:i+2])[0]))
        ## Cleaning the buffers to make sure there is nothing in it
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()

        # # Example 1
        # xmpl = ['0x00AE','0x499A','0x0000','0x2061','0x0005','0x0320','0x03E0','0x1710','0xA224','0x0185','0x0499','0x0000','0x1901','0x0000','0x0000','0xB533','0x4210','0xFFC2','0x0202','0x0202','0xF202','0xF1F2','0xD1E1','0xAFC0','0xFF00','0xF002','0xF103','0xE103','0xE1F5','0xD1E4','0xC1D5','0x91C2','0x8895','0x30D9','0xEDCB','0x110F','0x3322','0x2233','0x0011','0xCCEE','0xFFED','0x1100','0x2222','0x3333','0x2233','0x0022','0xDEF0','0x9ACC','0x15CC','0x2FA4','0x2555','0x9C78','0x7666','0x01C8','0x3B38','0x3534','0x2452','0x0463','0x13BB','0x0623','0xEC00','0x9797','0x9797','0x2AFB','0x00AE','0xFBE0','0x1B70','0xF3BE','0x000E','0xF86E','0x1B7E','0xF3CE','0xFFCE','0xF41E','0x102E','0xEC0E','0xFFDE','0xEC3E','0x139E','0xEF9E','0xFB9E','0xF77E','0x13E0','0xE7EE','0xF7AE','0xF750','0x0C30','0xEBEE','0xF730','0xF010','0x0B50','0xE430','0xF420','0xF370','0x07C0','0xE450','0x0470','0xFBCE','0xFF5C','0x0F90','0x07D0','0xFC3E','0xFF6C','0x0F90','0x03A0','0xFC0E','0xF40C','0x0BF0','0x03A0','0xF41E','0xF78C','0x0B70','0xFF72','0xFF6E','0xF7DE','0x07C0','0xFFA2','0x0330','0xF42E','0x0BC0','0xFF22','0xFC00','0xF75E','0x0410','0x0022','0x0350','0xF3A0','0x0832','0x04DE','0xFBF0','0x1BCE','0xF00E','0xFC5E','0xFC80','0x1BF0','0xF02E','0x0002','0xF81E','0x142E','0xEC9E','0x07DE','0xF09E','0x17CE','0xF3AE','0xFFC0','0xFBB0','0x1080','0xEBFE','0xFFE0','0xFF90','0x1460','0xE4AE','0xFBC0','0xF840','0x0FE0','0xE860','0xF8C0','0xF400','0x0842','0xE4B0','0x0890','0x03BE','0xFF9C','0x0FD0','0x0020','0x0450','0xFFCC','0x0FE0','0x07D0','0x03FE','0xFBEE','0x0C60','0x0B80','0xF86E','0xFB8E','0x1370','0x0782','0x038E','0xF85E','0x0FC2','0x07C2','0x037E','0xF84E','0x0880','0x0392','0x0420','0xF7CE','0x0C42','0xFCB2','0xFFE0','0xF020','0x0490','0x107E','0x03D0','0x1F90','0xFBCE','0x089E','0x0080','0x1820','0xF40E','0x0800','0xFC30','0x141E','0xF06E','0x0400','0xFFA0','0x17CE','0xF7B0','0x07D0','0xFFB0','0x1830','0xF3FE','0x0002','0xFFE0','0x14D0','0xECB0','0xFBE2','0xFCB0','0x13B0','0xECA0','0xF8DE','0xF432','0x0832','0xE8D0','0x1420','0xFF8E','0xFF6E','0x1380','0x0840','0x005E','0xFBEC','0x0FB0','0x0BB2','0xFFFE','0xFBDE','0x0820','0x0BC0','0x0360','0xFB8C','0x0F70','0x0794','0x036E','0xFBFE','0x0FA0','0x0BC4','0x0390','0xF89E','0x0C72','0xFFB2','0xFC70','0xFB7E','0x0470','0xFCB0','0xFFF0','0xF3F0','0x04A0','0x049E','0x03B0','0x1F90','0xF7D0','0x042E','0x0070','0x1F70','0xFBBE','0x0F00','0x03B0','0x142E','0xF01E','0x07B0','0xFFB0','0x1B60','0xF37E','0xFBD0','0xFF90','0x1410','0xF3C0','0xFC00','0x0370','0x1482','0xF030','0xF800','0xFC50','0x13C2','0xF050','0x0070','0xF812','0x0C02','0xEC80','0x00D0','0xFBFE','0xFBCC','0x0810','0xFC60','0xFCB0','0xFBCE','0x0FE0','0x0B40','0xFFFE','0xF05C','0x0840','0x07D0','0xFFD0','0xF79E','0x0FB0','0xF802','0xFFD0','0xF44E','0x0BF0','0xFC32','0x07A0','0xF4BE','0x0C60','0xF822','0x0080','0xF01E','0x0892','0x00B4','0xF850','0xF040','0x04B2','0x085E','0x0782','0x1F70','0xFBEE','0x001E','0x0420','0x1F80','0xFBB0','0x03B0','0x0390','0x17F0','0xF04E','0x0770','0xFFE0','0x1B40','0xF76E','0xFFC0','0xFFB0','0x17E0','0xEC1E','0x03A0','0x03A0','0x10C0','0xEC60','0xFBC2','0xFC80','0x0C00','0xEC60','0x0050','0xF800','0x0802','0xEC90','0x0080','0xF7B0','0xF7AE','0x0410','0xFC32','0xFC50','0xF7BE','0x07F0','0xFFD2','0xFBC0','0xF02E','0x0460','0x0382','0xF410','0xF36E','0x0BA0','0xFBF2','0xFBC0','0xF01C','0x0440','0xFFE2','0xFBE0','0xF0EE','0x08A2','0xF804','0xFCB0','0xEC3E','0x04A2','0x0082','0xF830','0xE830','0x04B2','0x13F0','0x0380','0x1F40','0xFBB0','0x0F90','0x0420','0x17A0','0xF7AE','0x0F40','0xFFE2','0x13AE','0xF03E','0x0F12','0xFF60','0x0F50','0xF340','0x0362','0xFF30','0x1760','0xEFD0','0x0762','0x0360','0x1072','0xEC50','0xF7B2','0xF852','0x07B0','0xE480','0xF820','0xF7C2','0x03C2','0xE490','0x1422','0x03AE','0x036E','0x13C2','0x13B2','0x0440','0xFFCE','0x13D2','0x1362','0x0002','0xFBDE','0x0C40','0x1732','0x0390','0xFF8E','0x1760','0x0B82','0x0750','0x039E','0x1000','0x0F82','0x0B80','0xFCAE','0x1080','0x0BD4','0x0470','0xFBCE','0x0C92','0x0832','0x07E0','0xF7FE','0x0CA2','0x0010','0x0380','0x13D0','0xF7A0','0xFFBE','0x0052','0x1380','0xF770','0xFF70','0xFFA0','0x0FC0','0xF3BE','0x0340','0xFF60','0x0FC0','0xF370','0xFB30','0xFB80','0x0C10','0xE40E','0xFBA0','0xFBB0','0x0C42','0xE860','0xFB92','0xF4A2','0x0B82','0xE850','0xF832','0xFBA2','0x0002','0xE470','0x0022','0xF7A0','0xEFFE','0x0BC0','0x03D2','0xF860','0xF79E','0x0F92','0x0390','0xFFB0','0xF3FE','0x0FC0','0x0762','0xFF70','0xEFFE','0x1380','0x0362','0xFFB0','0xF42E','0x0810','0x07A2','0x07C0','0xF87E','0x0C82','0x0B94','0x0490','0xFB90','0x1062','0x0842','0x07B0','0xEC10','0x0C82','0x0850','0x13E2','0x2360','0x0420','0x0460','0x10B0','0x1FB0','0x03E0','0x0B80','0x0BF0','0x1430','0xFC00','0x0F90','0x0BC2','0x1BA0','0xFFC0','0x07C2','0x0B82','0x1BF0','0xF44E','0x0BB2','0x0FD2','0x14C2','0xF8A0','0x0792','0x0852','0x13E2','0xF850','0x00A0','0x0032','0x0C22','0xF0D0','0xF452','0xEFE0','0xEF7E','0xFC32','0xF072','0xF4C0','0xEBCE','0x03F0','0xFBA2','0xF400','0xE45E','0x0410','0xFFA2','0xF7D0','0xEBBE','0x0BD0','0xFBC2','0xFB80','0xF00E','0x0050','0x03D2','0x03D0','0xF0E0','0x0CA0','0x0384','0x0440','0xF3EE','0x0C52','0x00A2','0x0030','0xEC20','0x04C0','0x1022','0x0FD2','0x1F80','0x03F0','0x0830','0x0C82','0x17E0','0xFFB0','0x0410','0x0432','0x0870','0xF48E','0x0BD0','0x07B2','0x0F90','0xFBB0','0xFFF0','0x07A2','0x1410','0xF410','0x0022','0x0BC2','0x0CE0','0xF850','0xFFB2','0x0490','0x0BC0','0xECC0','0xFC70','0x0012','0x0400','0xF0B2','0x0402','0xF7D0','0xF37E','0x0BF2','0x0022','0xFC90','0xEFFE','0x0FC2','0xFC12','0xF84E','0xE87E','0x0480','0x07E2','0xFFB0','0xF7AE','0x0FC0','0x0002','0x07A0','0xF81E','0x1002','0x0422','0x0FD0','0xF8CE','0x1842','0x07A4','0x0880','0xFBB0','0x0CB0','0x0C62','0x0BF0','0xFBF0','0x10A0','0xF030','0x07D2','0x0BE0','0xF800','0xECA0','0x0482','0x0830','0xFBE0','0xF040','0xFC80','0x0810','0xF030','0xF410','0xF830','0x0BA0','0xF7A0','0xF3D2','0xFFF2','0x0840','0xEFF0','0xF400','0x03B2','0x0872','0xF030','0xEFB2','0x0042','0x03B2','0xEC40','0xFFE0','0xFFE2','0x0012','0xF420','0xF422','0xF7B0','0xE7CE','0x0BD2','0xF080','0x0070','0xEC2E','0x0FE2','0xF850','0x0070','0xF00E','0x0C42','0x0020','0x0030','0xF7AE','0x17B2','0x03D2','0x0400','0xF84E','0x17F0','0x0BE2','0x13A0','0xFC4E','0x1820','0x0792','0x1020','0xFB9E','0x1C10','0x1BC2','0x13C0','0xFBE0','0x2002','0xF040','0x13A2','0x0F80','0xFC30','0xF46E','0x0CC2','0x17B2','0x0010','0xFC10','0x0872','0x1000','0xF8B0','0x07BE','0x0BE2','0x13B0','0xFFE0','0xF410','0x0450','0x0C70','0xF420','0x03C0','0x0F82','0x1060','0xFFE0','0xFB70','0x13D2','0x0F90','0xF820','0xFC40','0x0FA2','0x0BE2','0xFC60','0xF012','0xFB80','0xEB5E','0x0802','0xF420','0x0090','0xF78E','0x13E2','0xFC02','0x0060','0xF40E','0x1090','0x0F90','0x0BD0','0xFBAE','0x1FD2','0x0002','0x0820','0xF85E','0x1800','0x0F82','0x1B60','0xFC3E','0x23C2','0x0B42','0x1BA0','0xFF7E','0x27E0','0x1012','0x1B70','0xFFC0','0x2040','0xFC70','0x1BA2','0x0FA0','0x0BA0','0x0002','0x1432','0x0FE0','0x0010','0xF83E','0x13E0','0x085E','0x07E0','0x005E','0x0842','0x0FEE','0x03D0','0xFC20','0x0FE2','0x1400','0x0780','0x0B90','0x1772','0x1410','0x07B0','0xFB10','0x17F2','0x0B20','0x03F0','0xFC1E','0x17B2','0x07CE','0x0830','0xE050','0xEF80','0xD38E','0x0382','0xEBE0','0xF810','0xDFBE','0x07D0','0xEC10','0xFFC0','0xE01E','0x0BB0','0xF820','0xF810','0xEBBE','0x0BA0','0xFBF0','0x07A0','0xF3EE','0x1B50','0x0752','0x0F30','0xF7EE','0x1B80','0x02F2','0x0FD0','0xF70E','0x13C0','0x0BE0','0x1390','0xF79E','0x1C00']
        # for i in range(0, len(xmpl)):
        #     self._dataEE.append(int(xmpl[i], 16))

        # # Example 2
        # self._dataEE = [166, 27039, 0, 8289, 4, 800, 992, 2828, 11342, 4486, 1165, 0, 6401, 0, 0, 48691, 17168, 65460, 4626, 514, 257, 61937, 57569, 49360, 4644, 276, 57587, 53474, 49363, 49362, 45507, 37314, 31142, 12378, 56762, 4607, 13090, 13107, 290, 56831, 56780, 4094, 8465, 12834, 8755, 4386, 65280, 52718, 6066, 12225, 9558, 41609, 17203, 467, 28010, 26725, 9059, 127, 5046, 839, 60416, 62208, 40645, 9560, 3808, 2944, 7390, 63790, 1326, 126, 8414, 64510, 1006, 2046, 7278, 63374, 14, 64574, 6174, 61310, 878, 830, 4112, 62446, 1008, 63424, 5136, 61422, 144, 61566, 2192, 60480, 63696, 60544, 3922, 59248, 65296, 63534, 61630, 1264, 63712, 61502, 62638, 960, 63408, 64446, 61500, 848, 64494, 61470, 62462, 64352, 64320, 64286, 61438, 1984, 64450, 62366, 62446, 944, 64610, 61518, 60510, 1040, 62610, 60510, 61392, 65488, 65534, 64656, 5230, 62606, 64640, 65456, 6224, 61342, 1840, 65470, 6158, 62270, 974, 64510, 3102, 61198, 65342, 63310, 4094, 61374, 65456, 62320, 4032, 60318, 64560, 61440, 1058, 59390, 62544, 59408, 3058, 56496, 62592, 61662, 60590, 192, 62656, 63486, 60590, 65488, 896, 63486, 61550, 896, 63520, 61534, 59534, 65392, 63376, 62382, 59486, 2, 63488, 61406, 60462, 65504, 63618, 61518, 58464, 64560, 63618, 60496, 59440, 62722, 4080, 64, 4096, 61518, 96, 65440, 6192, 62302, 1904, 64462, 5166, 61310, 64574, 63566, 3150, 59262, 880, 63376, 2094, 59408, 960, 62400, 4048, 59342, 63552, 61440, 16, 60352, 62494, 60368, 1986, 56464, 7202, 3184, 1102, 7280, 4256, 4078, 2190, 7056, 7104, 3102, 2190, 6080, 4224, 2190, 1182, 5072, 6082, 3054, 126, 6240, 6162, 2078, 2094, 5120, 5250, 2128, 64, 7152, 5186, 1024, 2032, 3282, 65440, 65504, 5070, 62446, 64512, 65360, 4112, 60256, 63358, 63424, 3150, 61278, 60494, 61568, 2096, 58270, 63360, 61360, 1072, 58382, 61456, 61344, 2, 57296, 63490, 61424, 960, 58272, 62418, 59312, 1874, 56352, 3010, 1040, 64510, 4112, 2098, 1920, 78, 4000, 1968, 1024, 64654, 4992, 64640, 64718, 64638, 3024, 3010, 65520, 63614, 4160, 1106, 992, 63582, 3088, 4162, 1056, 64496, 5074, 4082, 65504, 65408, 2114, 6016, 6128, 10206, 3056, 6144, 5024, 10336, 1950, 5056, 6112, 9360, 958, 4206, 4208, 8368, 65486, 2062, 4080, 7280, 64654, 4128, 2048, 7216, 63504, 5138, 3072, 8146, 65456, 4032, 1938, 7042, 63504, 944, 62494, 61438, 1040, 50, 62414, 61598, 960, 64496, 64542, 61646, 2016, 64656, 64686, 60638, 1008, 62496, 63534, 61616, 1184, 82, 62526, 61550, 1072, 2114, 64560, 61440, 3024, 2018, 63408, 61344, 1058, 8000, 6032, 10098, 3008, 6128, 4928, 9248, 1888, 6032, 5088, 7326, 958, 5200, 3200, 6302, 65440, 4000, 3040, 6240, 64592, 3088, 2000, 6176, 64464, 1104, 1024, 4048, 64432, 1968, 1874, 4930, 63456, 65362, 62368, 60302, 65490, 63506, 62318, 60478, 65392, 65456, 61454, 59566, 64448, 64626, 61614, 58558, 64448, 64434, 61440, 59518, 64624, 63522, 63456, 59470, 65520, 63602, 62480, 59360, 65472, 64450, 62304, 60240, 64498, 2928, 5058, 7072, 992, 1024, 3968, 6240, 63440, 2000, 3072, 5312, 64448, 64670, 224, 4286, 63422, 64512, 2992, 3280, 61614, 1056, 64544, 3168, 63456, 98, 32, 4050, 64400, 962, 65410, 5940, 62448, 2930, 960, 64430, 5104, 2066, 896, 63614, 3040, 2000, 1038, 63710, 6082, 1168, 238, 63694, 5056, 2050, 4032, 62686, 4272, 3122, 1056, 63598, 7138, 4210, 3104, 65504, 8082, 5058, 3984, 2864, 5122, 62336, 2994, 4992, 63472, 63488, 1906, 3152, 62352, 65392, 2, 4192, 63406, 63552, 112, 2176, 61344, 65440, 944, 1152, 61520, 62528, 65504, 2080, 61408, 63586, 994, 976, 63360, 64416, 64354, 3858, 61424, 61312, 62384, 60302, 65522, 62466, 63328, 60494, 896, 65376, 64510, 61534, 2944, 64576, 63584, 60542, 1936, 930, 928, 60526, 3138, 64578, 976, 61456, 4050, 1106, 2000, 62400, 6000, 2978, 1888, 65280, 4066, 63426, 2, 2992, 62466, 62480, 882, 1120, 61296, 64384, 63504, 126, 60336, 63568, 63632, 64656, 60320, 62432, 62464, 64640, 60512, 63520, 62496, 48, 59392, 62512, 65520, 63472, 62368, 62400, 63378, 65346, 59442, 1970, 4080, 65454, 7154, 3074, 3920, 64590, 7010, 6002, 4080, 94, 6032, 5170, 3168, 110, 7040, 6066, 5088, 110, 8258, 7170, 6128, 2064, 9184, 7202, 8144, 2016, 11138, 9138, 7040, 4912, 8226, 63440, 6162, 7120, 1072, 64576, 6018, 6224, 1890, 2912, 7072, 6224, 1872, 3040, 4160, 5216, 880, 1918, 5040, 5168, 48, 3040, 5058, 5136, 1952, 3074, 6130, 6082, 2976, 2002, 6002, 6002, 1072, 59458, 63600, 59454, 1170, 62626, 65504, 60606, 4018, 946, 2032, 60590, 5040, 1074, 1152, 61616, 5042, 1986, 2032, 62592, 5248, 2098, 2064, 62560, 7154, 5202, 4160, 64544, 7170, 4162, 6096, 992, 8338, 58448, 4212, 1106, 64658, 61584, 3042, 2192, 64432, 64400, 5042, 4176, 63408, 63504, 3122, 2144, 64368, 63392, 2962, 3120, 63552, 1968, 3008, 4098, 64496, 63600, 4098, 66, 65520, 64562, 4066, 4034, 144, 61488, 2128, 61502, 5234, 114, 3008, 63614, 7042, 3938, 6000, 32, 7024, 5056, 6128, 64558, 8994, 3938, 6992, 2032, 10226, 10114, 8064, 3024, 10178, 6210, 10192, 16, 13266, 9234, 11200, 6048, 13426, 56512, 1250, 62624, 62658, 58576, 2018, 128, 62368, 61360, 1970, 63552, 62288, 63470, 2034, 63520, 62256, 61312, 1888, 64544, 63472, 63424, 962, 2034, 63424, 59504, 2066, 60512, 62496, 59504, 1074, 61488, 63728, 56480, 62656, 54414, 162, 60576, 960, 59502, 2930, 64368, 896, 60416, 2848, 1952, 2992, 62432, 4848, 834, 3856, 62446, 8112, 3984, 3968, 64448, 8082, 2114, 6112, 61504, 7168, 4178, 5136, 64528, 8402]
        return self._dataEE

    def MLX90640_ExtractParameters(self, eepromData):
        ## Check whether the devicedata is correct
        deviceSelect = self._dataEE[10] & 64
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
        self.ser.write(b'\x02')
        dataTemp = tc.temperature_calculation(self.ser, deviceParams).getPixData()
        # dataTemp = tcx.temperature_calculation_xmpl(deviceParams).getPixData()
        for i in range(ROWS):
            for j in range(COLS):
                self._imData[i,j] = dataTemp[(i*32) + j]

        
        ### IMAGE PROCESSING ###
        plt.ion()
        fig, ax = plt.subplots()
        im = ax.imshow(self._imData, 'jet')

        # # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel("", rotation=-90, va="bottom")

        for i in range(50):
            print(".", end="")
            dataTemp = tc.temperature_calculation(self.ser, deviceParams).getPixData()
            # dataTemp = tcx.temperature_calculation_xmpl(deviceParams).getPixData()
            for i in range(ROWS):
                for j in range(COLS):
                    self._imData[i,j] = dataTemp[(i*32) + j]
            im.set_data(self._imData)
            fig.canvas.flush_events()

        print()

if __name__ == '__main__':
    b = Base() 
    b.main()