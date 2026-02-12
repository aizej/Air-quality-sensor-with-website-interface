# CO2_laser_sensor.py  -- pigpio-based replacement
import time
import pigpio
import subprocess
import os

# module-level pigpio handle and measurement state
_pi = None
_last_rising_tick = None
_high_time_ms = None
_cb = None

# Time to wait for a measurement (ms)
_MEASUREMENT_TIMEOUT_MS = 2500
# Period constant used in original code
_PERIOD_MS = 1004

def _ensure_daemon_running():
    """Ensure pigpiod is running, try to start if not running (best-effort)."""
    # quick connection check will be done by GPIO_setup, but try to start if daemon missing
    try:
        # check if systemd service is active
        res = subprocess.run(["systemctl", "is-active", "--quiet", "pigpiod"])
        if res.returncode != 0:
            # try to start it (may require sudo privileges)
            subprocess.run(["sudo", "systemctl", "start", "pigpiod"], check=False)
    except Exception:
        # ignore — we'll check connection later and raise helpful error
        pass

def GPIO_setup(PWM_PIN=17):
    """
    Initialize pigpio and prepare the given pin as input.
    Keeps the same name as the old function so callers don't have to change anything.
    """
    global _pi, _cb
    if _pi is None:
        # Try to ensure daemon is running (best-effort)
        _ensure_daemon_running()
        _pi = pigpio.pi()
        if not _pi.connected:
            raise RuntimeError("pigpiod not running or pigpio.pi() failed. Start daemon with: sudo systemctl start pigpiod")

    # set input mode and enable pull-up (most CO2 PWM sensors are open-collector)
    _pi.set_mode(PWM_PIN, pigpio.INPUT)
    _pi.set_pull_up_down(PWM_PIN, pigpio.PUD_UP)

    # ensure no stale callback lingers for this pin
    if _cb is not None:
        try:
            _cb.cancel()
        except Exception:
            pass
        _cb = None

def PPM(pin=17):
    """
    Measure the PWM high time (ms) on `pin` using pigpio and return the PPM value.
    Returns None if no pulse was measured within the timeout.
    Keeps same function name and return math as original code:
       ppm = (high_time_ms - 2) * 5
    """
    global _pi, _last_rising_tick, _high_time_ms, _cb

    if _pi is None or not _pi.connected:
        # try to initialize automatically
        GPIO_setup(pin)

    # reset measurement state
    _last_rising_tick = None
    _high_time_ms = None

    # callback will capture one rising→falling pair and set _high_time_ms
    def _cb_func(gpio, level, tick):
        nonlocal_pin = pin  # shadow to avoid lint warning (not used further)
        global _last_rising_tick, _high_time_ms
        if level == 1:  # rising edge
            _last_rising_tick = tick
        elif level == 0:  # falling edge
            if _last_rising_tick is not None:
                # pigpio tickDiff(a, b) returns difference b - a in microseconds handling wrap
                dt_us = pigpio.tickDiff(_last_rising_tick, tick)
                # only accept reasonable values
                if 0 < dt_us < 5_000_000:  # <5s sanity guard
                    _high_time_ms = dt_us / 1000.0

    # register callback
    _cb = _pi.callback(pin, pigpio.EITHER_EDGE, _cb_func)

    # wait for measurement or timeout
    start = time.time()
    timeout_s = _MEASUREMENT_TIMEOUT_MS / 1000.0
    while (_high_time_ms is None) and (time.time() - start) < timeout_s:
        # sleep a tiny bit to yield CPU
        time.sleep(0.005)

    # cleanup callback (but keep _pi running for further calls)
    try:
        if _cb is not None:
            _cb.cancel()
    except Exception:
        pass
    _cb = None

    if _high_time_ms is None:
        return None

    high_time_ms = _high_time_ms
    ppm = (high_time_ms - 2) * 5
    # keep same duty-cycle calc if needed by callers later (not used here)
    duty_cycle = (high_time_ms / _PERIOD_MS) * 100.0

    return ppm

def GPIO_cleanup():
    """Cancel callbacks and stop pigpio connection (mirrors GPIO.cleanup)."""
    global _pi, _cb
    if _cb is not None:
        try:
            _cb.cancel()
        except Exception:
            pass
        _cb = None
    if _pi is not None:
        try:
            _pi.stop()
        except Exception:
            pass
        _pi = None

if __name__ == "__main__":
    GPIO_setup()
    print("started (pigpio)")
    try:
        while True:
            ppm = PPM()
            if ppm is not None:
                print("PPM:", int(round(ppm, 0)))
            else:
                print("No pulse detected")
            time.sleep(0.1)
    finally:
        GPIO_cleanup()
