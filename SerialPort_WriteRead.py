import serial
import datetime



SERIAL_PORT = 'COM' + input("Enter COM port number (e.g., COM7): ")


BAUD_RATE = input("Enter baud rate: ")

file_name = input("Save into (exclude '.txt'): ") + ".txt"

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

    with open(file_name, 'a') as file:
        print(f"Reading from {SERIAL_PORT} and writing to {file_name}")
        file.write("dataTag,Middle,Side,Top,Horizontal,Vertical,Pressure (mBar),Temperature (K),Altitude (m), Average Roll, Max Roll, Average Pitch, Max Pitch\n")
        
        while True:
        # Read line from serial port
            if ser.in_waiting > 0:
                # Get time
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                try:
                    data = ser.readline().decode('utf-8').strip()
                except UnicodeDecodeError as uni_e:
                    print(f"\n{timestamp} | Error - NOT wrote to SD: {uni_e}")
                    continue
                data = data[1:-1]  #Cut the brackets at both ends because it was sent in C-strings
                if data:
                    # put time before the data
                    output = f"{timestamp} | {data}"
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