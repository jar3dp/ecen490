import imp

rc = imp.load_source('roboclaw', '/home/odroid/Documents/VectorKrum/RobotSoccer/MotionControl/scripts/motor_control/roboclaw.py')

import serial


#rc.M1Forward(0x80,0)
rc.M1Forward(0x81,0)

while 1:
    print rc.readM1encoder(0x81)


# rc.M2Forward(0x80, 10)

#Get version string
# rc.sendcommand(128,21)
# rcv = port.read(32)
# print repr(rcv)
#

