import evdev
import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for the servo
servo_pin = 18

# Set the GPIO pin as an output
GPIO.setup(servo_pin, GPIO.OUT)

# Initialize the servo PWM at 50Hz
servo = GPIO.PWM(servo_pin, 50)

# Start the PWM with 0% duty cycle
servo.start(0)

# Function to move the servo to a specific angle
def move_servo(angle):
    duty_cycle = angle / 18 + 2
    servo.ChangeDutyCycle(duty_cycle)
    print(f"Moving servo to angle: {angle}")

# Function to wait for the controller to become available
def wait_for_controller(path):
    while True:
        try:
            return evdev.InputDevice(path)
        except FileNotFoundError:
            print("Controller not found, waiting...")
            time.sleep(1)

# Wait for the controller to be available
controllerInput = wait_for_controller("/dev/input/event2")

try:
    for event in controllerInput.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            if event.code == evdev.ecodes.BTN_A and event.value == 1:  # A button pressed
                move_servo(0)  # Move to 0 degrees
            elif event.code == evdev.ecodes.BTN_X and event.value == 1:  # X button pressed
                move_servo(180)  # Move to 180 degrees
            else:
                servo.ChangeDutyCycle(0)  # Stop the servo if no relevant button is pressed

except KeyboardInterrupt:
    # Clean up GPIO settings when the script is terminated
    servo.stop()
    GPIO.cleanup()
