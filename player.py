from interception.stroke import key_stroke
import time
import random

# Scancodes for arrow and alphanumeric/modifier keys should be separated. They have different key-states.
SC_DECIMAL_ARROW = {
    "LEFT": 75, "RIGHT": 77, "DOWN": 80, "UP": 72,
}

SC_DECIMAL = {
    "ALT": 56, "SPACE": 57, "CTRL": 29, "SHIFT": 42,
    "PGDN": 81, "PGUP": 73, "ESC": 1, "ENTER": 28,
    "A": 30, "S": 31, "D": 32, "F": 33, "H": 35, "Q": 16,  "J": 36,
    "Q": 16, "W": 17, "E": 18, "R": 19, "C": 46, "X": 45, "Y": 21,
    "N": 49,
    "1": 2, "2": 3, "3": 4, "4": 5, "5": 6,
    "F10": 68
}

# Change these to your own settings.
JUMP_KEY = "ALT"
ROPE_LIFT_KEY = "SPACE" #!!! changed from "D" from origin

#random gap
rdm_gap = random.uniform(0.1, 0.2)
# rdm_gap = random.uniform(0.05, 0.85)

class Player:
    def __init__(self, context, device, game):
        self.game = game
        # interception
        self.context = context
        self.device = device

    def release_all(self):
        for key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 3, 0))
        for key in SC_DECIMAL:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 1, 0))

    def press(self, key):
        """
        Mimics a human key-press.
        Delay between down-stroke and up-stroke was tested to be around 50 ms.
        """
        if key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 2, 0))
            time.sleep(random.uniform(0.05, 0.13))
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 3, 0))
            time.sleep(0.05)
        else:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 0, 0))
            time.sleep(random.uniform(0.05, 0.13))
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 1, 0))
            time.sleep(0.05)
    
    def press_wt(self, key, duration = 1):
        """
        Mimics a human key-press.
        Delay between down-stroke and up-stroke was tested to be around 50 ms.
        """
        if key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 2, 0))
            time.sleep(duration)
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 3, 0))
            time.sleep(0.05)
        else:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 0, 0))
            time.sleep(duration)
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 1, 0))
            time.sleep(0.05)
            
    def release(self, key):
        if key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 3, 0))
        else:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 1, 0))

    def hold(self, key):
        if key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 2, 0))
            # time.sleep(rdm_gap)
        else:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 0, 0))
            # time.sleep(rdm_gap)

    # def junp_attack(self):
        # self.hold
        
        
    def go_to(self, target):
        """
        Attempts to move player to a specific (x, y) location on the screen.
        """
        while True:
            player_location = self.game.get_player_location()
            if player_location is None:
                # continue
                print('cant find player in the mini-map')
                exit()

            x1, y1 = player_location
            x2, y2 = target

            """
            There are delays between taking a screenshot, processing the image, sending the key press, and game server ping.
            Player should be within 2 pixels of x-destination and 7 pixels of y-destination.
            """
            if abs(x1 - x2) < 2:
                print('Player has reached target x-destination, release all held keys.')
                self.release_all()
                if abs(y2 - y1) < 5:
                    print('Player has reached target y-destination, release all held keys.')
                    self.release_all()
                    break
                # Player is above target y-position.
                elif y1 < y2:
                    print("Player is above target y-position.")
                    self.hold("DOWN")
                    self.press(JUMP_KEY)
                    self.release("DOWN")
                # Player is below target y-position.
                else:
                    print('Player is below target y-position.')
                    if y1 - y2 > 10:
                        print('Y is too far, use rope')
                        self.press(ROPE_LIFT_KEY)
                    else:
                        # self.press("UP")
                        # self.press("UP")
                        print('Y is not that far, also use rope')
                        self.press(ROPE_LIFT_KEY)
                # Delay for player falling down or jumping up.
                time.sleep(1)
            else:
                # Player is to the left of target x-position.
                if x1 < x2:
                    print('Player is at the left of target x-position.')
                    self.hold("RIGHT")
                # Player is to the right of target x-position.
                else:
                    print('Player is at the right of target x-position.')
                    self.hold("LEFT")
                # if abs(x2 - x1) > 30:
                    # print('X is too far, use double jump')
                    # self.press(JUMP_KEY)
                    # self.press(JUMP_KEY)

    def go_to_IL(self, target):
        """
        Attempts to move player to a specific (x, y) location on the screen.
        """
        while True:
            player_location = self.game.get_player_location()
            if player_location is None:
                # continue
                print('cant find player in the mini-map')
                exit()

            x1, y1 = player_location
            x2, y2 = target

            """
            There are delays between taking a screenshot, processing the image, sending the key press, and game server ping.
            Player should be within 2 pixels of x-destination and 7 pixels of y-destination.
            """
            if abs(x1 - x2) < 2:
                print('Player has reached target x-destination, release all held keys.')
                self.release_all()
                if abs(y2 - y1) < 5:
                    print('Player has reached target y-destination, release all held keys.')
                    self.release_all()
                    break
                # Player is above target y-position.
                elif y1 < y2:
                    print("Player is above target y-position.")
                    self.hold("DOWN")
                    self.press(JUMP_KEY)
                    self.release("DOWN")
                # Player is below target y-position.
                else:
                    print('Player is below target y-position.')
                    if y1 - y2 > 10:
                        print('Y is too far, use fly')
                        self.hold('UP')
                        self.press('ALT')
                        self.hold('SPACE')
                        time.sleep(1)
                        self.release_all
                    else:
                        print('Y is not that far, also use rope')
                        self.hold('UP')
                        self.press('SPACE')
                        self.release_all()
                # Delay for player falling down or jumping up.
                time.sleep(1)
            else:
                # Player is to the left of target x-position.
                if x1 < x2:
                    print('Player is at the left of target x-position.')
                    self.hold("RIGHT")
                # Player is to the right of target x-position.
                else:
                    print('Player is at the right of target x-position.')
                    self.hold("LEFT")
                # if abs(x2 - x1) > 30:
                    # print('X is too far, use double jump')
                    # self.press(JUMP_KEY)
                    # self.press(JUMP_KEY)
                    
    def go_to_KI(self, target):
        """
        Attempts to move player to a specific (x, y) location on the screen.
        """
        # self.release('LEFT')
        # self.release('RIGHT')
        self.release_all()
        while True:
            player_location = self.game.get_player_location()
            if player_location is None:
                continue

            x1, y1 = player_location
            x2, y2 = target

            """
            There are delays between taking a screenshot, processing the image, sending the key press, and game server ping.
            Player should be within 2 pixels of x-destination and 7 pixels of y-destination.
            """
            if abs(x1 - x2) < 2:
                print('Player has reached target x-destination, release all held keys.')
                self.release_all()
                # self.release("LEFT")
                # self.release("RIGHT")
                if abs(y2 - y1) < 5:
                    print('Player has reached target y-destination, release all held keys.')
                    self.release_all()
                    break
                # Player is above target y-position.
                elif y1 < y2:
                    print("Player is above target y-position.")
                    self.hold("DOWN")
                    self.press(JUMP_KEY)
                    self.release("DOWN")
                # Player is below target y-position.
                else:
                    print('Player is below target y-position.')
                    if y1 - y2 > 10:
                        print('Y is too far, use rope')
                        time.sleep(0.5)
                        self.press('SPACE')
                        time.sleep(0.3)
                        self.press('SPACE')
                    else:
                        # self.press("UP")
                        # self.press("UP")
                        print('Y is not that far, use S')
                        self.press('S')
                # Delay for player falling down or jumping up.
                time.sleep(1)
            else:
                # Player is to the left of target x-position.
                if x1 < x2:
                    print('Player is at the left of target x-position.')
                    self.hold("RIGHT")
                # Player is to the right of target x-position.
                else:
                    print('Player is at the right of target x-position.')
                    self.hold("LEFT")
                # if abs(x2 - x1) > 30:
                    # print('X is too far, use double jump')
                    # self.press(JUMP_KEY)
                    # self.press(JUMP_KEY)

