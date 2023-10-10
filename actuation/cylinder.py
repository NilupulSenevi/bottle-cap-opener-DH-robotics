# from communication.modbus_RTU_client import ModbusRTUClient
from .communication import modbus_RTU_client
import time

class Cylinder:
    def __init__(self, client, unit):
        self.client = client
        self.unit = unit

    def init(self):
        self.client.write_register(address=256,  value = 1, unit=self.unit)

    def location(self, location): 
        value = location
        self.client.write_register(address=259,  value = location, unit=self.unit)

    def set_push_pressure(self,ratio):
        self.client.write_register(address=257,  value = ratio, unit=self.unit)

    def set_push_speed(self,ratio):
        self.client.write_register(address=777,  value = ratio, unit=self.unit)
        
    def set_maximum_speed(self,ratio):
        self.client.write_register(address=260,  value = ratio, unit=self.unit)


    #MCE don't have init feedback
    def check_init(self):
        # Read the status register of the gripper
        status = self.client.read_registers(address=512, count=1, unit=self.unit)
        # Check if status indicates successful initialization
        if status.registers[0] != 1:
        # isinstance(status, ReadHoldingRegistersResponse):
            print("not initialized!!")
            return False      
        else:
            print("I'm ready!" )
            return True

    def check_operational_status(self): #Grip status feedback
        # Read the status register of the gripper
        status = self.client.read_registers(address=513, count=1, unit=self.unit)
        # Check if status indicates successful initialization
        if status.registers[0] == 0:  #0: in motion; 1: arriving at position; 2: blocking rotation
            print("Cylinder in motion!!")
            return False
        elif status.registers[0] == 1:
            print("Cylinder arriving at position" )
            return True
        elif status.registers[0] == 2:
            print("Cylinder blocking motion" )
            return True
        
    def check_operational_status_no_msg(self): #Grip status feedback
        # Read the status register of the gripper
        status = self.client.read_registers(address=513, count=1, unit=self.unit)
        # Check if status indicates successful initialization
        if status.registers[0] == 0:  #0: in motion; 1: arriving at position; 2: blocking rotation
            return False
        elif status.registers[0] == 1:
            return True
        elif status.registers[0] == 2:
            return True

    
    def check_push_pressure(self):
        # Read the status register of the gripper
        value = self.client.read_registers(address=257, count=1, unit=self.unit)    
        return value
    
    def current_Feedback(self):
        # Read the status register of the gripper
        value = self.client.read_registers(address=516, count=1, unit=self.unit)    
        return value.registers[0]


if __name__ == "__main__":
    client = modbus_RTU_client.ModbusRTUClient()
    #initialize    
    cylinder =Cylinder(client,2)
    
    if not cylinder.check_init():
        cylinder.init()
        time.sleep(1)
        while not cylinder.check_init():
            time.sleep(1)
    
    cylinder.location(location=0)
    # cylinder.absolute_angle(angle=0)
    
    while not cylinder.check_operational_status():
        time.sleep(0.1)