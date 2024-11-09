import time
from pydexarm import Dexarm

# Initialize DexArm on the specified port (replace with your actual port)
dexarm = Dexarm("COM5")  # Replace "COM5" with the correct serial port

# Function to read and execute G-code from a file
def execute_gcode(file_path):
    with open("C:\\Users\\mario\\Documents\\University Stuff\\DexArm_Files\\g_code\\asd.txt", 'r') as file:
        for line in file:
            command = line.strip()  # Remove any leading/trailing whitespace
            
            # Ignore empty lines and comments (G-code comments often start with ';')
            if not command or command.startswith(';'):
                continue
            
            print("Executing:", command)  # Optional: Print the command for debugging
            
            # Send the G-code command to DexArm
            dexarm.g_code(command)
            
            # Optional: Small delay to ensure commands are executed sequentially
            time.sleep(0.1)

# Send the DexArm to the home position before starting
dexarm.go_home()

# Execute G-code file
execute_gcode("C:\\Users\\mario\\Documents\\University Stuff\\DexArm_Files\\g_code\\asd.txt")  # Replace with your G-code file path

# Return DexArm to the home position after finishing
dexarm.go_home()

# Close the connection
dexarm.disconnect()