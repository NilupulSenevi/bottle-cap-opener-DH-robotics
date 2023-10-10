from actuation.communication.modbus_RTU_client import ModbusRTUClient
#from pymodbus.client.sync import ModbusSerialClient
from actuation.gripper import Gripper
from actuation.cylinder import Cylinder
from actuation.rotating_gripper import RotatingGripper
from rich.console import Console
from rich.table import Table
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

def show_key_map():
    table = Table(title="Key Map for Bottle Capping/ De-Capping System Operation")

    table.add_column("Tool/Function", style="cyan", no_wrap=True)
    table.add_column("Key", style="magenta")
    table.add_column("Action",justify="center", style="green")

    table.add_row("Cylinder", "+", "Move down")
    table.add_row("        ", "-", "Move up")
    table.add_row()
    table.add_row("Gripper", "z", "Full Close")
    table.add_row("        ", "x", "Full Open")
    table.add_row("        ", "c", "Open steps")
    table.add_row("        ", "v", "Close steps")
    table.add_row()
    table.add_row("Rotary Gripper", "a", "Full Close")
    table.add_row("        ", "s", "Full Open")
    table.add_row("        ", "d", "Open steps")
    table.add_row("        ", "f", "Close steps")
    table.add_row("        ", "g", "Rotate CW")
    table.add_row("        ", "h", "Rotate CCW")
    table.add_row()
    table.add_row("Set home position", "i", "Set to home position and calibrate")
    table.add_row()
    table.add_row("Run Capping/ De-Capping example", "e", "Automated capping and decapping ")
    table.add_row("        ", " ", "based on user input parameters")
    table.add_row()
    table.add_row("show key map", "o", "show keymap again")

    table1 = Table(title="Capping/ De-Capping example")
    
    console = Console()
    #console.print(table, justify="center")
    console.print(table)
    

if __name__ == "__main__":
    client = ModbusRTUClient()
    gripper = Gripper(client,1)
    cylinder = Cylinder(client,2)
    rotating_gripper =RotatingGripper(client,3)

    init(gripper,cylinder,rotating_gripper)
    rotating_gripper.set_force(50)
    setup_work(gripper,cylinder,rotating_gripper)
    #init_signal_send(pi)
    

    angle = 0
    cylinder_location = 0
    threadgap = 600
    totrotangle = 470
    show_key_map()
    
    while True:        
        x=sys.stdin.read(1)[0] #get user keyboard inputs
        
############# cylinder
        if x == "+":
            cylinder_location += 10
            if cylinder_location>5000 :
                cylinder_location = 5000
            print("come down loc ", cylinder_location)
            cylinder.location(cylinder_location)
            
        if x == "-":
            cylinder_location -= 10
            if cylinder_location<0 :
                cylinder_location = 0
            print("come up loc ", cylinder_location)
            cylinder.location(cylinder_location)
            
#############   gripper
        if x == "z":
            print("gripper full close")
            gripper.location(0)
            Gripper_location = 0
        if x == "x":
            print("gripper full open")
            gripper.location(1000)
            Gripper_location = 1000
        if x == "v":
            Gripper_location += 10
            if Gripper_location>1000 :
                Gripper_location = 1000 
            print("opening loc ", Gripper_location)
            gripper.location(Gripper_location)
            
        if x == "c":
            Gripper_location -= 10
            if Gripper_location<0 :
                Gripper_location = 0
            print("closing loc ", Gripper_location)
            gripper.location(Gripper_location)
            
#############  rotation gripper
        
        if x == "a":
            print("gripper full close")
            rotating_gripper.position(0)
            Rot_Gripper_location = 0
        if x == "s":
            print("gripper full open")
            rotating_gripper.position(1000)
            Rot_Gripper_location = 1000
            
        if x == "f":
            Rot_Gripper_location += 10
            if Rot_Gripper_location>1000 :
                Rot_Gripper_location = 1000 
            print("opening loc ", Rot_Gripper_location)
            rotating_gripper.position(Rot_Gripper_location)
            
        if x == "d":
            Rot_Gripper_location -= 10
            if Rot_Gripper_location<0 :
                Rot_Gripper_location = 0
            print("closing loc ", Rot_Gripper_location)
            rotating_gripper.position(Rot_Gripper_location)
            
        if x == "g":
            rotating_gripper.relative_rotation_angle(angle = 1)
            angle += 1
            print("rotating angle + = ", angle)
            
        if x == "h":
            rotating_gripper.relative_rotation_angle(angle = -1)
            angle -= 1
            print("rotating angle - = ", angle)
            
############# go home
        if x == "i":
            gripper.init()
            cylinder.init()
            rotating_gripper.init()
            print("home position")
############# show key map
        if x == "o":
            show_key_map()
            
#############        
        if x == "e":
           #first come to home position
           
           print("Capping/ De-Capping demo")
           gripper.init()
           cylinder.init()
           rotating_gripper.init()
           
           #if need to run with fixed parameters uncomment and assing realvant values 
           #threadgap = 600  ### 6 mm
           #totrotangle = 720  ## 700 degrees 
           #speed = 20 
           
           #if need to run with user input parameters uncomment below 
           #get the user input for thread engagement
           threadgapS = input("Enter the thread engagement(<5000): ")
           threadgap = int(threadgapS)
           print("\n Thread engagement set = ", threadgap)
           
           #get the user input for total rotational angle          
           totrotangleS = input("Enter total rotational angle of the thread(>100degree) : ")
           totrotangle = int(totrotangleS)
           print("\n Total rotational angle set = ", totrotangle)
           
           #get the user input for speed
           speedS = input("Enter rotational speed (1~100) : ")
           speed = int(speedS)
           print("\n Rotational speed set = ", speed)
           
           
           
           inc_perdec = threadgap/totrotangle
           print( "Calculated linear increment per 1 degree rotation = ", inc_perdec)
           time.sleep(0.5)
           
           rotating_gripper.set_rotational_speed(speed)
           time.sleep(0.5)
           #rotating_gripper.relative_rotation_angle(10000)
           
           print( "Start De-Capping /Put bottle...")
           time.sleep(3)
           gripper.location(600)
           time.sleep(0.5)
           cylinder.location(5000)
           time.sleep(0.5)
           rotating_gripper.position(100)
           time.sleep(0.5)
           
           
           totrotangleI = round(totrotangle/speed)
           for i in range(totrotangleI):
                rotating_gripper.relative_rotation_angle(angle = 1*speed)
                inc_perdecI = round(5000-(inc_perdec*i*speed))
                print(inc_perdecI)
                cylinder.location(inc_perdecI)
                time.sleep(0.1)
           time.sleep(0.5)
           cylinder.location(500)
           print( "End De-Capping")
           
           print( "Do you want to cap the bottle again(y/n)")
           while True:
               x=sys.stdin.read(1)[0]
               if x == "y":
                    print( "Start Capping...")
                    time.sleep(1)
                    cylinder.location(5000-threadgap)
                    time.sleep(0.5)
                    for i in range(totrotangleI):
                        rotating_gripper.relative_rotation_angle(angle = -1*speed)
                        inc_perdecI = round((5000-threadgap)+(inc_perdec*i*speed))
                        print(inc_perdecI)
                        cylinder.location(inc_perdecI)
                        time.sleep(0.1)
                    time.sleep(1)
                    rotating_gripper.position(1000)
                    time.sleep(0.5)
                    cylinder.location(0)
                    print( "End Capping")
                    break
                
               if x == "n":
                    print("Go home position")
                    gripper.init()
                    cylinder.init()
                    rotating_gripper.init()
                    break
           

            
                

        
                 
            
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)  

