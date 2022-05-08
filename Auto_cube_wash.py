import win32api
import win32con
import win32gui
import io

from pymouse import *
from pykeyboard import PyKeyboard

import random
import time

from PIL import ImageGrab
from PIL import Image
from aip import AipOcr

import pyautogui as pag

class Auto_cube_wash():

    global confirm_button_location, b_mark

    def __init__(self): 
        self.b_mark = False
    
    '''
    def move_click(self, x, y, t=0):  # 移动鼠标并点击左键
        
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE,   x, y, 0, 0)
        time.sleep(0.5)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)  # 点击鼠标左键
        if t == 0:
            time.sleep(random.random()*2+1)  # sleep一下
        else:
            time.sleep(t)
        return 0
    '''
    'get WIN10 window'
    def get_window_resolution (self):
        w = win32api.GetSystemMetrics(0)
        h = win32api.GetSystemMetrics(1)
        print ('my width: ', w, '  & my height: ', h )
        return w,h

    'get Maplestory window'
    def get_window_info(self):
        wdname = u'Maplestory'
        handle = win32gui.FindWindow(0, wdname)  # 获取窗口句柄

        if handle == 0:
            print("Cant get Maplestory window")
            return False, False
        else:
            print("handle position: ", handle)
            w_rect = win32gui.GetWindowRect(handle)
            return w_rect, handle

    # distinguish word
    def OCR_confirm_button(self, string, img):
     
        b_mark = False
        #百度文字识别
        APP_ID = '24698995'
        API_KEY = '2b41B6uCUG3FRqTGHUH5AolH'
        SECRECT_KEY = 'r32fUc6iUHxWOXCKaaAKH20V6i2cPG6S'
        client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
        
        # """ OCR可选参数 """
        options = {}
        # options = {"recognize_granularity": "small"}
        #options["language_type"] = "CHN_ENG"
        #options["detect_direction"] = "true"
        #options["detect_language"] = "true"
        #options["probability"] = "true"

        #截屏
        # img = ImageGrab.grab()
        #字节容器
        img_b = io.BytesIO()
        #image转换为png
        img.save(img_b, format='PNG')
        #存入容器
        img_b = img_b.getvalue()

        try:
            result=client.accurate(img_b, options)
        except:
             print('网络问题')
        
        print("api_result:", result)
            
        num=result['words_result_num']
        resultword=result['words_result']
        
        for f in result['words_result']:
            n = f['words'].find(string)
            if n != -1:
                print('Confirm button: ', f['words'],f['location'])
                b_mark = True
                return f['location']

    def OCR_epic(self, string, img):
     
        b_mark = False
        #百度文字识别
        APP_ID = '24698995'
        API_KEY = '2b41B6uCUG3FRqTGHUH5AolH'
        SECRECT_KEY = 'r32fUc6iUHxWOXCKaaAKH20V6i2cPG6S'
        client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
        
        # """ OCR可选参数 """
        options = {}
        # options = {"recognize_granularity": "small"}
        #options["language_type"] = "CHN_ENG"
        #options["detect_direction"] = "true"
        #options["detect_language"] = "true"
        #options["probability"] = "true"

        #截屏
        # img = ImageGrab.grab()
        #字节容器
        img_b = io.BytesIO()
        #image转换为png
        img.save(img_b, format='PNG')
        #存入容器
        img_b = img_b.getvalue()

        # try:
            # result=client.accurate(img_b, options)
        # except:
             # print('网络问题')
        
        result=client.basicAccurate(img_b, options)
        
        print("api_result:", result)
        print("\n")
            
        num=result['words_result_num']
        resultword=result['words_result']
        
        for f in result['words_result']:
            n = f['words'].find(string)
            if n != -1:
                # print('Epic found: ', f['words'],f['location'])
                print('Epic found: ', f['words'])
                b_mark = True
                return b_mark

# 测试
if __name__ == "__main__":

    # m = PyMouse()
    # k = PyKeyboard()
    acw = Auto_cube_wash()
    
    img = pag.screenshot(region=(0, 0, 1100, 800))

    # x scale number
    # img_ready = ImageGrab.grab(bbox=(w_rect[0]*1.25, w_rect[1]*1.25, w_rect[2]*1.25, w_rect[3]*1.25))
    # 查看图片
    # img.show()
    # exit()

    epic_string = "DEX"
    b_mark = acw.OCR_epic(epic_string, img)
         

    print('out end')

'''
    wr_w = 0
    wr_h = 0
    
    wr_w, wr_h = get_window_resolution()
    print('window rslt: ', wr_w, ' & ', wr_h)
'''























