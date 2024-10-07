
import serial.tools.list_ports
class Weight_reader:
    def __init__(self):
        self.connected = False
        self.last_weight = 0

    def __del__(self):
        self.serial_connection.close()
        print("Serial connection closed")

    def connect(self):
        ports = serial.tools.list_ports.comports()
        self.serial_connection = serial.Serial()

        for x in range(len(ports)):
            port_info = str(ports[x]).split()
            if port_info[2] == "Arduino":
                port = port_info[0]

        self.serial_connection.baudrate = 57600
        self.serial_connection.port = port
        self.serial_connection.open()
        while True:
            if self.connected:
                break
            if self.serial_connection.in_waiting:
                line = self.serial_connection.readline().decode('utf-8').rstrip('\n\r')
                print(line)
                if line == "Startup is complete":
                    self.connected = True
                    break
                elif line.startswith("Timeout"):
                    self.serial_connection.close()
                    self.connect()

    def get_weight(self) -> float:
        self.serial_connection.write(b'r')
        self.last_weight = float(self.serial_connection.readline().decode('utf-8'))
        return self.last_weight