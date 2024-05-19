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

try:
    for event in controllerInput.read_loop():
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == evdev.ecodes.ABS_Z:  # RT trigger
                angle = 2 + (event.value / 255 * 10)  # Map to 2-12 duty cycle
                servo.ChangeDutyCycle(angle)
                print(f"RT Trigger Angle: {angle}")

            if event.code == evdev.ecodes.ABS_RZ:  # LT trigger
                angle = 2 + (event.value / 255 * 10)  # Map to 2-12 duty cycle
                servo.ChangeDutyCycle(angle)
                print(f"LT Trigger Angle: {angle}")

except KeyboardInterrupt:
    # Clean up GPIO settings when the script is terminated
    servo.stop()
    GPIO.cleanup()
