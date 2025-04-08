import RPi.GPIO as GPIO
import time



def GPIO_setup(PWM_PIN = 17):
    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PWM_PIN, GPIO.IN)

# Variables to store pulse times


# Function to measure high time in milliseconds
def PPM(pin=17):
    PERIOD_MS = 1004
    # Wait for rising edge (high pulse start)
    GPIO.wait_for_edge(pin, GPIO.RISING)
    pulse_start = time.perf_counter()

    # Wait for falling edge (high pulse end)
    GPIO.wait_for_edge(pin, GPIO.FALLING)
    pulse_end = time.perf_counter()

    # Calculate the high time in milliseconds
    high_time_ms = (pulse_end - pulse_start) * 1000
    ppm = (high_time_ms-2)*5

    # Calculate the duty cycle
    duty_cycle = (high_time_ms / PERIOD_MS) * 100

    # Print the high time and duty cycle
    return ppm

if __name__ == "__main__":
    GPIO_setup()
    print("started")
        
    while True:
        GPIO_setup()
        ppm = PPM()
        print(f"PPM: {int(round(ppm,0))}")
        time.sleep(0.1)  # Small delay to avoid excessive CPU usage

    GPIO.cleanup()  # Cleanup all the used GPIO pins
