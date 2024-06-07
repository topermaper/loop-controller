import time
import collections
from threading import Event


class PidLoopController(object):
    def __init__(self, function, f_args, target_interval: float, logger=None, print_stats=False):
        self._logger = logger
        self._print_stats = print_stats

        self._kp = None
        self._ki = None
        self._kd = None

        self._target_interval = target_interval

        self._function = function
        self._f_args = f_args

        self._stop_event = Event()

    def set_controller_parameters(self, kp, ki, kd):
        self._kp = kp
        self._ki = ki
        self._kd = kd

    def start(self):
        self._stop_event.clear()

        integral = 0
        previous_error = 0
        sleep_time = 0

        time_stamp = collections.deque([], maxlen=2)

        if self._kd is None or self._ki is None or self._kd is None:
            raise Exception("Set controller parameters first")

        # Get initial timestamp
        time_stamp.append(time.monotonic())

        while not self._stop_event.is_set():
            # Call iteration function
            try:
                self._function(*self._f_args)
            except Exception as e:
                import traceback
                traceback.print_exc()
                if self._logger:
                    self._logger.error(f"Loop error. {e}")

            # Get current timestamp
            time_stamp.append(time.monotonic())

            elapsed_time = time_stamp[-1] - time_stamp[-2]

            # Calculate the error (difference between desired and actual speed)
            error = self._target_interval - elapsed_time

            # Calculate the PID components
            proportional = self._kp * error
            integral += self._ki * error
            derivative = self._kd * (error - previous_error)

            # Calculate the control variable (adjustment to loop speed)
            control_variable = proportional + integral + derivative

            # Apply the control variable as a delay (if control_variable is positive) or accelerate (if negative)
            sleep_time = max(0, sleep_time + control_variable)

            if self._logger and self._print_stats:
                self._logger.info(
                    f"Loop elapsed time: {elapsed_time:.3f}s "
                    f"control_variable: {control_variable} "
                    f"p: {proportional} "
                    f"i: {integral} "
                    f"d: {derivative} "
                    f"sleep: {sleep_time}"
                )

            # Store the current error for the next iteration
            previous_error = error

            # Sleep a bit
            time.sleep(sleep_time)

    def stop(self):
        self._stop_event.set()
