#!/usr/bin/python
"""
Basic botting program for Zero. Works with my keybindings only.

Premise:
A - Giga Crash
S - Flash Cut
D - Rising Slash
Del - Shadow Rain
End - Rhinne's Protection

Ctrl - Health pots

Run while in Beta form standing on a platform with a wall to your right.
This will bump the character against the wall and spam abilties in all
directions. This bot is not smart responsive except for potting when your
HP is low, so make sure you have thousands of health potions. If you get
moved out of position, the bot will continue doing the same thing, so you
need to find a place to stand where mobs do not or can not attack you.

Author: Alvin Lin (alvin.lin.dev@gmail)
"""

from Bot import Bot
from Keys import *
# from Auto_cube_wash import Auto_cube_wash

import sys
# sys.path.append('C:/0_tsa/Code/Python/Python_TMS/OSK/rune/')

from rune_solver import find_arrow_directions
from interception import *
from game import Game
from player import Player

import time
import random

import winsound

import pyautogui as pag
import cv2 as cv

import image_function


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

def alert(duration = 3, times = 1):
    for t in range(times):
        d = int(duration*1000)  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, d)
        time.sleep(0.5)
        
def quit_game():
    p.release_all()
    time.sleep(1)
    p.press('ESC')
    time.sleep(0.5)
    p.press('UP')
    time.sleep(0.5)
    p.press('ENTER')
    time.sleep(0.5)
    p.press('ENTER')

def changeChannel():
    p.release_all()
    # time.sleep(10)
    p.press('F10')
    time.sleep(1)
    p.press('RIGHT')
    time.sleep(1)
    p.press('ENTER')
    time.sleep(1)
    p.press('ENTER')

def solve_rune(g, p, target):
    """
    Given the (x, y) location of a rune, the bot will attempt to move the player to the rune and solve it.
    """
    iteration_runetime = 0
    while True:
        if iteration_runetime > 20:
            print('Already 20 times trys on runes. Give up.')
            alert(duration = 0.5, times = 4)
            return False
        iteration_runetime += 1
        print("Pathing towards rune...: ",target )
        # exit()
        # target += (0, 27)
        p.go_to_KI(target)
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
                time.sleep(5)
    return True

def isPulito():
    #pulito
    try:
        puluto_x, puluto_y = pag.locateCenterOnScreen('./pic_src/pulito.png'
                                                    , region = (0, 0, 300, 300))
        return 1
    except TypeError:
        return 0

def isHP():
    #hp
    try:
        hp25_x, hp25_y = pag.locateCenterOnScreen('./pic_src/HP75.png', 
                                          region = (300, 600, 400, 400))
        print('bad HP!~~~~~~~~~~~')
        return 1
    except TypeError:
        return 0

def isMP():
    #hp
    try:
        mp25_x, mp25_y = pag.locateCenterOnScreen('./pic_src/MP25.png', 
                                          region = (300, 600, 400, 400))
        return 1
    except TypeError:
        return 0

def isWarning():
    # use warning left door
    try:
        warning_x, warning_y = pag.locateCenterOnScreen('./pic_src/warning_left_door.png', 
                                          region = (0, 0, 300, 800))
        return 1
    except TypeError:
        return 0
        
def isReward():
    try:
        reward_x, reward_y = pag.locateCenterOnScreen('./pic_src/reward.png', 
                                          region = (700, 0, 500, 400))
        pag.click(reward_x, reward_y)
        time.sleep(1)
        pag.click(reward_x, reward_y)
        time.sleep(1)
        pag.click(reward_x, reward_y)
        time.sleep(1)
        return 1
    except TypeError:
        return 0

def isMileCoin():
    # if has coin
    try:
        mile_coin_x, mile_coin_y = pag.locateCenterOnScreen('./pic_src/mile_coin.png', 
                                          region = (600, 600, 600, 400))
        return 1
    except TypeError:
        return 0

def checkLieDetection(pyautogui, indic = 1):
        lie_Dt = pyautogui.locateOnScreen('data/Lie_Detection_small.png', 
                                          region = (0, 0, 1050, 800))
        while lie_Dt != None:
            #警报
            duration = 1000  # milliseconds
            freq = 440  # Hz
            winsound.Beep(freq, duration)
            
            lie_Dt_pt = pag.center(lie_Dt)
            bot.click(lie_Dt_pt, 0.5)
            print('click for lie detection: ', indic, 'times')
            indic +=1
            lie_Dt = pyautogui.locateOnScreen('data/Lie_Detection_small.png', 
                                              region = (0, 0, 1050, 800))
        else:
            return indic


if __name__ == "__main__":
        
    pag.FAILSAFE = True

    # for img locating
    imgf = image_function()
    
    #random gap
    rdm_gap = random.uniform(0.1, 0.2)
    # rdm_gap = random.uniform(0.05, 0.1)
    
    # this is for mouse click
    bot = Bot()
    
    # This setup is required for Interception to mimic your keyboard.
    c = interception()
    d = bind(c)
        
    # # 1s way to Get reasonable minimap (caution: without words of 'minimap' and 'arc')
    # try:
        
    #     # yellow_bulb_location = pag.locateOnScreen('./person_bottom_minimap.png')
    #     # minimap_bottom_y = arc_location[1]-60
    #     minimap_bottom_y = 130
    #     print('minimap_bottom_y: ', minimap_bottom_y)
    #     # exit()        
        
    #     # world_minimap_location = pag.locateOnScreen('./world_minimap.png')
    #     # minimap_right_x = world_minimap_location[0]+40
    #     # print('minimap_right_x: ', minimap_right_x)
    #     # exit()

    #     minimap_right_x = 250
    #     print('before minimap')
    #     # img = t.get_minimap_image(0, minimap_bottom_y, 0, minimap_right_x)
    #     print('after minimap')

    #     # exit()

    # except TypeError:
    #     # pass
    #     print(TypeError)
    #     # pag.alert(title = 'ERROR', text = 'Not in bot map', button = 'OK')
    #     exit()
    
    # 2nd way to get resonable minimap wih cv2
    

    # test
    # minimap = (0,minimap_bottom_y, 0,minimap_right_x)
    # img = t.get_minimap_image(minimap)
    # exit()
    

    # minimap_bottom_y = 50, minimap_right_x = 200
    g = Game((0, minimap_bottom_y, 0, minimap_right_x)) #!!! samll map four corner
    p = Player(c, d, g)
    

    # get center
    center = g.get_player_location()
    print("initial position: ", center)
    
    # Get and Set left&right wall
    lf_w = (60,center[1])
    # lf_w = (50,center[1])
    rt_w = (minimap_right_x-130, center[1])
    # rt_w = (minimap_right_x-50, center[1])
    # rt_w = (minimap_right_x-30, center[1])

    iterations_run = 0
    direction_mark = 0
    while True:
        # ''a'
        # pulito
        if isPulito() == 1:
            alert()
        else:
            pass
        # '''
        
        # HP
        if isHP()==1:
            p.press('PGUP')
        
        # HP
        if isMP()==0:
            p.press('PGDN')
            
        #WARNING
        if isWarning()==1:
            alert()
            p.press('2')
            time.sleep(1)
            p.press('2')
            time.sleep(10)
            changeChannel()
        
        # Reward
        isReward()
        
        # Coin
        if isMileCoin() == 1:
            p.press('H')
        
        # # Rune detection
        # rune_location = g.get_rune_location()
        # if rune_location is not None:
        #     # try:
        #         # pag.locateCenterOnScreen('./pic_src/rune_up_half.png')
        #         # pag.locateCenterOnScreen('./pic_src/rune_down_half.png')
        #         # print('Already got rune buff. Wait for fading.')
        #     # except TypeError:
        #     print('Rune location ：', rune_location)
        #     alert()
        #     # exit()
        
        #     print("A rune has appeared.")
        #     rune_mark = solve_rune(g, p, rune_location)
        #     if rune_mark == False:
        #         # quit_game
        #         print('Quit game')
        #         quit_game()
        #         exit()
        
        # Botting start
        iterations_run += 1
        print('itration: ', iterations_run)
        print (bot.getDebugText())
        # i_for_lie_dtc = 1
        
        try:
            x1, y1 = g.get_player_location()
        except TypeError:
        # if x1 and y1 == None:
            # pag.alert(text="Player Lost", title = 'ERROR', button = 'OK' )
            print('Player Lost')
            # exit()
            continue
        if x1 - lf_w[0] < 2:
            direction_mark = 0
            p.release("LEFT")
        elif rt_w[0] - x1 < 2:
            direction_mark = 1
            p.release("RIGHT")
        # elif y1<60:
            # time.sleep(0.3+rdm_gap)
            # p.hold("DOWN")
            # p.press("ALT")
            # p.release("DOWN")
            # time.sleep(0.3+rdm_gap)
            
        strPro = 'KI'
        if strPro == 'KI':
            if direction_mark == 0:
                p.hold("RIGHT")
                time.sleep(0.1)
                p.press("ALT")
                p.press("ALT")
                p.press("A")
            else:
                p.hold("LEFT")
                time.sleep(0.1)
                p.press("ALT")
                p.press("ALT")
                p.press("A")
            # time.sleep(0.8)
            if iterations_run %60 == 0:
                time.sleep(0.5)
                p.press("Y")
            elif iterations_run %90 == 0:
                time.sleep(0.8)
                p.press("N")
                time.sleep(1)
            elif iterations_run %167 == 0:
                time.sleep(0.8)
                p.press("J")
                time.sleep(1 + rdm_gap)
            elif iterations_run %13 == 0:
                p.press("SHIFT")
                time.sleep(rdm_gap+0.3)
                p.press("S")
                # time.sleep(rdm_gap)
            elif iterations_run %9 == 0:
                p.press("SHIFT")
                time.sleep(rdm_gap+0.3)
                p.press("D")
                # time.sleep(1 + rdm_gap)
            elif iterations_run %3 == 0:
                # p.release_all()
                time.sleep(0.8)
                p.press("SPACE")
                p.press("SPACE")

        # IL
        elif strPro == 'IL':
            if direction_mark == 0:
                p.press_wt("RIGHT", 1)
                time.sleep(0.3)
                p.press("SHIFT")
                time.sleep(0.3)
                for i in range(5):
                    p.press("A")
                    time.sleep(0.3)
            else:
                p.press_wt("LEFT", 1)
                time.sleep(0.3)
                p.press("SHIFT")
                time.sleep(0.3)
                for i in range(5):
                    p.press("A")
                    time.sleep(0.3)
            if iterations_run %17 == 0:
                p.release_all()
                time.sleep(0.3)
                p.press("F")
        # EW
        elif strPro == 'EW':
            if direction_mark == 0:
                p.hold("RIGHT")
                time.sleep(0.2)
                p.press("ALT")
                p.press("ALT")
                # time.sleep(0.3)
                p.press("Q")
            else:
                p.hold("LEFT")
                time.sleep(0.2)
                p.press("ALT")
                p.press("ALT")
                # time.sleep(0.3)
                p.press("Q")
            # time.sleep(0.5)
            # p.press("F")
            # time.sleep(0.1)
            # p.press("Q")
            # time.sleep(0.3)
            '''
            # if iterations_run %9 == 0:
                # time.sleep(0.5)
                # p.press("S")
                # time.sleep(0.6)
                # p.press("D")
            # el
            # if iterations_run %4 == 0:
                # p.release_all()
                # time.sleep(0.4)
                # p.press("ALT")
                # p.press("ALT")
                # p.press("SPACE")
            '''
        # ZR
        elif strPro == 'ZR':
            if direction_mark == 0:
                p.hold("RIGHT")
                # time.sleep(rdm_gap)
                p.press("A")
                time.sleep(0.3)
                p.press("A")
                time.sleep(0.3)
                p.press("A")
                time.sleep(0.3)
                p.press("S")
            else:
                p.hold("LEFT")
                p.press("A")
                time.sleep(0.3)
                p.press("A")
                time.sleep(0.3)
                p.press("A")
                time.sleep(0.3)
                p.press("S")
                
            if iterations_run %7 == 0:
                p.release_all()
                time.sleep(0.3)
                p.press("UP")
                time.sleep(0.3)
                p.press("UP")

        # CND
        elif strPro == 'CND':
            if direction_mark == 0:
                p.hold("RIGHT")
                # time.sleep(rdm_gap)
                p.press("ALT")
                p.press("ALT")
                p.press("A")
            else:
                p.hold("LEFT")
                # time.sleep(rdm_gap)
                p.press("ALT")
                p.press("ALT")
                p.press("A")
            
            p.press("F")
           
            if iterations_run %19 == 0:
                time.sleep(0.8)
                p.press("R")
            elif iterations_run %11 == 0:
                time.sleep(0.5)
                p.press("ALT")
                p.press("ALT")
                p.press("E")
                time.sleep(1)
                p.press("ALT")
                p.press("ALT")
                p.press("D")
            elif iterations_run %7 == 0:
                time.sleep(0.5)
                p.press("ALT")
                p.press("ALT")
                p.press("W")
                time.sleep(0.5)
                p.press("S")
            elif iterations_run %5 == 0:
                time.sleep(0.5)
                p.press("ALT")
                p.press("ALT")
                p.press("Q")
                p.press("X")
                
                p.release_all()
                time.sleep(0.5)
                p.hold('UP')
                p.press('SPACE')
                p.release('UP')
                time.sleep(0.5)
                p.press('SPACE')
                time.sleep(0.5)

        # HY
        elif strPro == 'HY':
            if direction_mark == 0:
                p.hold("RIGHT")
                time.sleep(rdm_gap)
                p.press("ALT")
                p.press("ALT")
                p.press("A")
            else:
                p.hold("LEFT")
                time.sleep(rdm_gap)
                p.press("ALT")
                p.press("ALT")
                p.press("A")
                
            if iterations_run %5 == 0:
                time.sleep(0.5) 
                p.press("S")
            elif iterations_run %7 == 0:
                time.sleep(0.5)
                p.press("ALT")
                p.press("Q")
            elif iterations_run %11 == 0:
                time.sleep(0.5)
                p.press("E")
                # print("wozai  EEE")
            elif iterations_run %13 == 0:
                time.sleep(0.5)
                p.press("R")
                # print("wozai  RRR")
            elif iterations_run %9 == 0:
                time.sleep(0.5)
                p.press("ALT")
                p.hold("UP")
                p.press_wt("SPACE")
                p.release_all()
        # DA
        elif strPro == 'DA':
            if direction_mark == 0:
                p.hold("RIGHT")
                time.sleep(rdm_gap)
                p.press("ALT")
                p.press("ALT")
                p.press("A")
            else:
                p.hold("LEFT")
                time.sleep(rdm_gap)
                p.press("ALT")
                p.press("ALT")
                p.press("A")
                
            if iterations_run %9 == 0:
                # p.go_to((minimap_right_x-40, center[1]))
                p.release_all()
                p.press('SHIFT')
                time.sleep(0.5)
                p.press('SPACE')
                time.sleep(1)
                # p.press_wt('LEFT', 5)
                # p.go_to(center)
                # p.press('SPACE')
                # time.sleep(1)
                # p.press_wt('LEFT',5)
                # p.go_to(center)
            elif iterations_run %6 == 0:
                p.release_all()
                time.sleep(0.5)
                p.press("D")
                time.sleep(2)
                p.press("F")
        # AK
        elif strPro == 'AK':
            if direction_mark == 0:
                p.hold("RIGHT")
                time.sleep(rdm_gap)
                p.press("ALT")
                p.press("ALT")
                p.press("A")
            else:
                p.hold("LEFT")
                time.sleep(rdm_gap)
                p.press("ALT")
                p.press("ALT")
                p.press("A")
            
            if iterations_run %11 == 0:
                time.sleep(0.5)
                p.press('X')
            elif iterations_run %9 == 0:
                p.press("ALT")
                p.press("ALT")
                # time.sleep(0.2)
                p.press("F")
            elif iterations_run %7 == 0:
                time.sleep(0.5)
                p.press('UP')
                p.press('D')
                time.sleep(0.8)
                p.press('D')
                time.sleep(1)
            elif iterations_run %3 == 0:
                time.sleep(rdm_gap)
                p.press("ALT")
                p.press("ALT")
                p.press("A")
                time.sleep(0.5)
                p.press("S")
            
        # BM
        elif strPro == 'BM':
            if direction_mark == 0:
                p.hold("RIGHT")
                time.sleep(0.2)
                p.press("ALT")
                p.press("ALT")
                time.sleep(0.25)
                p.press("A")
            else:
                p.hold("LEFT")
                time.sleep(0.2)
                p.press("ALT")
                p.press("ALT")
                time.sleep(0.25)
                p.press("A")
            
            if iterations_run %31 == 0:
                print('press F')
                p.release_all()
                time.sleep(0.2)
                p.press('F')
            elif iterations_run %17 == 0:
                print('press S')
                p.release_all()
                time.sleep(0.2)
                p.press("S")
        # PF
        elif strPro == 'PF':
            if direction_mark == 0:
                p.hold("RIGHT")
                
                p.press("ALT")
                p.press("ALT")
                # time.sleep(0.25)
                p.press("A")
            else:
                p.hold("LEFT")
                # time.sleep(0.2)
                p.press("ALT")
                p.press("ALT")
                # time.sleep(0.25)
                p.press("A")
            
            time.sleep(0.2)
            if iterations_run %11 == 0:
                time.sleep(0.2)
                p.press('D')
                time.sleep(0.8)
                p.press('W')
            '''
            elif iterations_run %3 == 0:
                # time.sleep(0.2)
                # p.press("ALT")
                # time.sleep(0.1)
                # p.press("UP")
                # p.press("UP")
            '''
        # IX
        elif strPro == 'IX':
            if direction_mark == 0:
                p.hold("RIGHT")
                time.sleep(0.1)
                p.press("ALT")
                p.press("ALT")
                time.sleep(0.25)
                p.press("S")
            else:
                p.hold("LEFT")
                time.sleep(0.1)
                p.press("ALT")
                p.press("ALT")
                time.sleep(0.25)
                p.press("S")
            time.sleep(0.8)
            '''
            if iterations_run %11 == 0:
                time.sleep(0.2)
                p.press('1')
            '''







