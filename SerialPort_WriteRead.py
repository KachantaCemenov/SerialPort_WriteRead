import serial
import datetime
SERIAL_PORT = 'COM7'  
BAUD_RATE = 115200     
file_name = 'serial_output.txt'

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

try:
    with open(file_name, 'a') as file:
        print(f"Reading from {SERIAL_PORT} and writing to {file_name}")
        
        while True:
        # Read line from serial port
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                data = data[1:-1]  #Cut the brackets at both ends because it was sent in C-strings
                if data:
                    # Get time
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # put time before the data
                    output = f"{timestamp}, {data}"
                    # Write file
                    file.write(output+"\n")
                    file.flush()  
                    print(output)

except serial.SerialException as e:
    print(f"Serial port error: {e}")
except KeyboardInterrupt:
    print("\nStopped by user")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed")