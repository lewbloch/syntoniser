from enum import Enum
from gpiozero import OutputDevice as Outpin
import time


class Spin(Enum):
    deosil = True
    widdershins = False


class Substep(Enum):
    """
    # Substeps per full cycle: [200, 400, 800, 1600, 3200, 6400]
    #  200 steps / cycle = 1.8 degrees / step = π/100 radians
    """
    FULL = (0, 0, 0)
    HALF = (1, 0, 0)
    QUARTER = (0, 1, 0)
    EIGHTH = (1, 1, 0)
    SIXTEENTH = (0, 0, 1)
    THIRTYSECONDTH = (1, 0, 1)


class Stepper:
    """
    # motor_a = Stepper(wayward=13, moving=19, disabler=12, substepper=(16, 17, 20))
    # motor_b = Stepper(wayward=24, moving=18, disabler=4, substepper=(21, 22, 27))
    """

    def __init__(self, wayward, moving, disabler, substepper):
        self.wayward = Outpin(wayward)
        self.moving = Outpin(moving)
        self.disabler = Outpin(disabler)
        self.substepper = []
        for pn in substepper:
            pin = Outpin(pn)
            self.substepper.append(pin)
            pin.off()

        self.halt()

    def halt(self):
        self.moving.off()
        self.wayward.off()
        self.disabler.on()

    def rotate(self, direction, steps, pause=0.005):
        print(direction, steps, pause)
        if steps == 0 or pause <= 0.0:
            return

        if direction.value:
            self.wayward.on()
        else:
            self.wayward.off()

        self.disabler.off()
        for i in range(steps):
            self.moving.off()
            time.sleep(pause)
            self.moving.on()
            time.sleep(pause)
        self.disabler.on()

    def substep(self, substep: Substep):
        """
        substep: subdivision of the standard full step size,
         from (FULL, HALF, QUARTER, EIGHTH, SIXTEENTH, THIRTYSECONDTH)
        """
        substeppins = substep.value
        for pinx in range(len(substeppins)):
            self.substepper[pinx].on() if substeppins[pinx] == 0 else self.substepper[pinx].off()

        print(self.substepper)
