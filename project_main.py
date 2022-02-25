import serial
import struct
import numpy             as np
import matplotlib.pyplot as plt
import asyncio

from azure.iot.device.aio   import IoTHubDeviceClient
from datetime               import datetime
from azure.iot.device       import Message

import calibration_restoration_EEPROM as cre
import temperature_calculation        as tc
import heatmap_visualisations         as hv
import person_detection               as pd

## Set to True if live serial data is used, set to False if example data is used
LIVE = False
## Set to True if real-time feedback is desired, set to False if a snapshot has to be analysed
VID = False
## Set to True if contours have to be shown in the real-time version, set to False if not
CONTOUR = True

## The number of rows and columns of a frame from the sensor
ROWS = 24
COLS = 32

## Indicates in which files data has to be saved for possible analysis later on
FIGURE = 'test_data/newfigure.jpg'
FIGDATA = 'test_data/newfigure.txt'
FIGTEMP = 'test_data/figureTemp.txt'

## Connection string needed to connect and authenticate to the IoT Hub (Azure IoT, but provided by try.IoT)
CONNECTION_STRING = "HostName=geojson-ticket-hub.azure-devices.net;DeviceId=tudelft_device001;SharedAccessKey=6dCj+Nr3TqWAuuJ303DbpEqOheoXWNKi60ixbG3Dx2Q="

## JSON data format for messaging to the IoT Hub
PROPERTY_TXT = '{{"client":"{client}","accuracy":{accuracy},"battery":"{battery}","color":"{color}","dateTime":"{dateTime}"}}'
GEOM_TXT = '{{"type":"{typeGeom}","coordinates":{coordinates}}}'
MSG_TXT = '{{"type":"{type}","id":"{id}","properties":{properties},"geometry":{geometry}}}' 

class Base():
    """
    Main class of the occupancy detection program
    """
    def __init__(self):
        """
        Constructor for the base class of the occupancy detection project
        """
        ## EEPROM data, restored EEPROM data and pixel temperature data
        self._EERAW = np.empty(832)  
        self._EEPROM = {}
        self._pixTemp = np.empty([ROWS, COLS])

        if LIVE:
            ## Configure the serial connection (the port might differ per machine)
            self.ser = serial.Serial(port='/dev/ttyUSB0',baudrate=256000,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
            ## Cleaning the buffers to make sure there is no junk in there, before EEPROM receival
            self.ser.reset_output_buffer()
            self.ser.reset_input_buffer()
        else:
            self.ser = 0

    def read_EEPROM(self):
        """
        Function to gather EEPROM data
        
        Returns:
            np.array: Uncalibrated EEPROM Hex data
        """        
        # If live, then gather data from sensor, if not then use provided exemplary data
        if LIVE:
            ## sending 0x01 to the sensor will activate EEPROM data transmission and this set of data contains 1664 bytes
            self.ser.write(b'\x01')          
            read = self.ser.read(1664)

            ## Upon receival, extract the correct hex values from the bytes
            for i in range(0, len(read), 2):
                self._EERAW[int(i/2)] = (struct.unpack('<H', read[i:i+2])[0])
            self._EERAW = self._EERAW.astype(int)
            ## Cleaning the buffers again to make sure there is no junk in there, before communication
            self.ser.reset_output_buffer()
            self.ser.reset_input_buffer()
        else:
            ## Exemplary EEPROM data
            self._EERAW = np.array([166, 27039, 0, 8289, 4, 800, 992, 2828, 11342, 4486, 1165, 0
, 6401, 0, 0, 48691, 17168, 65460, 4626, 514, 257, 61937, 57569, 49360
, 4644, 276, 57587, 53474, 49363, 49362, 45507, 37314, 31142, 12378, 56762, 4607
, 13090, 13107, 290, 56831, 56780, 4094, 8465, 12834, 8755, 4386, 65280, 52718
, 6066, 12225, 9558, 41609, 17203, 467, 28010, 26725, 9059, 127, 5046, 839
, 60416, 62208, 40645, 9560, 3808, 2944, 7390, 63790, 1326, 126, 8414, 64510
, 1006, 2046, 7278, 63374, 14, 64574, 6174, 61310, 878, 830, 4112, 62446
, 1008, 63424, 5136, 61422, 144, 61566, 2192, 60480, 63696, 60544, 3922, 59248
, 65296, 63534, 61630, 1264, 63712, 61502, 62638, 960, 63408, 64446, 61500, 848
, 64494, 61470, 62462, 64352, 64320, 64286, 61438, 1984, 64450, 62366, 62446, 944
, 64610, 61518, 60510, 1040, 62610, 60510, 61392, 65488, 65534, 64656, 5230, 62606
, 64640, 65456, 6224, 61342, 1840, 65470, 6158, 62270, 974, 64510, 3102, 61198
, 65342, 63310, 4094, 61374, 65456, 62320, 4032, 60318, 64560, 61440, 1058, 59390
, 62544, 59408, 3058, 56496, 62592, 61662, 60590, 192, 62656, 63486, 60590, 65488
, 896, 63486, 61550, 896, 63520, 61534, 59534, 65392, 63376, 62382, 59486, 2
, 63488, 61406, 60462, 65504, 63618, 61518, 58464, 64560, 63618, 60496, 59440, 62722
, 4080, 64, 4096, 61518, 96, 65440, 6192, 62302, 1904, 64462, 5166, 61310
, 64574, 63566, 3150, 59262, 880, 63376, 2094, 59408, 960, 62400, 4048, 59342
, 63552, 61440, 16, 60352, 62494, 60368, 1986, 56464, 7202, 3184, 1102, 7280
, 4256, 4078, 2190, 7056, 7104, 3102, 2190, 6080, 4224, 2190, 1182, 5072
, 6082, 3054, 126, 6240, 6162, 2078, 2094, 5120, 5250, 2128, 64, 7152
, 5186, 1024, 2032, 3282, 65440, 65504, 5070, 62446, 64512, 65360, 4112, 60256
, 63358, 63424, 3150, 61278, 60494, 61568, 2096, 58270, 63360, 61360, 1072, 58382
, 61456, 61344, 2, 57296, 63490, 61424, 960, 58272, 62418, 59312, 1874, 56352
, 3010, 1040, 64510, 4112, 2098, 1920, 78, 4000, 1968, 1024, 64654, 4992
, 64640, 64718, 64638, 3024, 3010, 65520, 63614, 4160, 1106, 992, 63582, 3088
, 4162, 1056, 64496, 5074, 4082, 65504, 65408, 2114, 6016, 6128, 10206, 3056
, 6144, 5024, 10336, 1950, 5056, 6112, 9360, 958, 4206, 4208, 8368, 65486
, 2062, 4080, 7280, 64654, 4128, 2048, 7216, 63504, 5138, 3072, 8146, 65456
, 4032, 1938, 7042, 63504, 944, 62494, 61438, 1040, 50, 62414, 61598, 960
, 64496, 64542, 61646, 2016, 64656, 64686, 60638, 1008, 62496, 63534, 61616, 1184
, 82, 62526, 61550, 1072, 2114, 64560, 61440, 3024, 2018, 63408, 61344, 1058
, 8000, 6032, 10098, 3008, 6128, 4928, 9248, 1888, 6032, 5088, 7326, 958
, 5200, 3200, 6302, 65440, 4000, 3040, 6240, 64592, 3088, 2000, 6176, 64464
, 1104, 1024, 4048, 64432, 1968, 1874, 4930, 63456, 65362, 62368, 60302, 65490
, 63506, 62318, 60478, 65392, 65456, 61454, 59566, 64448, 64626, 61614, 58558, 64448
, 64434, 61440, 59518, 64624, 63522, 63456, 59470, 65520, 63602, 62480, 59360, 65472
, 64450, 62304, 60240, 64498, 2928, 5058, 7072, 992, 1024, 3968, 6240, 63440
, 2000, 3072, 5312, 64448, 64670, 224, 4286, 63422, 64512, 2992, 3280, 61614
, 1056, 64544, 3168, 63456, 98, 32, 4050, 64400, 962, 65410, 5940, 62448
, 2930, 960, 64430, 5104, 2066, 896, 63614, 3040, 2000, 1038, 63710, 6082
, 1168, 238, 63694, 5056, 2050, 4032, 62686, 4272, 3122, 1056, 63598, 7138
, 4210, 3104, 65504, 8082, 5058, 3984, 2864, 5122, 62336, 2994, 4992, 63472
, 63488, 1906, 3152, 62352, 65392, 2, 4192, 63406, 63552, 112, 2176, 61344
, 65440, 944, 1152, 61520, 62528, 65504, 2080, 61408, 63586, 994, 976, 63360
, 64416, 64354, 3858, 61424, 61312, 62384, 60302, 65522, 62466, 63328, 60494, 896
, 65376, 64510, 61534, 2944, 64576, 63584, 60542, 1936, 930, 928, 60526, 3138
, 64578, 976, 61456, 4050, 1106, 2000, 62400, 6000, 2978, 1888, 65280, 4066
, 63426, 2, 2992, 62466, 62480, 882, 1120, 61296, 64384, 63504, 126, 60336
, 63568, 63632, 64656, 60320, 62432, 62464, 64640, 60512, 63520, 62496, 48, 59392
, 62512, 65520, 63472, 62368, 62400, 63378, 65346, 59442, 1970, 4080, 65454, 7154
, 3074, 3920, 64590, 7010, 6002, 4080, 94, 6032, 5170, 3168, 110, 7040
, 6066, 5088, 110, 8258, 7170, 6128, 2064, 9184, 7202, 8144, 2016, 11138
, 9138, 7040, 4912, 8226, 63440, 6162, 7120, 1072, 64576, 6018, 6224, 1890
, 2912, 7072, 6224, 1872, 3040, 4160, 5216, 880, 1918, 5040, 5168, 48
, 3040, 5058, 5136, 1952, 3074, 6130, 6082, 2976, 2002, 6002, 6002, 1072
, 59458, 63600, 59454, 1170, 62626, 65504, 60606, 4018, 946, 2032, 60590, 5040
, 1074, 1152, 61616, 5042, 1986, 2032, 62592, 5248, 2098, 2064, 62560, 7154
, 5202, 4160, 64544, 7170, 4162, 6096, 992, 8338, 58448, 4212, 1106, 64658
, 61584, 3042, 2192, 64432, 64400, 5042, 4176, 63408, 63504, 3122, 2144, 64368
, 63392, 2962, 3120, 63552, 1968, 3008, 4098, 64496, 63600, 4098, 66, 65520
, 64562, 4066, 4034, 144, 61488, 2128, 61502, 5234, 114, 3008, 63614, 7042
, 3938, 6000, 32, 7024, 5056, 6128, 64558, 8994, 3938, 6992, 2032, 10226
, 10114, 8064, 3024, 10178, 6210, 10192, 16, 13266, 9234, 11200, 6048, 13426
, 56512, 1250, 62624, 62658, 58576, 2018, 128, 62368, 61360, 1970, 63552, 62288
, 63470, 2034, 63520, 62256, 61312, 1888, 64544, 63472, 63424, 962, 2034, 63424
, 59504, 2066, 60512, 62496, 59504, 1074, 61488, 63728, 56480, 62656, 54414, 162
, 60576, 960, 59502, 2930, 64368, 896, 60416, 2848, 1952, 2992, 62432, 4848
, 834, 3856, 62446, 8112, 3984, 3968, 64448, 8082, 2114, 6112, 61504, 7168
, 4178, 5136, 64528, 8402])
        return self._EERAW

    def MLX90640_ExtractParameters(self, eepromData):
        """
        Function to gather EEPROM data
        
        Parameters:
            eepromData (np.array): Uncalibrated EEPROM Hex data obtained in the read_EEPROM() function
        """        
    
        ## Check whether the devicedata is correct, otherwise error
        deviceSelect = self._EERAW[10] & 64
        if deviceSelect == 0:
            error = 0
        else:
            error = -7

        ## Restoring and calibrating the EEPROM data
        if error == 0:
            self._EEPROM['kVdd'], self._EEPROM['vdd25'] = eepromData.extractVDDParams()
            self._EEPROM['kvPTAT'], self._EEPROM['ktPTAT'], self._EEPROM['vPTAT25'], self._EEPROM['alphaPTAT'] = eepromData.extractPTATParams()
            self._EEPROM['gainEE'] = eepromData.extractGainCoef()
            self._EEPROM['tgc'] = eepromData.extractTGCCoef()
            self._EEPROM['resolutionEE'] = eepromData.extractResConCoef()
            self._EEPROM['KsTa'] = eepromData.extractKsTaCoef()
            self._EEPROM['KsTo'] = eepromData.extractKsToCoef()
            self._EEPROM['ct'] = eepromData.extractCornerTemps()
            self._EEPROM['alpha'] = eepromData.extractPixSens()
            self._EEPROM['offset'] = eepromData.extractPixOff()
            self._EEPROM['kta'] = eepromData.extractKtaCoef()
            self._EEPROM['kv'] = eepromData.extractKvCoef()
            self._EEPROM['cpAlpha'] = eepromData.extractComPixSens()
            self._EEPROM['cpOffset'] = eepromData.extractComPixOff()
            self._EEPROM['cpKv'] = eepromData.extractKvComPixCoef()
            self._EEPROM['cpKta'] = eepromData.extractKtaComPixCoef()
            self._EEPROM['calibrationModeEE'] = eepromData.extractCalMode()
            self._EEPROM['ilChessC'] = eepromData.extractChessCorrCoef()
            dev_val = eepromData.extractDeviatingPix()
            self._EEPROM['brokenPixels'] = dev_val[0]
            self._EEPROM['outlierPixels'] = dev_val[1]
            self._EEPROM['warning'] = dev_val[2]

    def calculate_PixTemp(self):
        """
        Function that calculates the temperature of each pixel and fits it to the corresponding pixel
        """        
        # Calculate the temperature based on real-time sensor data, if not live then calculate the temperature based on the provided exemplary data
        dataTemp = tc.temperature_calculation(self._EEPROM, self.ser, FIGDATA).getPixData()

        # Fit temperature to each corresponding pixel
        for i in range(ROWS):
            for j in range(COLS):
                self._pixTemp[i,j] = dataTemp[(i*32) + j]
        
        # For saving temperature data of a frame
        framefile = open(FIGTEMP, 'w')
        framefile.write("temperature data: " + str(self._pixTemp) + "\n")
        framefile.close()

    async def run_telemetry(self, client, fig, im, bg):
        """
        Function to gather EEPROM data
        
        Parameters:
            client (IoTHubDeviceClient): The IoT Hub connection string
            fig (Figure): The canvas on which the image is drawn
            im (AxesImage): Image attached to an axes, contains the image obtained
            bg (np.array): Relative background temperature (manually obtained)
        """        
        ## Connect to the IoT Hub
        await client.connect()
        print("IoT Hub device connected")

        ## For X (50) consecutive frames show the result of the person detection algorithm applied to the frames
        for i in range(5):
            ## If person detection is desired in the video then detect and send it to the IoT Hub, if not then don't send anything and just show the video
            if CONTOUR == True:
                b.calculate_PixTemp()
                ## Remove the background from each new frame
                im.set_data(np.subtract(self._pixTemp, bg))
                plt.savefig(FIGURE, bbox_inches='tight',pad_inches = 0)
                ## Build the message with simulated telemetry values.
                dateTime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+01:00")
                personCount = pd.person_detection(FIGURE).contour_detection(1)

                ## Construction of the JSON formatted message to be sent to the IoT Hub (lots of unnecessary data but it was easier for tests this way)
                properties = PROPERTY_TXT.format(client="TUDelft", accuracy=personCount, battery="89%", color="black", dateTime=dateTime)
                geometry = GEOM_TXT.format(typeGeom="Point", coordinates=[52.011578, 4.357068])
                msg_txt_formatted = MSG_TXT.format(type="feature", id="54ee7557b859", properties=properties, geometry=geometry)
                message = Message(msg_txt_formatted)

                ## Sending the message to the IoT Hub
                print("Sending message: {}".format(message))
                await client.send_message(message)
                print("Message successfully sent")
            else:
                b.calculate_PixTemp()
                im.set_data(np.subtract(self._pixTemp, bg))
                fig.canvas.flush_events()

    def main(self):
        """
        Function that is executed first thing when the program is started
        """        
        ## PIR SETUP DATA ##
        self.read_EEPROM()
        self.MLX90640_ExtractParameters(cre.calibration_restoration_EEPROM(self._EERAW, ROWS, COLS))
        
        ## For saving eeprom data of a frame
        framefile = open(FIGDATA, 'w')
        framefile.write("eepromdata: " + str(self._EERAW) + "\n")
        framefile.close()

        ## If real-time data acquisition is desired then send the sensor 0x02, if not then use the exemplary data for processing
        if LIVE:
            self.ser.write(b'\x02')

        self.calculate_PixTemp()

        ## Instantiate the IoT Hub client
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        loop = asyncio.get_event_loop()

        fig, im, bg = hv.heatmap_visualisations(self._pixTemp, VID).show_Heatmap()

        if VID == True:
            try:
                ## Run the event loop for contour detection and telemetry with the IoT Hub
                loop.run_until_complete(self.run_telemetry(client, fig, im, bg))
            except KeyboardInterrupt:
                print("Connection with IoT Hub stopped")
            finally:
                ## Upon application exit, shut down the client
                print("Shutting down connection with IoT Hub")
                loop.run_until_complete(client.shutdown())
                loop.close()
        else:
            ## Snapshot with person detection
            plt.savefig(FIGURE, bbox_inches='tight',pad_inches = 0)
            pd.person_detection(FIGURE).contour_detection(0)

if __name__ == '__main__':
    b = Base() 
    b.main()
