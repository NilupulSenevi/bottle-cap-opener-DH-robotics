from .communication import modbus_RTU_client
import time
class RotatingGripper:
    def __init__(self, client, unit):
        self.client = client
        self.unit = unit

    # def init(self, client,unit):
    def init(self):
        self.client.write_register(address=256,  value = 1, unit=self.unit)

    def position(self,position): 
        self.client.write_register(address=259,  value = position, unit=self.unit)

    def absolute_angle(self, angle):
        self.client.write_register(address=261,  value = angle, unit=self.unit)


    def relative_rotation_angle(self, angle):
        #Hex signed 2's complement
        num = angle  # Convert hex to decimal
        if num >= 2**(16-1):  # If the highest bit is set
            num -= 2**16  # Subtract 2^bit_length

        self.client.write_register(address=265,  value = num, unit=self.unit)
        
        

## set param##
    def set_force(self,ratio):
        self.client.write_register(address=257,  value = ratio, unit=self.unit)
        
    def set_speed(self,ratio):
        self.client.write_register(address=258,  value = ratio, unit=self.unit)
        
    def set_rotational_force(self,ratio):
        self.client.write_register(address=259,  value = ratio, unit=self.unit)
        
    def set_rotational_speed(self,ratio):
        self.client.write_register(address=263,  value = ratio, unit=self.unit)

## check status##
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
    
    def check_rotation_status(self): #Rotation status feedback
            # Read the status register of the gripper
        status = self.client.read_registers(address=523, count=1, unit=self.unit)
        # Check if status indicates successful initialization
        if status.registers[0] == 0:      #0: in motion,1: reached position,2: blocked rotation
            print("rotation gripper in motion!!")
            return False
        elif status.registers[0] == 1:
            print("rotation gripper reached position" )
            return True
        elif status.registers[0] == 2:
            print("rotation gripper blocked position" )
            return False
        
    def check_rotation_status_no_msg(self): #Rotation status feedback
            # Read the status register of the gripper
        status = self.client.read_registers(address=523, count=1, unit=self.unit)
        # Check if status indicates successful initialization
        if status.registers[0] == 0:      #0: in motion,1: reached position,2: blocked rotation
            return False
        elif status.registers[0] == 1:
            return True
        elif status.registers[0] == 2:
            return False

    def check_force(self):
        # Read the status register of the gripper
        value = self.client.read_registers(address=257, count=1, unit=self.unit)    
        return value

if __name__ == "__main__":
    client = modbus_RTU_client.ModbusRTUClient()
    #initialize    
    rotating_gripper =RotatingGripper(client,3)
    
    if not rotating_gripper.check_init():
        rotating_gripper.init()
        time.sleep(1)
        while not rotating_gripper.check_init():
            time.sleep(1)
    
    # rotating_gripper.position(position=1000)
    # rotating_gripper.absolute_angle(angle=0)
    rotating_gripper.relative_rotation_angle(angle = 1000)
    
    while not rotating_gripper.check_rotation_status():
        time.sleep(0.1)

    rotating_gripper.position(position=0)
    while not rotating_gripper.check_clamping_status():
        time.sleep(0.1)
    # relative_rotation_angle(client=client,angle=100,unit=3)
    # time.sleep(2)
    # relative_rotation_angle(client=client,angle=300,unit=3)
    # position(client=client,location=0,unit=3)
    