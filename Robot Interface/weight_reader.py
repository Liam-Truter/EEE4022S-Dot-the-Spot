
import serial.tools.list_ports
class Weight_reader:
    def __init__(self):
        self.last_received = ''
        self.buffer = ''
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
                print(port)

        self.serial_connection.baudrate = 57600
        self.serial_connection.port = port
        self.serial_connection.open()
        while True:
            if self.serial_connection.in_waiting:
                line = self.serial_connection.readline().decode('utf-8').rstrip('\n\r')
                print(line)
                if line == "Startup is complete":
                    break

    def get_weight(self) -> float:
        """"
        if self.serial_connection.inWaiting:
            self.buffer = self.buffer + self.serial_connection.read(self.serial_connection.inWaiting()).decode('utf-8')
        if '\n' in self.buffer:
            lines = self.buffer.split('\n')
            self.last_received = lines[-2]
            self.buffer = lines[-1]
        items = self.last_received.split()
        if len(items) > 0:
            if items[0] == "Load_cell":
                self.last_weight = float(items[-1])
        print(self.last_weight)
        return self.last_weight
        
        lines = self.serial_connection.readlines()
        line = lines[-1].decode('utf-8')
        line_split = line.split()
        if len(line_split)>0:
            if line_split[0] == "Load_cell":
                self.last_weight = float(line_split[-1])
                print(f"Load cell: {self.last_weight:.2f}g")
                return self.last_weight
        """
        self.serial_connection.write(b'r')
        self.last_weight = float(self.serial_connection.readline().decode('utf-8'))
        return self.last_weight