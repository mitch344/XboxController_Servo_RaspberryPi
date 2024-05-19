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

def map_value(value, from_low, from_high, to_low, to_high):
    # Map the input value from one range to another
    return to_low + (float(value - from_low) / (from_high - from_low) * (to_high - to_low))

try:
    for event in controllerInput.read_loop():
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == evdev.ecodes.ABS_Z:  # RT trigger
                angle = map_value(event.value, 0, 255, 2, 12)
                angle = max(0, min(angle, 100))  # Ensure angle is within 0-100
                servo.ChangeDutyCycle(angle)
                print(f"RT Trigger Angle: {angle}")

            if event.code == evdev.ecodes.ABS_RZ:  # LT trigger
                angle = map_value(event.value, 0, 255, 2, 12)
                angle = max(0, min(angle, 100))  # Ensure angle is within 0-100
                servo.ChangeDutyCycle(angle)
                print(f"LT Trigger Angle: {angle}")

except KeyboardInterrupt:
    # Clean up GPIO settings when the script is terminated
    servo.stop()
    GPIO.cleanup()
