# from pymodbus.client.sync import ModbusSerialClient
# from pymodbus.exceptions import ConnectionException

# import time
# class ModbusRTUClient:
#     def __init__(self, port='/dev/ttyACM0', baudrate=115200, bytesize=8, parity='N', stopbits=1):
#         self.client = ModbusSerialClient(
#             method='rtu',
#             port=port,
#             baudrate=baudrate,
#             bytesize=bytesize,
#             parity=parity,
#             stopbits=stopbits,
#         )

#     def read_registers(self, address, count, unit):
#         if not self.client.is_socket_open():
#             if not self.client.connect():
#                 print("Could not connect to MODBUS client.")
#                 return None

#         response = self.client.read_holding_registers(
#             address=address,
#             count=count,
#             unit=unit,
#         )

#         if not response.isError():
#             return response.registers
#         else:
#             print("MODBUS error: {}".format(response))
#             return None

#     def write_register(self, address, value, unit):
#         if not self.client.is_socket_open():
#             if not self.client.connect():
#                 print("Could not connect to MODBUS client.")
#                 return None

#         response = self.client.write_register(
#             address=address,
#             value=value,
#             unit=unit,
#         )

#         if not response.isError():
#             return True
#         else:
#             print("MODBUS error: {}".format(response))
#             return False


# # def grab(client, location, unit):
# #     value = location
# #     client.write_register(address=259,  value = location, unit=unit)

# # def release(client, unit):
# #     client.write_register(address=259, value = 0, unit=unit)

# # if __name__ == "__main__":
#     # client = ModbusRTUClient()
#     # # Reading registers
#     # registers = client.read_registers(address=0, count=10, unit=4)
#     # print(registers)
#     # # Writing to a register
#     # success = client.write_register(address=259, value=50, unit=1)
#     # print("Write success: ", success)
    
#     # client = ModbusRTUClient()
#     # release(client=client,unit=1)
#     # time.sleep(2)
#     # grab(client=client,location=500,unit=1)

from pymodbus.client import ModbusSerialClient
import struct
class ModbusRTUClient:
    def __init__(self, port='/dev/ttyACM0', baudrate=115200, stopbits=1, parity='N', bytesize=8):
        self.port = port
        self.baudrate = baudrate
        self.stopbits = stopbits
        self.parity = parity
        self.bytesize = bytesize
        self.client = ModbusSerialClient(
            method='rtu',
            port=self.port,
            baudrate=self.baudrate,
            stopbits=self.stopbits,
            parity=self.parity,
            bytesize=self.bytesize
        )

    def connect(self):
        return self.client.connect()

    def disconnect(self):
        self.client.close()

    def read_registers(self, address, count=1, unit=0):
        return self.client.read_holding_registers(address, count, slave=unit)
    
    def write_register(self, address, value, unit=0):
        if value < 0:  # if value is negative
            value = struct.unpack("H", struct.pack("h", value))[0]  # convert to unsigned 16-bit integer
        try:
            self.client.write_register(address, value, slave=unit)
        except Exception as e:
            print(f"Failed to write register: {e}")
        return
