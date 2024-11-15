from dexarm import Dexarm

# Replace with the appropriate serial port for your DexArm
SERIAL_PORT = "COM3"  # Update to your serial port, e.g., /dev/ttyUSB0 on Linux/Mac

# Connect to the DexArm
dexarm = Dexarm(SERIAL_PORT)

try:
    # Initialization commands for 3D printing
    gcode_commands = [
        "M104 S200",      # Set extruder temperature to 200°C
        "M140 S60",       # Set bed temperature to 60°C
        "G28",            # Home all axes
        "G21",            # Set units to millimeters
        "G92 E0",         # Zero the extruder
        "M109 S200",      # Wait for extruder temperature
        "M190 S60",       # Wait for bed temperature
        "G1 Z0.2 F1200",  # Move to the first layer height
        "G92 E0"          # Reset extrusion distance
    ]

    # Send initialization G-code commands
    for command in gcode_commands:
        dexarm.send_cmd(command)
        print(f"Sent: {command}")

    # G-code to print a circular layer
    radius = 20.0  # Radius of the circle in mm
    center_x = 100.0  # X-coordinate of the circle center
    center_y = 100.0  # Y-coordinate of the circle center
    feedrate = 1200  # Movement speed in mm/min
    extrusion_amount = 0.1  # Extrusion amount per circle

    circle_gcode = [
        f"G0 X{center_x + radius} Y{center_y} Z0.2 F{feedrate}",  # Move to starting point
        f"G2 X{center_x + radius} Y{center_y} I{-radius} J0 E{extrusion_amount}"  # Draw a circle
    ]

    # Send circle G-code commands
    for command in circle_gcode:
        dexarm.send_cmd(command)
        print(f"Sent: {command}")

    print("Circular layer print complete.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the connection
    dexarm.close()

    