from actuation.communication.modbus_RTU_client import ModbusRTUClient
from actuation.gripper import Gripper
from actuation.cylinder import Cylinder
from actuation.rotating_gripper import RotatingGripper
import socket 
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
    rotating_gripper.absolute_angle(angle=90)

def catch_work(gripper):
    gripper.location(10)
    time.sleep(1)

def release_work(gripper):
    gripper.location(1000)
    time.sleep(1)

def grab_cap(cylinder,rotating_gripper):
    cylinder.location(location = 5000)
    # cylinder.location(location = 4200)
    cylinder.set_maximum_speed(100)
    time.sleep(1)
    rotating_gripper.position(position = 200)
    time.sleep(0.5)

def release_cap(cylinder,rotating_gripper):
    rotating_gripper.position(position = 1000)
    time.sleep(1)
    cylinder.location(location = 0)
    time.sleep(0.5)

def open_cap(cylinder,rotating_gripper):
    rotating_gripper.set_rotational_speed(100)
    time.sleep(1)
    gripper.location(600)
    cylinder.set_maximum_speed(100)
    time.sleep(0.5)
    cylinder.location(5000)
    time.sleep(0.5)
    rotating_gripper.position(100)
    time.sleep(0.5)

    cylinder.set_maximum_speed(12)    # calc
    tcheck = int(round(time.time() * 1000))   # count start
    rotating_gripper.relative_rotation_angle(740)
    cylinder.location(4400)
    while True:
        if rotating_gripper.check_rotation_status() == False:
            print(int(round(time.time() * 1000)) - tcheck) # count end print
        if cylinder.check_operational_status() == False:
            print(int(round(time.time() * 1000)) - tcheck)
        if cylinder.check_operational_status() == True and rotating_gripper.check_rotation_status() == True:
            print("break while", int(round(time.time() * 1000)) - tcheck)
            break
            # if cylinder.check_operational_status() == False:
            #     print(int(round(time.time() * 1000)) - tcheck)
            #     continue
            # if  rotating_gripper.check_rotation_status() == True:
            #     print("break while", int(round(time.time() * 1000)) - tcheck)
            #     break

            
    time.sleep(1)
    cylinder.set_maximum_speed(100)
    cylinder.location(0)
           

def close_cap(cylinder,rotating_gripper):
    
    cylinder.location(4400)
    time.sleep(2)
    cylinder.set_maximum_speed(12)                 
    rotating_gripper.relative_rotation_angle(-720)
    cylinder.location(5000)
                     
    time.sleep(0.5)
    rotating_gripper.position(1000)
    time.sleep(0.5)
    cylinder.set_maximum_speed(100)
    cylinder.location(0)
    rotating_gripper.absolute_angle(angle=90)
    

    # print( "End Capping")

    
def start_server(gripper, cylinder, rotating_gripper):
    host = '192.168.1.15'
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)

    print(f'Server started at {host}:{port}')

    try:
        while True:
            conn, addr = s.accept()
            print(f'Connected to {addr}')
            
            while True:
                try:
                    data = conn.recv(1024).decode('utf-8')
                    if not data:
                        break
                    print("Received:", data)

                    if data == "INIT":
                        init(gripper,cylinder, rotating_gripper)
                        release_cap(cylinder, rotating_gripper)
                        release_work(gripper)
                        rotating_gripper.absolute_angle(angle=90)

                    elif data == "CATCH_WORK":
                        catch_work(gripper)
                    elif data == "RELEASE_WORK":
                        release_work(gripper)
                    elif data == "GRAB_CAP":
                        grab_cap(cylinder, rotating_gripper)
                    elif data == "RELEASE_CAP":
                        release_cap(cylinder, rotating_gripper)
                    elif data == "OPEN_CAP":
                        open_cap(cylinder, rotating_gripper)
                    elif data == "CLOSE_CAP":
                        close_cap(cylinder, rotating_gripper)
                    else:
                        response = "NO_COMMAND"
                    response = "DONE"
                except Exception as e:
                    response = f"ERROR: {str(e)}"

                conn.sendall(response.encode('utf-8'))

    except KeyboardInterrupt:
        print("Server is shutting down...")
    finally:
        conn.close()
        print("Connection with client closed.")
        s.close()
        print("Server socket closed.")

if __name__ == "__main__":
    client = ModbusRTUClient()
    gripper = Gripper(client,1)
    cylinder = Cylinder(client,2)
    rotating_gripper =RotatingGripper(client,3)

    init(gripper,cylinder,rotating_gripper)
    setup_work(gripper,cylinder,rotating_gripper)
    start_server(gripper,cylinder,rotating_gripper)