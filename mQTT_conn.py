# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.
import asyncio
from datetime import datetime
import random
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

# The device connection authenticates your device to your IoT hub. The connection string for 
# a device should never be stored in code. For the sake of simplicity we're using an environment 
# variable here. If you created the environment variable with the IDE running, stop and restart 
# the IDE to pick up the environment variable.
#
# You can use the Azure CLI to find the connection string:
#     az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table

CONNECTION_STRING = "HostName=geojson-ticket-hub.azure-devices.net;DeviceId=tudelft_device001;SharedAccessKey=6dCj+Nr3TqWAuuJ303DbpEqOheoXWNKi60ixbG3Dx2Q="

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
PROPERTY_TXT = '{{"accuracy": {accuracy}, "battery": {battery}, "client": {client}, "color": {color}, "dateTime": {dateTime}}}'
GEOM_TXT = '{{"type": {typeGeom}, "coordinates": {coordinates}}}'
MSG_TXT = '{{"type": {type},"id": {id}, "properties": {properties}, "geometry": {geometry}}}' 

#   "geometry": {
#     "type": "Point",
#     "coordinates": [
#       5.458188056945801,
#       51.41125257942182
#     ]
#   }
# }

async def run_telemetry_sample(client):
    # This sample will send temperature telemetry every second
    print("IoT Hub device sending periodic messages")

    await client.connect()

    while True:
        # Build the message with simulated telemetry values.
        # temperature = TEMPERATURE + (random.random() * 15)
        # humidity = HUMIDITY + (random.random() * 20)

        type = "Feature"
        id = "54:ee:75:57:b8:59"
        accuracy = 100
        battery = "85%"
        clientel = "TUDelft"
        color = "red"
        dateTime = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        typeGeom = "Point"
        coordinates = [51.43, 24.31]

        properties = PROPERTY_TXT.format(accuracy=accuracy, battery=battery, client=clientel, color=color, dateTime=dateTime)
        geometry = GEOM_TXT.format(typeGeom=typeGeom, coordinates=coordinates)

        msg_txt_formatted = MSG_TXT.format(type=type, id=id, properties=properties, geometry=geometry) #temperature=temperature, humidity=humidity, 
        message = Message(msg_txt_formatted)
        # Add a custom application property to the message.
        # An IoT hub can filter on these properties without access to the message body.
        # if temperature > 30:
        #     message.custom_properties["temperatureAlert"] = "true"
        # else:
        #     message.custom_properties["temperatureAlert"] = "false"

        # Send the message.
        print("Sending message: {}".format(message))
        await client.send_message(message)
        print("Message successfully sent")
        await asyncio.sleep(1)


def main():
    print ("IoT Hub Quickstart #1 - Simulated device")
    print ("Press Ctrl-C to exit")

    # Instantiate the client. Use the same instance of the client for the duration of
    # your application
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    loop = asyncio.get_event_loop()
    try:
        # Run the sample in the event loop
        loop.run_until_complete(run_telemetry_sample(client))
    except KeyboardInterrupt:
        print("IoTHubClient sample stopped by user")
    finally:
        # Upon application exit, shut down the client
        print("Shutting down IoTHubClient")
        loop.run_until_complete(client.shutdown())
        loop.close()


if __name__ == '__main__':
    main()