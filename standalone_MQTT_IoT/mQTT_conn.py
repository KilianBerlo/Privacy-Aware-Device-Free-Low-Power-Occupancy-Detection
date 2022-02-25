# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import asyncio
from datetime import datetime
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

## Connection string needed to connect and authenticate to the IoT Hub (Azure IoT, but provided by try.IoT)
CONNECTION_STRING = "HostName=geojson-ticket-hub.azure-devices.net;DeviceId=tudelft_device001;SharedAccessKey=6dCj+Nr3TqWAuuJ303DbpEqOheoXWNKi60ixbG3Dx2Q="
# ## A second option, or in case of two devices:
# CONNECTION_STRING = "HostName=geojson-ticket-hub.azure-devices.net;DeviceId=tudelft_device002;SharedAccessKey=Su0mJ00EyxwIDGsDfaDIPPHXYO8G8CvSpUdgXSkDmSk="

## Define the JSON message contents to send to the IoT Hub
type = "feature"
id = "54ee7557b859"
accuracy = 74
battery = "89%"
clientel = "TUDelft"
color = "black"
typeGeom = "Point"
coordinates = [52.011578, 4.357068]

## JSON data format for messaging to the IoT Hub
PROPERTY_TXT = '{{"client":"{client}","accuracy":{accuracy},"battery":"{battery}","color":"{color}","dateTime":"{dateTime}"}}'
GEOM_TXT = '{{"type":"{typeGeom}","coordinates":{coordinates}}}'
MSG_TXT = '{{"type":"{type}","id":"{id}","properties":{properties},"geometry":{geometry}}}' 

async def run_telemetry_sample(client):
    """
    Function to run a telemetry sample with the IoT Hub
    
    Parameters:
        client (IoTHubDeviceClient): The IoT Hub connection string
    """        
    ## This sample will send temperature telemetry every second
    print("IoT Hub device sending periodic messages")

    await client.connect()

    while True:
        ## Build the message with simulated telemetry values
        dateTime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+01:00")

        ## Construction of the JSON formatted message to be sent to the IoT Hub
        properties = PROPERTY_TXT.format(client=clientel, accuracy=accuracy, battery=battery, color=color, dateTime=dateTime)
        geometry = GEOM_TXT.format(typeGeom=typeGeom, coordinates=coordinates)
        msg_txt_formatted = MSG_TXT.format(type=type, id=id, properties=properties, geometry=geometry)

        message = Message(msg_txt_formatted)

        ## Send the message
        print("Sending message: {}".format(message))
        await client.send_message(message)
        print("Message successfully sent")
        await asyncio.sleep(1)


def main():
    """
    Function that is executed first thing when the program is started
    """        
    print ("IoT Hub Quickstart #1 - Simulated device")
    print ("Press Ctrl-C to exit")

    ## Instantiate the client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    loop = asyncio.get_event_loop()
    try:
        ## Run the sample in the event loop
        loop.run_until_complete(run_telemetry_sample(client))
    except KeyboardInterrupt:
        print("IoTHubClient sample stopped by user")
    finally:
        ## Upon application exit, shut down the client
        print("Shutting down IoTHubClient")
        loop.run_until_complete(client.shutdown())
        loop.close()


if __name__ == '__main__':
    main()