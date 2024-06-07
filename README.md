# Pid Loop Controller

A PID loop controller for managing execution intervals.

## Installation

You can install the package via pip:

```bash
pip install loop-controller
```

## Usage
```
from pid_loop_controller import PidLoopController

# Your function to be called in the loop
def my_function():
    print("Function called")

controller = PidLoopController(my_function, [], 1.0)
controller.set_controller_parameters(1.0, 0.1, 0.01)
controller.start()
```