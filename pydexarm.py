import serial
import re

class Dexarm:

    def __init__(self, port,baud=115200):
        self.ser = serial.Serial(port, baud, timeout=None)
        self.is_open = self.ser.isOpen()
        if self.is_open:
            print('pydexarm: %s open' % self.ser.name)
        else:
            print('Failed to open serial port')

    def _send_cmd(self, data):
        self.ser.write(data.encode())
        while True:
            str = self.ser.readline().decode("utf-8")
            if len(str) > 0:
                if str.find("ok") > -1:
                    print("read ok")
                    break
                else:
                    print("read：", str)
                    
    def go_home(self):
        self._send_cmd("M1112\r")

    def go_home_G(self):
        self._send_cmd("G28\r")

    def set_workorigin(self):
        self._send_cmd("G92 X0 Y0 Z0 E0\r")

    def set_acceleration(self, acceleration, travel_acceleration, retract_acceleration=60):
        cmd = "M204"+"P" + str(acceleration) + "T"+str(travel_acceleration) + "T" + str(retract_acceleration) + "\r\n"
        self._send_cmd(cmd)

    def set_module_kind(self, kind):
        self._send_cmd("M888 P" + str(kind) + "\r")

    def get_module_kind(self):
        self.ser.write('M888\r'.encode())
        while True:
            str = self.ser.readline().decode("utf-8")
            if len(str) > 0:
                if str.find("PEN") > -1:
                    module_kind = 'PEN'
                if str.find("LASER") > -1:
                    module_kind = 'LASER'
                if str.find("PUMP") > -1:
                    module_kind = 'PUMP'
                if str.find("3D") > -1:
                    module_kind = '3D'
            if len(str) > 0:
                if str.find("ok") > -1:
                    return module_kind

    def move_to(self, x, y, z, feedrate=2000):
        cmd = "G1"+"F" + str(feedrate) + "X"+str(x) + "Y" + str(y) + "Z" + str(z) + "\r\n"
        self._send_cmd(cmd)

    def fast_move_to(self, x, y, z, feedrate=2000):
        cmd = "G0"+"F" + str(feedrate) + "X"+str(x) + "Y" + str(y) + "Z" + str(z) + "\r\n"
        self._send_cmd(cmd)

    def get_current_position(self):
        self.ser.write('M114\r'.encode())
        while True:
            str = self.ser.readline().decode("utf-8")
            if len(str) > 0:
                if str.find("X:") > -1:
                    temp = re.findall(r"[-+]?\d*\.\d+|\d+", str)
                    x = float(temp[0])
                    y = float(temp[1])
                    z = float(temp[2])
                    e = float(temp[3])
            if len(str) > 0:
                if str.find("DEXARM Theta") > -1:
                    temp = re.findall(r"[-+]?\d*\.\d+|\d+", str)
                    a = float(temp[0])
                    b = float(temp[1])
                    c = float(temp[2])
            if len(str) > 0:
                if str.find("ok") > -1:
                    return x,y,z,e,a,b,c

    """Delay"""
    def dealy_ms(self, value):
        self._send_cmd("G4 P" + str(value) + '\r')

    def dealy_s(self, value):
        self._send_cmd("G4 S" + str(value) + '\r')

    """SoftGripper & AirPicker"""
    def soft_gripper_pick(self):
        self._send_cmd("M1001\r")

    def soft_gripper_place(self):
        self._send_cmd("M1000\r")

    def soft_gripper_nature(self):
        self._send_cmd("M1002\r")

    def soft_gripper_stop(self):
        self._send_cmd("M1003\r")

    def air_picker_pick(self):
        self._send_cmd("M1000\r")

    def air_picker_place(self):
        self._send_cmd("M1001\r")

    def air_picker_nature(self):
        self._send_cmd("M1002\r")

    def air_picker_stop(self):
        self._send_cmd("M1003\r")

    """Laser"""
    def laser_on(self, value=0):
        self._send_cmd("M3 S" + str(value) + '\r')

    def laser_off(self):
        self._send_cmd("M5\r")

    """Conveyor Belt"""
    def conveyor_belt_forward(self, speed=0):
        self._send_cmd("M2012 S" + str(speed) + 'D0\r')
    def conveyor_belt_backward(self, speed=0):
        self._send_cmd("M2012 S" + str(speed) + 'D1\r')
    def conveyor_belt_stop(self, speed=0):
        self._send_cmd("M2013\r")
    
    """Direct G-code"""
    def g_code(self,code):
        self._send_cmd(code+'\r')
    
    """Enable/Disable Stepper"""
    # Enable Stepper M17 X Y Z
    # Disable Stepper M18 X Y Z
    def enable_stepper_all(self):
        self._send_cmd('M17  X Y Z'+'\r')
    def disable_stepper_all(self):
        self._send_cmd('M18  X Y Z'+'\r')
        
    def disconnect(self):
        self.ser.close()
        
        
    def quick_stop(self): #Stop all steppers instantly
        self._send_cmd('M410'+'\r')
        
    def emergency_stop(self): #A reset is required to return to operational mode
        self._send_cmd('M112'+'\r')
        
        
    """magnetic encoder value """    
       
    def get_mag_encoder(self):
        self.ser.write('M895\r'.encode())
        while True:
            str = self.ser.readline().decode("utf-8")
            if len(str) > 0:
                if str.find("X:") > -1:
                    temp = re.findall(r"[-+]?\d*\.\d+|\d+", str)
                    x = float(temp[0])
                    y = float(temp[1])
                    z = float(temp[2])
                   
                if len(str) > 0:
                    if str.find("ok") > -1:
                        return x,y,z
    def go_to_custom_home(self, x, y, z, feedrate=2000):
        '''
        Move the DexArm to a custom home position.
        :param x: Target X coordinate
        :param y: Target Y coordinate
        :param z: Target Z coordinate
        :param feedrate: Speed of the movement (default: 2000)
        '''
        cmd = f"G1 X{x} Y{y} Z{z} F{feedrate}\r\n"
        self._send_cmd(cmd)
        print(f"Moved to custom home: X={x}, Y={y}, Z={z}")
                    
            
        
        
        
"""
    New Version (for firmware V2.2.0 and above)
M895 inversely obtains the front end module position via the magnetic encoder value and the module off-set value. 
M896 moves to a specified position under Fast, Line, Jump moving mode.
P0-2, corresponding to the three moving modes of Fast, Line, and Jump respectively. The default is Fast mode.
Fast mode corresponds to G0 or M2001,
Line mode corresponds to G1 or M2000, added over-limit detection of interpolation points during line mode, 
Jump mode is divided into three steps, from the current position to raise the height of H, move horizontally to the target position, and move vertically to the target position.
F corresponds to the moving speed, H corresponds to Jump height, the F default value is 3000unit/min, the H default value is 50mm. 

SampleObtain the current position
Send: ​M895​
recv: ​X:0.00 Y:320.00 Z:0.00​
Set to tech&play and setup JUMP height, ​M896 P2 F5000 H20, ​Move to the target position, ​M896 X0 Y320 Z0
"""