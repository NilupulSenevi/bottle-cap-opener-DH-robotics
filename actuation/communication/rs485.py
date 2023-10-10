import serial
import time

# Create a serial object
ser = serial.Serial('/dev/ttyACM0')

def send_data(data):
    """
    Function to send data over RS485
    """
    # Convert string data to bytes
    data_bytes = data.encode('utf-8')

    # Write data to the serial port
    ser.write(data_bytes)

def read_data():
    """
    Function to read data from RS485
    """
    # Wait for data to be available
    while ser.inWaiting() == 0:
        pass

    # Read data from the serial port
    data_bytes = ser.read(ser.inWaiting())

    # Convert bytes to string
    data = data_bytes.decode('utf-8')

    return data

def create_data(command, value):
    """
    Create a byte array to send over RS485.
    """
    # Start byte
    data = [0x02]

    # Command byte
    data.append(command)

    # Value bytes
    data.append((value >> 8) & 0xFF)  # High byte
    data.append(value & 0xFF)         # Low byte

    # End byte
    data.append(0x03)

    # Convert list to byte array
    data_bytes = bytearray(data)

    return data_bytes


def parse_data(data_bytes):
    """
    Parse a byte array received over RS485.
    """
    # Check start and end bytes
    if data_bytes[0] != 0x02 or data_bytes[-1] != 0x03:
        raise ValueError("Invalid data format")

    # Extract command and value
    command = data_bytes[1]
    value = (data_bytes[2] << 8) | data_bytes[3]  # Combine high and low bytes

    return command, value


# Example usage
send_data("Hello World!")
time.sleep(1)
print(read_data())

ser.close()