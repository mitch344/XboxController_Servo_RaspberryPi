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
    angle = 90  # Start at the midpoint (90 degrees)
    for event in controllerInput.read_loop():
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == evdev.ecodes.ABS_Z:  # RT trigger
                if event.value > 0:
                    angle += 1  # Increment angle
                    angle = min(angle, 180)  # Clamp to 180 degrees max
                    duty_cycle = map_value(angle, 0, 180, 2, 12)
                    servo.ChangeDutyCycle(duty_cycle)
                    print(f"RT Trigger Angle: {angle}")
            elif event.code == evdev.ecodes.ABS_RZ:  # LT trigger
                if event.value > 0:
                    angle -= 1  # Decrement angle
                    angle = max(angle, 0)  # Clamp to 0 degrees min
                    duty_cycle = map_value(angle, 0, 180, 2, 12)
                    servo.ChangeDutyCycle(duty_cycle)
                    print(f"LT Trigger Angle: {angle}")

except KeyboardInterrupt:
    # Clean up GPIO settings when the script is terminated
    servo.stop()
    GPIO.cleanup()
