import time
import pigpio
import RPi.GPIO as GPIO
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize pigpio and GPIO
pi = pigpio.pi()
if not pi.connected:
    exit()

GPIO.setmode(GPIO.BCM)
for pin in [12, 13, 18, 19]:
    GPIO.setup(pin, GPIO.OUT)

# Initialize the GUI window
root = tk.Tk()
root.title("Temperature Sensor GUI")

# Initialize global variables for sensor readings
sensor_readings = [0] * 20  # Store last 20 readings
latest_temp = tk.DoubleVar()  # Variable to display the latest reading

# Function to read sensor data
def read_sensor():
    global sensor_readings
    sensor = pi.spi_open(1, 1000000, 0)  # CE1, 1Mbps, main SPI
    c, d = pi.spi_read(sensor, 2)
    
    if c == 2:
        sign = (d[0] & 0x80) >> 7
        value = (((d[0] & 0x7f) << 8) | d[1]) >> 5
        temp = value * 0.125
        if sign == 1:
            temp = -temp
        latest_temp.set(temp)
        
        # Update the sensor readings list
        sensor_readings.pop(0)  # Remove oldest value
        sensor_readings.append(temp)  # Add new value

        # Update LEDs based on temperature
        for pin in [12, 13, 18, 19]:
            GPIO.output(pin, GPIO.LOW)
        
        if temp >= 24:
            GPIO.output(12, GPIO.HIGH)
        if temp > 26:
            GPIO.output(13, GPIO.HIGH)
        if temp > 27:
            GPIO.output(18, GPIO.HIGH)
        if temp > 29:
            GPIO.output(19, GPIO.HIGH)

    pi.spi_close(sensor)
    update_plot()
    root.after(250, read_sensor)  # Schedule the function to run every 250ms

# Function to update the plot with the latest readings
def update_plot():
    ax.clear()
    ax.plot(sensor_readings, marker='o')
    ax.set_ylim(20, 30)  # Adjust based on expected temperature range
    ax.set_title("Temperature Sensor Readings")
    ax.set_ylabel("Temperature (°C)")
    canvas.draw()

# Display the latest reading
tk.Label(root, text="Latest Temperature (°C):").pack()
tk.Label(root, textvariable=latest_temp).pack()

# Set up the plot
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Start reading the sensor data
read_sensor()

# Run the GUI loop
root.mainloop()

# Cleanup GPIO and pigpio on exit
pi.stop()
GPIO.cleanup()
