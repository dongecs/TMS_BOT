import time
import random
from rune_solver import find_arrow_directions
from interception import *
from game import Game
from player import Player

# from DA import main as 


def bind(context):
    context.set_filter(interception.is_keyboard, interception_filter_key_state.INTERCEPTION_FILTER_KEY_ALL.value)
    print("Click any key on your keyboard.")
    device = None
    while True:
        device = context.wait()
        if interception.is_keyboard(device):
            print(f"Bound to keyboard: {context.get_HWID(device)}.")
            c.set_filter(interception.is_keyboard, 0)
            break
    return device

def solve_rune(g, p, target):
    """
    Given the (x, y) location of a rune, the bot will attempt to move the player to the rune and solve it.
    """
    while True:
        print("Pathing towards rune...")
        p.go_to(target)
        # Activate the rune.
        time.sleep(1)
        p.press("C")
        # Take a picture of the rune.
        time.sleep(1)
        img = g.get_rune_image()
        print("Attempting to solve rune...")
        directions = find_arrow_directions(img)

        if len(directions) == 4:
            print(f"Directions: {directions}.")
            for d, _ in directions:
                p.press(d)

            # The player dot will be blocking the rune dot, attempt to move left/right to unblock it.
            p.hold("LEFT")
            time.sleep(random.uniform(0.5, 1.25))
            p.release("LEFT")

            p.hold("RIGHT")
            time.sleep(random.uniform(0.5, 1.25))
            p.release("RIGHT")

            rune_location = g.get_rune_location()
            if rune_location is None:
                print("Rune has been solved.")
                break
            else:
                print("Trying again...")


if __name__ == "__main__":
    # This setup is required for Interception to mimic your keyboard.
    c = interception()
    d = bind(c)

    # Example Script for Hayato @ SS4.
    # g = Game((5, 60, 180, 130)) #!!! samll map four corner
    g = Game((15, 100, 175, 143)) #!!! samll map four corner
    p = Player(c, d, g)
    # target = (97, 32.5)
    target = (80, 45)
    
    # left bottm
    # lf_bt = (25, 155)
    # right bottom
    # rt_bt = (170, 155)

    while True:
        other_location = g.get_other_location()
        if other_location > 0:
            print("A player has entered your map.")

        # rune_location = g.get_rune_location()
        # if rune_location is not None:
            # print("A rune has appeared.")
            # solve_rune(g, p, rune_location)

        print("Running...")
        p.go_to(target)

        time.sleep(1)
        p.press("D")
        time.sleep(1)
        p.press("F")
        time.sleep(4)

        p.press("D")
        time.sleep(1)
        p.press("F")
        time.sleep(4)

        # p.go_to(lf_bt)
        # p.go_to(rt_bt)
