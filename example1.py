from actuation.communication.modbus_RTU_client import ModbusRTUClient
from actuation.gripper import Gripper
from actuation.cylinder import Cylinder
from actuation.rotating_gripper import RotatingGripper


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
        time.sleep(1)#ãããªã

actuation.operate_lid(grab,cylinder,rotating_gripper)
#actuation.operate_lid(grab)

#transfer_work()
#actuation.init_signal_send()

if __name__ == "__main__":
    client = ModbusRTUClient()
    gripper = Gripper(client,1)
    cylinder = Cylinder(client,2)
    rotating_gripper =RotatingGripper(client,3)
 
    init(gripper,cylinder,rotating_gripper)
    setup_work(gripper,cylinder,rotating_gripper)

    operate_lid("open",cylinder,rotating_gripper)


