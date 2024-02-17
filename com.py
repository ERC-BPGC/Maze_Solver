import serial
import time

def arduino(data):
    try:
        print("Connecting to arduino")
        # Replace 'COM9' with the actual COM port of your Arduino
        with serial.Serial('COM9', 9600, timeout=1) as ser:
            time.sleep(2)  # Wait for the Arduino to initialize (increased to 2 seconds)
            ser.write(str(data).encode())
        print(f"Sent data to Arduino: {data}")

    except Exception as e:
        print(f"Error: {e}")

your_string = "ll"

for char in your_string:
    if char.lower() == 'f':
        arduino('7')  # Pass the command as a string
    elif char.lower() == 'b':
        arduino('6')  # Pass the command as a string
    elif char.lower() == 'l':
        arduino('5')  # Pass the command as a string
    elif char.lower() == 'r':
        arduino('4')  # Pass the command as a string
    elif char.lower() == 's':
        arduino('3')  # Pass the command as a string
    time.sleep(0.3)  # Introduce a small delay between commands to avoid potential issues
