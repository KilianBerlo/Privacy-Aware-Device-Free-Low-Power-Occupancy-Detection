// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.

using Microsoft.Azure.Devices.Client;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;

namespace mQTTDevice
{
    public class deviceProps{
        public int accuracy { get; set; }
        public string battery { get; set; }
        public string client { get; set; }
        public string color { get; set; }
        public string dateTime { get; set; }
    }

    public class dataset{
        public string type { get; set; }
        public double[] coordinates { get; set; }
    }

    internal class Program
    {
        private static DeviceClient s_deviceClient;
        private static readonly TransportType s_transportType = TransportType.Mqtt;

        // The device connection string to authenticate the device with your IoT hub.
        private static string s_connectionString = "HostName=geojson-ticket-hub.azure-devices.net;DeviceId=tudelft_device001;SharedAccessKey=6dCj+Nr3TqWAuuJ303DbpEqOheoXWNKi60ixbG3Dx2Q=";

        private static async Task Main(string[] args)
        {
            Console.WriteLine("IoT Hub Quickstarts #1 - Simulated device.");

            // This sample accepts the device connection string as a parameter, if present
            ValidateConnectionString(args);

            // Connect to the IoT hub using the MQTT protocol
            s_deviceClient = DeviceClient.CreateFromConnectionString(s_connectionString, s_transportType);

            // Set up a condition to quit the sample
            Console.WriteLine("Press control-C to exit.");
            using var cts = new CancellationTokenSource();
            Console.CancelKeyPress += (sender, eventArgs) =>
            {
                eventArgs.Cancel = true;
                cts.Cancel();
                Console.WriteLine("Exiting...");
            };

            // Run the telemetry loop
            await SendDeviceToCloudMessagesAsync(cts.Token);
            await s_deviceClient.CloseAsync();

            s_deviceClient.Dispose();
            Console.WriteLine("Device simulator finished.");
        }

        private static void ValidateConnectionString(string[] args)
        {
            if (args.Any())
            {
                try
                {
                    var cs = IotHubConnectionStringBuilder.Create(args[0]);
                    s_connectionString = cs.ToString();
                }
                catch (Exception)
                {
                    Console.WriteLine($"Error: Unrecognizable parameter '{args[0]}' as connection string.");
                    Environment.Exit(1);
                }
            }
            else
            {
                try
                {
                    _ = IotHubConnectionStringBuilder.Create(s_connectionString);
                }
                catch (Exception)
                {
                    Console.WriteLine("This sample needs a device connection string to run. Program.cs can be edited to specify it, or it can be included on the command-line as the only parameter.");
                    Environment.Exit(1);
                }
            }
        }

        // Async method to send simulated telemetry
        private static async Task SendDeviceToCloudMessagesAsync(CancellationToken ct)
        {

            while (!ct.IsCancellationRequested)
            {
                // Create JSON message
                string messageBody = JsonSerializer.Serialize(
                    new
                    {
                        type = "Feature",
                        id = "54:ee:75:57:b8:59",
                        properties = new deviceProps {accuracy = 100, battery = "85%", client = "TUDelft", color = "red", dateTime = DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ssZ")},
                        geometry = new dataset {type = "Point", coordinates = new[] {5.458188056945801, 51.41125257942182 }}
                    });
                using var message = new Message(Encoding.ASCII.GetBytes(messageBody))
                {
                    ContentType = "application/json",
                    ContentEncoding = "utf-8",
                };

                // Send the telemetry message
                await s_deviceClient.SendEventAsync(message);
                Console.WriteLine($"{DateTime.Now} > Sending message: {messageBody}");

                await Task.Delay(1000);
            }
        }
    }
}