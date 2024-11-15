from pydexarm import Dexarm

# Initialize DexArm on the specified port


dexarm = Dexarm("COM5")  # Replace "COM5" with your port

# Set a custom home position
custom_home_x = 0
custom_home_y = 300
custom_home_z = -50
dexarm.go_to_custom_home(custom_home_x, custom_home_y, custom_home_z)

# Close the connection
dexarm.disconnect()