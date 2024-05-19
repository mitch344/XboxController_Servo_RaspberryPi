import evdev
import RPi.GPIO as GPIO
import time
import os

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
    time.sleep(0.5)  # Allow some time for the servo to move
    print(f"Moving servo to angle: {angle}")

# Function to wait for the controller to become available
def wait_for_controller(path):
    while True:
        try:
            return evdev.InputDevice(path)
        except FileNotFoundError:
            print("Controller not found, waiting...")
            time.sleep(1)

# Function to handle controller events
def handle_events(controllerInput):
    start_button_pressed_time = None
    start_button_hold_duration = 3  # seconds

    for event in controllerInput.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            if event.code == evdev.ecodes.BTN_A and event.value == 1:  # A button pressed
                move_servo(0)  # Move to 0 degrees
            elif event.code == evdev.ecodes.BTN_X and event.value == 1:  # X button pressed
                move_servo(180)  # Move to 180 degrees
            elif event.code == evdev.ecodes.BTN_START:
                if event.value == 1:  # Start button pressed
                    start_button_pressed_time = time.time()
                elif event.value == 0:  # Start button released
                    if start_button_pressed_time is not None:
                        press_duration = time.time() - start_button_pressed_time
                        if press_duration >= start_button_hold_duration:
                            print("Shutting down system...")
                            os.system("sudo shutdown -h now")
                        start_button_pressed_time = None

# Main loop to handle reconnections
controller_path = "/dev/input/event2"
controllerInput = wait_for_controller(controller_path)

try:
    # Move servo to 180 degrees and then back to 0 degrees to verify the program has started
    move_servo(180)
    time.sleep(1)
    move_servo(0)
    time.sleep(1)
    servo.ChangeDutyCycle(0)  # Stop the servo

    while True:
        try:
            handle_events(controllerInput)
        except OSError:
            print("Controller disconnected, waiting for reconnection...")
            controllerInput = wait_for_controller(controller_path)

except KeyboardInterrupt:
    # Clean up GPIO settings when the script is terminated
    servo.stop()
    GPIO.cleanup()
