import time

from stepper import Stepper, Spin, Substep

"""
# Substeps per full cycle: [200, 400, 800, 1600, 3200, 6400]
#  200 steps / cycle = 1.8 degrees / step
"""

# noinspection PyBroadException
motor_a = Stepper(wayward=13, moving=19, disabler=12, substepper=(16, 17, 20))
motor_b = Stepper(wayward=24, moving=18, disabler=4, substepper=(21, 22, 27))
motor_a.substep(Substep.FULL)
motor_a.rotate(direction=Spin.deosil, steps=400, pause=0.001)
time.sleep(0.5)
motor_a.rotate(direction=Spin.widdershins, steps=400, pause=0.001)

time.sleep(0.5)

motor_a.substep(Substep.QUARTER)
motor_a.rotate(direction=Spin.deosil, steps=4000, pause=0.0001)
time.sleep(0.5)
motor_a.rotate(direction=Spin.widdershins, steps=4000, pause=0.0001)

print("\nStop")

motor_a.halt()
motor_b.halt()
