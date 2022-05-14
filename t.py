
# Auto-Kain


import string
import pyautogui as pag

from ctypes import *

from pymouse import *
from pykeyboard import PyKeyboard

import random
import time
import winsound

from PIL import ImageGrab
from PIL import Image
from aip import AipOcr

import pyautogui as pag
import numpy as np
import cv2 as cv
import pytesseract

sys.path.append('C:/0_tsa/Code/Python/Python_TMS/Bot_t/')
sys.path.append('C:/0_tsa/Code/Python/Python_TMS/maple_cube/')
from image_function import ImgFuction
from game import Game
import gdi_capture

def alert(duration = 3, times = 1):
    for t in range(times):
        d = int(duration*1000)  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, d)
        time.sleep(0.5)
        
def get_minimap_image(minimap):
    """
    Takes a picture of the application window.
    """
    hwnd = gdi_capture.find_window_from_executable_name("MapleStory.exe")
    with gdi_capture.CaptureWindow(hwnd) as img:
        if img is None:
            print("MapleStory.exe was not found.")
            return None
        else: 
            imgc = img.copy()
            imgc = imgc[minimap[0]:minimap[1], minimap[2]:minimap[3]]
            cv.imshow('minimap', imgc)
            cv.waitKey(0)
            cv.destroyAllWindows()
            # exit()
            return imgc[minimap[0]:minimap[1], minimap[2]:minimap[3]]
            
def legendInner():

    try:
        use_inner_x, use_inner_y = pag.locateCenterOnScreen('./pic_src/use_inner.png')
    except TypeError:
        print('no use_inner button')
        alert()
        return 0
        
    while True:
        try:
            legend_inner_x, legend_inner_y = pag.locateCenterOnScreen('./pic_src/legend_inner.png')
            alert()
            return 1
        except TypeError:
            pag.moveTo(use_inner_x, use_inner_y, duration = 0.25)
            pag.click(use_inner_x, use_inner_y)
            time.sleep(0.3)
            pag.press('enter')
            time.sleep(0.3)
            pag.press('enter')
            time.sleep(0.5)
            # return 1

            
        
    
if __name__ == "__main__":

    imgf = ImgFuction()

    # p_minimap = imgf.getScreenImg('p_mini_map.png')
    # p_minimap_world = './pic_src/world_minimap.png'
    # imgf.locatesOnImg(p_minimap, p_minimap_world, 0.98)

    imgf.getScreenImgByGui()
    
    # try:
    #     loca = pag.locateOnScreen('./pic_src/world_minimap.png')
    #     print ('loca: ', loca)
    # except TypeError as e:
    #     print('no loca:', e)

    # minimap = (0, 80, 0, 300)
    # img = get_minimap_image(minimap)
    

    # legendInner()

    '''
    img = cv2.imread("./data/test1.png")
    imgContour = img.copy()
    #转换为灰度图像
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #模糊图像
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    #边缘检测
    imgCanny = cv2.Canny(imgBlur, 50, 50)

    getContours(imgCanny)
    #定义空白图像
    imgBlank = np.zeros_like(img)
    imgStack = stackImages(0.6, ([img, imgGray, imgBlur], [imgCanny, imgContour, imgBlank]))

    cv2.imshow("imgStack", imgStack)

    cv2.waitKey(0)
    '''

    '''
    img = cv2.imread('./data/d1-1.png', 0)    
    # img = cv2.imread('C:/0_tsa/Code/Python/Python_TMS/OSK/data/mv.png', 0)
    
    gaus = cv2.GaussianBlur(img,(3,3),0)
    cv2.imshow('Gaussian', gaus)
    edges = cv2.Canny(gaus,100,200)
    cv2.imshow('Edges',edges)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    exit()
    
    ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
    ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
    ret,thresh5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)
    
    cv2.imshow('Original Image', img)
    cv2.imshow('BINARY', thresh1)
    cv2.imshow('BINARY_INV', thresh2)
    cv2.imshow('TRUNC', thresh3)
    cv2.imshow('TOZERO', thresh4)
    cv2.imshow('TOZERO_INV', thresh5)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


    test = pytesseract.image_to_string(thresh3, lang = 'chi_tra+chi_sim+eng+num')
    print(test)
    '''