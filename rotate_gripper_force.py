from actuation.communication.modbus_RTU_client import ModbusRTUClient
#from pymodbus.client.sync import ModbusSerialClient
from actuation.gripper import Gripper
from actuation.cylinder import Cylinder
from actuation.rotating_gripper import RotatingGripper
#import pigpio 

import time
import tty, sys, termios

filedescriptors = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)
x = 0
 
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
#     pi.write(gpio,0)
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

    init(gripper,cylinder,rotating_gripper)
    rotating_gripper.set_force(50)
    setup_work(gripper,cylinder,rotating_gripper)
    #init_signal_send(pi)
    
    rotating_gripper.init()
    time.sleep(0.5)
    
    print("for cloce gripper press a ")
    print("for open gripper press s ")
    print("for cloce gripper steps press d ")
    print("for open  gripper steps press f ")

    rotating_gripper.set_rotational_speed(100)
    time.sleep(0.5)
    #rotating_gripper.relative_rotation_angle(angle = 5000)
    #time.sleep(5)
    angle = 0
    while True:
     #   process_signal_wait(pi)#1 grab_pre

        #Open process        
        # print("gripper full close")
        # rotating_gripper.position(0)
        # time.sleep(1)
        # print("gripper full open")
        # rotating_gripper.position(1000)
        # time.sleep(1)
        
        # rotating_gripper.set_rotational_force(50)
        # rotating_gripper.relative_rotation_angle(angle = 100)
        # time.sleep(1)
        # rotating_gripper.set_rotational_force(100)
        # rotating_gripper.relative_rotation_angle(angle = 360)
        # time.sleep(1)
        
        x=sys.stdin.read(1)[0]
        
        if x == "a":
            print("gripper full close")
            rotating_gripper.position(0)
            Gripper_location = 0
        if x == "s":
            print("gripper full open")
            rotating_gripper.position(1000)
            Gripper_location = 1000
        if x == "f":
            Gripper_location += 10
            if Gripper_location>1000 :
                Gripper_location = 1000 
            print("opening loc ", Gripper_location)
            rotating_gripper.position(Gripper_location)
            
        if x == "d":
            Gripper_location -= 10
            if Gripper_location<0 :
                Gripper_location = 0
            print("closing loc ", Gripper_location)
            rotating_gripper.position(Gripper_location)
            
        if x == "g":
            rotating_gripper.relative_rotation_angle(angle = 1)
            angle += 1
            print("rotating angle + = ", angle)
            
        if x == "h":
            rotating_gripper.relative_rotation_angle(angle = -1)
            angle -= 1
            print("rotating angle - = ", angle)
                 
            
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)  

