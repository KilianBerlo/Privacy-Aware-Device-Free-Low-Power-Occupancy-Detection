# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.
import asyncio
from datetime import datetime
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

CONNECTION_STRING = "HostName=geojson-ticket-hub.azure-devices.net;DeviceId=tudelft_device001;SharedAccessKey=6dCj+Nr3TqWAuuJ303DbpEqOheoXWNKi60ixbG3Dx2Q="

# Define the JSON message to send to IoT Hub.
type = "Feature"
id = "54:ee:75:57:b8:59"
accuracy = 100
battery = "85%"
clientel = "TUDelft"
color = "red"
typeGeom = "Point"
coordinates = [51.43, 24.31]
# MSG_TXT2 = '{{"Accuracy": {acc}, "Battery": {bat}, "Color": {col}, "id": {idd}, "Latitude": {lat}, "Longitude": {long}}}'
PROPERTY_TXT = '{{"accuracy": {accuracy}, "battery": {battery}, "client": {client}, "color": {color}, "dateTime": {dateTime}}}'
GEOM_TXT = '{{"type": {typeGeom}, "coordinates": {coordinates}}}'
MSG_TXT = '{{"type": {type},"id": {id}, "properties": {properties}, "geometry": {geometry}}}' 

async def run_telemetry_sample(client):
    # This sample will send temperature telemetry every second
    print("IoT Hub device sending periodic messages")

    await client.connect()

    while True:
        # Build the message with simulated telemetry values.
        dateTime = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        properties = PROPERTY_TXT.format(accuracy=accuracy, battery=battery, client=clientel, color=color, dateTime=dateTime)
        geometry = GEOM_TXT.format(typeGeom=typeGeom, coordinates=coordinates)

        msg_txt_formatted = MSG_TXT.format(type=type, id=id, properties=properties, geometry=geometry)
        # msg_txt_formatted = MSG_TXT2.format(acc=accuracy, bat=battery, col=color, idd=id, lat=coordinates[0], long=coordinates[1])
        message = Message(msg_txt_formatted)

        # Send the message.
        print("Sending message: {}".format(message))
        await client.send_message(message)
        print("Message successfully sent")
        await asyncio.sleep(1)


def main():
    print ("IoT Hub Quickstart #1 - Simulated device")
    print ("Press Ctrl-C to exit")

    # Instantiate the client
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