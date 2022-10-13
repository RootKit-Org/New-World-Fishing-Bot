import pyautogui
import pydirectinput
import time
import random
import mss
import numpy as np
from PIL import Image
import tkinter as tk
import gc

def main():
    """
    Main function for the program
    """
    # Max cast is 1.9 secs
    # Base time it will always cast at
    castingBaseTime = 1.2
    # Max random amount of time to add to the base
    castingRandom = .4

    # How long to slack the line
    lineSlackTime = 2

    # Adding randomness to the wait times for the animations
    animationSleepTime = .5 + (.1 * random.random())

    # Randomly will move right or left to keep from AFKing
    moveDirection = ["a", "d"]

    # Free cam key
    freeCamKey = "b"

    # Finds all Windows with the title "New World"
    newWorldWindows = pyautogui.getWindowsWithTitle("New World")
   
    # Find the Window titled exactly "New World" (typically the actual game)
    for window in newWorldWindows:
        if window.title == "New World":
            newWorldWindow = window
            break

    # Select that Window
    newWorldWindow.activate()
   
    # Move your mouse to the center of the game window
    centerW = newWorldWindow.left + (newWorldWindow.width/2)
    centerH = newWorldWindow.top + (newWorldWindow.height/2)
    pyautogui.moveTo(centerW, centerH)

    # Clicky Clicky
    time.sleep(animationSleepTime)
    pyautogui.click()
    time.sleep(animationSleepTime)
    
    # Selecting the middle 3rd of the New World Window
    mssRegion = {"mon": 1, "top": newWorldWindow.top, "left": newWorldWindow.left + round(newWorldWindow.width/3), "width": round(newWorldWindow.width/3), "height": newWorldWindow.height}
   #root = tk.Tk()
   #window = tk.Toplevel()
   #window.resizable(False, False)
   #window.attributes("-fullscreen", True)
   #window.wm_attributes("-transparentcolor", window["bg"])
   #window.attributes("-topmost", True)
   #canvas = tk.Canvas(window, width=10000, height=10000)
   ##x,y, x+width,y+height
   #canvas.create_rectangle( 
   #  newWorldWindow.left + round(newWorldWindow.width/3),
   #  newWorldWindow.top,
   #  newWorldWindow.left + round(newWorldWindow.width/3)+round(newWorldWindow.width/3),
   #  newWorldWindow.height +newWorldWindow.top,
   #  outline="green",
   #  width=5,
   #)
   #canvas.pack()
   #root.mainloop()
     #Starting screenshotting object
    sct = mss.mss()
    output = "sct-1.png"

    # This should resolve issues with the first cast being short
    time.sleep(animationSleepTime * 3)
    i =0;
    while True:
        # Screenshot
        #sct_img = sct.grab(mssRegion)
       # mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))
        # Calculating those times
        castingTime = castingBaseTime + (castingRandom * random.random())

        # Hold the "Free Look" Button
        print("Holding Free Look Button")
        pydirectinput.keyDown(freeCamKey)

        # Like it says, casting
        print("Casting Line")
        pyautogui.mouseDown()
        time.sleep(castingTime)
        pyautogui.mouseUp()

        # Looking for the fish icon, doing forced garbage collection
        while pyautogui.locate("imgs/fishIcon.png", sctImg, grayscale=True, confidence=.6) is None:
            gc.collect()
            # Screenshot
            sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))

        # Hooking the fish
        print("Fish Hooked")
        pyautogui.click()
        time.sleep(animationSleepTime)

        # Keeps reeling into "HOLD Cast" text shows on screen
        while pyautogui.locate("imgs/holdCast.png", sctImg, grayscale=True, confidence=.55) is None:
           
            pyautogui.mouseDown()

            # If icon is in the orange area slack the line
            if pyautogui.locate("imgs/fishReelingOrange.png", sctImg, grayscale=True, confidence=.75) is not None:
                print("Slacking line...")
                pyautogui.mouseUp()
                time.sleep(lineSlackTime)

            # Uses a lot of memory if you don't force collection
            gc.collect()
            # Screenshot
            sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))

            # Reel down time
            time.sleep(animationSleepTime)

        pyautogui.mouseUp()
        time.sleep(animationSleepTime)
        i = i+1
        print("Caught Fish #{0}".format(i) )
        
            
        # 20% chance to move to avoid AFK timer
        if random.randint(1, 5) == 5:
            key = moveDirection[random.randint(0, 1)]
            pyautogui.keyDown(key)
            time.sleep(.1)
            pyautogui.keyUp(key)

        time.sleep(animationSleepTime)

        # Release the "Free Look" Button
        print("Released Free Look Button")
        pydirectinput.keyUp(freeCamKey)
        
        #repair rod
        if i == 100:
            print("repair Rod")
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.moveTo(870,508)
            time.sleep(1)
            pyautogui.keyDown('r')
            time.sleep(1)
            pyautogui.click()
            time.sleep(1)
            pyautogui.keyUp('r')
            time.sleep(1)
            pyautogui.press('e')
            time.sleep(1)
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.press('f3')
            time.sleep(5)
# Runs the main function
if __name__ == '__main__':
    main()
