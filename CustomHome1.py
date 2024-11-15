from pydexarm import Dexarm

# Initialize DexArm on the specified port
def go_to_custom_home(self, x, y, z, feedrate=2000):
    """
    Move the DexArm to a custom home position.
    :param x: Target X coordinate
    :param y: Target Y coordinate
    :param z: Target Z coordinate
    :param feedrate: Speed of the movement (default: 2000)
    """
    cmd = f"G1 X{x} Y{y} Z{z} F{feedrate}\r\n"
    self._send_cmd(cmd)
    print(f"Moved to custom home position: X={x}, Y={y}, Z={z}")
    
dexarm = Dexarm("COM5")  # Replace "COM5" with your port

# Set a custom home position
custom_home_x = 100
custom_home_y = 100
custom_home_z = 50
dexarm.go_to_custom_home(custom_home_x, custom_home_y, custom_home_z)

# Close the connection
dexarm.disconnect()