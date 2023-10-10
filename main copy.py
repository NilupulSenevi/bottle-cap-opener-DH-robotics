from actuation.communication.modbus_RTU_client import ModbusRTUClient
#from pymodbus.client.sync import ModbusSerialClient
from actuation.gripper import Gripper
from actuation.cylinder import Cylinder
from actuation.rotating_gripper import RotatingGripper
import pigpio 
 
import time

def init(gripper,cylinder,rotating_gripper):
    if not gripper.check_init(): 
        gripper.init()
        time.sleep(1)
        while not gripper.check_init():
            time.sleep(1)

    if not cylinder.check_init():
        cylinder.init()
        time.sleep(1)
        while not cylinder.check_init():
            time.sleep(1)
    
    if not rotating_gripper.check_init():
        rotating_gripper.init()
        time.sleep(1)
        while not rotating_gripper.check_init():
            time.sleep(1)

def setup_work(gripper,cylinder,rotating_gripper):
    gripper.location(location=1000)
    cylinder.location(location=0)
    rotating_gripper.position(position=1000)
    rotating_gripper.absolute_angle(angle=0)

def handle_and_move_work(operate, ):
    pass

def transfer_work(operate,gripper):
    gripper.location(location=100)

def operate_lid(operate,cylinder,rotating_gripper):
    print(operate)
    if operate == "grab":
        cylinder.location(location = 4200)
        time.sleep(1)
        rotating_gripper.position(position = 200)
        time.sleep(0.5)
    elif operate == "release":
        rotating_gripper.position(position = 1000)
        time.sleep(1)
        cylinder.location(location = 0)
        time.sleep(0.5)
    elif operate == "open":        
        rotating_gripper.relative_rotation_angle(angle = 1440)
        time.sleep(0.5)
        cylinder.location(location = 3000) #jog?
        time.sleep(1)#よくない
        cylinder.location(location = 0)
        time.sleep(1)#よくない 上がりきったことを確認
    elif operate == "close":
        cylinder.location(location = 3500)
        time.sleep(0.5)
        rotating_gripper.relative_rotation_angle(angle = -1300)
        time.sleep(0.5)
        cylinder.location(location = 4200)
        rotating_gripper.relative_rotation_angle(angle = -140)
        # rotating_gripper.relative_rotation_angle(angle = -650)
        time.sleep(0.5)

def process_signal_ON(pi,gpio):
    pi.write(gpio,1)
    return
def process_signal_OFF(pi,gpio):
    pi.write(gpio,0)
    return

def init_signal_send(pi):
    process_signal_ON(pi,25)
    while pi.read(27) != True:
        time.sleep(1)
    process_signal_OFF(pi,25)
    print("start")
    return

def process_signal_wait(pi):
    while pi.read(17) != True:
        time.sleep(1)
    process_signal_ON(pi,24)
    while pi.read(17) != False:
        time.sleep(1)
    process_signal_OFF(pi,24)
    print("STOP")
    return

def process_signal_send(pi):
    process_signal_ON(pi,24)
    while pi.read(17) != True:
        time.sleep(1)
    process_signal_OFF(pi,24)
    while pi.read(17) != False:
        time.sleep(0.5)
    print("STOP")
    return 

if __name__ == "__main__":
    client = ModbusRTUClient()
    gripper = Gripper(client,1)
    cylinder = Cylinder(client,2)
    rotating_gripper =RotatingGripper(client,3)
    pi = pigpio.pi()
    process_signal_OFF(pi,24)
    pi.set_mode(17, pigpio.INPUT)
    pi.set_mode(24, pigpio.OUTPUT)
    pi.set_pull_up_down(24, pigpio.PUD_DOWN)

    init(gripper,cylinder,rotating_gripper)
    setup_work(gripper,cylinder,rotating_gripper)
    init_signal_send(pi)
    while True:
        process_signal_wait(pi)#1 grab_pre

        #Open process        
        print("grab")
        gripper.location(10)
        process_signal_wait(pi)#2 grab_post
        process_signal_wait(pi)#3 MG400_safe
        
        operate_lid("grab",cylinder,rotating_gripper)
        # process_signal_wait(pi)#4 
        
        operate_lid("open",cylinder,rotating_gripper)
        process_signal_wait(pi)#4 open
        process_signal_wait(pi)#5 MG400Grab
        # process_signal_wait(pi)#6
        # process_signal_wait(pi)#8
        print("release")
        gripper.location(1000)
        process_signal_wait(pi)#6 release
        

        #Close process
        process_signal_wait(pi)#7 grab_pre
        print("grab")
        gripper.location(10)
        process_signal_wait(pi)#8 grab_post
        process_signal_wait(pi)#9 MG400_safe

        operate_lid("close",cylinder,rotating_gripper)
        operate_lid("release",cylinder,rotating_gripper)
        process_signal_wait(pi)#10 close
        process_signal_wait(pi)#11 MG400grab
        
        gripper.location(1000)
        process_signal_wait(pi) #12

        # time.sleep(1)
        # process_signal_ON(pi,24)
        # time.sleep(2)
        # while process_signal_wait(pi,17) != True:
        #     time.sleep(1)
        # process_signal_OFF(pi,24)