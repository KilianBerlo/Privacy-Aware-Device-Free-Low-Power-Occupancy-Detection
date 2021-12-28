def main():
    ## Show available ports ##
    print("\nAvailable ports: ")
    for i in range(len(list_ports.comports())):
        print(str(i+1) + " " + str(list_ports.comports()[i]) + "\n")

    ## Set up the serial connection to the desired port ##
    ser = serial.Serial(port='/dev/ttyUSB0',baudrate=256000,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=5)
    print("Connected to: " + ser.portstr)

    ## read data from the LOCI and write it to a file ##
    while True:
        try:
            ser.write(b'\x01')
            line = str(ser.read())
            if line:
                file1 = open("testFile.txt", "a") 
                # if r"b'\x" in line:
                file1.write(line + "\n")
                file1.close()
        except KeyboardInterrupt:
            sys.exit()

    ser.close()
    sys.exit()

if __name__ == "__main__":
    import serial, sys
    from serial.tools import list_ports
    main()