# Standalone MQTT IoT Hub connection example
Examples on how to connect your device to an Azure IoT Hub using the MQTT protocol.


## Technologies:
Languages, libraries and versions used in the project:
- Python 3.8 with libs asyncio and datetime
- Microsoft .NET SDK 6.0
- Azure IoT Python SDK v2
- Azure IoT C SDK v1


## Launch
Since this is a development project, no command line UI was added for selecting proper options, this can all be edited in the code itself. The code is (build and) run as follows:
- Python:
``` 
$ python project_main.py
 ```
 - C#:
 ```
 $ dotnet build /home/kilian/Desktop/extra_project/LOCI/standalone_MQTT_IoT/mQTTDevice.csproj /property:GenerateFullPaths=true /consoleloggerparameters:NoSummary
 $ dotnet publish /home/kilian/Desktop/extra_project/LOCI/standalone_MQTT_IoT/mQTTDevice.csproj /property:GenerateFullPaths=true /consoleloggerparameters:NoSummary
 $ dotnet /home/kilian/Desktop/extra_project/LOCI/standalone_MQTT_IoT/bin/Debug/net6.0/mQTTDevice.dll [s_connectionString]
 ```

In both applications one argument still has to be set correctly, namely the s_connectionString. This argument is the device connection string to authenticate the device with your IoT hub. The current strings are placeholders and hence, don't work. This is done for security reasons. In the C# application setting the connection string can be done directly from the terminal or in the code, in the python file the only option is to adjust the code itself. The place in the code is indicated by the comment ```DUMMY VARIABLE, STILL TO BE CORRECTLY SET```.


## Usage
Depending on the data you want to send to the IoT Hub you'll have to edit the message variables to be send out. An easy example is already given in both cases, adjusting this speaks for itself. In the Python file this example is created and send in the _run_telemetry_sample_ function, while in the C# file this example is created in the _SendDeviceToCloudMessagesAsync_ function.

Once the data is successfully sent, you should see a message in the terminal like: 
```
$ 2/25/2022 3:04:50 PM > Sending message: {"type":"feature","id":"110AF1844EA0","properties":{"client":"Embassy","accuracy":74,"battery":"89%","color":"black","dateTime":"2022-02-25T15:04:49\u002B01:00"},"geometry":{"type":"Point","coordinates":[78.011578, 34.357068]}}
```
If you have an integration with Azure and Wapice IoT-TICKET your device and accompanying data should show up in the device overview. From there, dashboards can be created that react in real-time on the data received.


## Contact
Kilian van Berlo - S5436737 - k.vanberlo@student.tudelft.nl

Project Link: https://github.com/KilianBerlo/LOCI


## Acknowledgements
- https://try.iot-ticket.com
- https://github.com/Azure-Samples/azure-iot-samples-csharp
- https://github.com/Azure/azure-iot-sdk-python
