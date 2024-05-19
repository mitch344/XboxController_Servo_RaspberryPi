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
    print(f"Moving servo to angle: {angle}")

# Function to wait for the controller to become available
def wait_for_controller(path):
    while True:
        try:
            return evdev.InputDevice(path)
        except FileNotFoundError:
            print("Controller not found, waiting...")
            time.sleep(1)

# Function to make the controller rumble
def rumble_controller(controllerInput, duration=1):
    try:
        # Create a force feedback event
        effect_id = controllerInput.upload_effect({
            "type": evdev.ecodes.FF_RUMBLE,
            "replay": {"length": duration * 1000, "delay": 0},
            "u": {
                "rumble": {
                    "strong_magnitude": 0xc000,
                    "weak_magnitude": 0x8000,
                }
            }
        })
        # Play the effect
        controllerInput.write(evdev.ecodes.EV_FF, effect_id, 1)
        time.sleep(duration)
        # Stop the effect
        controllerInput.write(evdev.ecodes.EV_FF, effect_id, 0)
    except Exception as e:
        print(f"Failed to rumble controller: {e}")

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
            else:
                servo.ChangeDutyCycle(0)  # Stop the servo if no relevant button is pressed

# Main loop to handle reconnections
controller_path = "/dev/input/event2"
controllerInput = wait_for_controller(controller_path)

# Rumble the controller when the program starts
rumble_controller(controllerInput)

try:
    while True:
        try:
            handle_events(controllerInput)
        except OSError:
            print("Controller disconnected, waiting for reconnection...")
            controllerInput = wait_for_controller(controller_path)
            # Rumble the controller when reconnected
            rumble_controller(controllerInput)

except KeyboardInterrupt:
    # Clean up GPIO settings when the script is terminated
    servo.stop()
    GPIO.cleanup()
