import threading
import serial
import binascii

class recvData(threading.Thread):
    def __init__(self):
        super(recvData, self).__init__()

        self.listing = [] #the received data is put in a list

        #configure serial connection
        self.ser = serial.Serial(port='/dev/ttyUSB0',baudrate=256000,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)

    def run(self):              
        while len(self.listing) < 1664: #temporary for now just for 0x01, when 0x02 is going to be read it is to be changed to be continuous
            read = self.ser.read(self.ser.inWaiting())
            if read != b'':
                for i in range(0, len(binascii.hexlify(read).decode()), 2):
                    self.listing.append(binascii.hexlify(read).decode()[i: i+2])
        self.ser.close()
        print(self.listing)

class Base():
    def __init__(self):
        self.ser = recvData() 
        self.ser.start() #run thread

    def main(self):
        self.ser.ser.write(b'\x01')


if __name__ == '__main__':
    b = Base() 
    b.main()