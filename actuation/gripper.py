from .communication import modbus_RTU_client
import time

class Gripper:
    def __init__(self, client, unit):
        self.client = client
        self.unit = unit

    def init(self):
        self.client.write_register(address=256,  value = 1, unit=self.unit)

    def location(self, location):
        value = location
        self.client.write_register(address=259,  value = location, unit=self.unit)

    
## set param##
    def set_power(self,ratio):
        self.client.write_register(address=257,  value = ratio, unit=self.unit)
        
    def set_speed(self,ratio):
        self.client.write_register(address=260,  value = ratio, unit=self.unit)

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
    
    
    def check_clamping_status(self): #Grip status feedback
            # Read the status register of the gripper
        status = client.read_registers(address=513, count=1, unit=self.unit)
        # Check if status indicates successful initialization
        if status.registers[0] == 0:  #0: in motion, 1: arriving at position; 2: clamping object;3: object falling
            print("in motion!!")
            return False
        elif status.registers[0] == 1:
            print("arriving at position" )
            return True
        elif status.registers[0] == 2:
            print("clamping object" )
            return True
        elif status.registers[0] == 3:
            print("object falling" )
            return False
    


if __name__ == "__main__":
    client = modbus_RTU_client.ModbusRTUClient()
    gripper = Gripper(client,3)    
    if not gripper.check_init():
        gripper.init()
        time.sleep(1)
        while not gripper.check_init():
            time.sleep(1)
    
    # gripper.position(position=1000)
    # gripper.absolute_angle(angle=0)
    gripper.location(location = 1000)
    
    while not gripper.check_location_status():
        time.sleep(0.1)
