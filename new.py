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

# Open the controller device
controllerInput = evdev.InputDevice("/dev/input/event2")

def move_servo(angle):
    duty_cycle = angle / 18 + 2
    servo.ChangeDutyCycle(duty_cycle)
    print(f"Moving servo to angle: {angle}")

try:
    for event in controllerInput.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            if event.code == evdev.ecodes.BTN_A and event.value == 1:  # A button pressed
                move_servo(0)  # Move to 0 degrees
            elif event.code == evdev.ecodes.BTN_B and event.value == 1:  # B button pressed
                move_servo(90)  # Move to 90 degrees
            elif event.code == evdev.ecodes.BTN_X and event.value == 1:  # X button pressed
                move_servo(180)  # Move to 180 degrees

except KeyboardInterrupt:
    # Clean up GPIO settings when the script is terminated
    servo.stop()
    GPIO.cleanup()
