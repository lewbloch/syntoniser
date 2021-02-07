from enum import Enum
from gpiozero import OutputDevice as Outpin
import time


class Spin(Enum):
    deosil = True
    widdershins = False


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

        self.substeppings = {
            200: (0, 0, 0),
            400: (1, 0, 0),
            800: (0, 1, 0),
            1600: (1, 1, 0),
            3200: (0, 0, 1),
            6400: (1, 0, 1)
        }

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

    def set_substepping(self, substep):
        """
        substep: number of steps per cycle, from (200, 400, 800, 1600, 3200, 6400)
        """
        substepping = self.substeppings[substep]
        for mp in range(len(substepping)):
            if substepping[mp] == 0:
                self.substepper[mp].on()
            else:
                self.substepper[mp].off()

        print(self.substepper)
