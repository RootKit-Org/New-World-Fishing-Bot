import pyautogui
import pygetwindow
import pydirectinput
import time
import random
import mss
import numpy as np
from PIL import Image
import gc
import win32api
import win32con
import bettercam
import cv2

def main():
    """
    Main function for the program
    """
    # Max cast is 1.9 secs
    # Base time it will always cast at
    castingBaseTime = 1.0
    # Max random amount of time to add to the base
    castingRandom = .4

    # How long to slack the line
    lineSlackTime = 1.5

    # Adding randomness to the wait times for the animations
    animationSleepTime = .1 + (.1 * random.random())

    # Randomly will move right or left to keep from AFKing
    moveDirection = ["a", "d"]

    # Free cam key
    freeCamKey = "alt"

    visuals = False

    # Finds all Windows with the title "New World"
    newWorldWindows = pygetwindow.getWindowsWithTitle("New World")

    # TODO - Fix this, cause it could choose the wrong window
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

    print(centerH, centerW)
    # pyautogui.moveTo(centerW, centerH)
    # win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE, int(centerW), int(centerH), 0, 0)

    win32api.SetCursorPos((int(centerW), int(centerH)))

    # Clicky Clicky
    time.sleep(animationSleepTime)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(animationSleepTime)

    # TODO - newWorldWindow.top keeps giving a negative number, so I'm just going to use 0 for now
    region = (
        newWorldWindow.left + round(newWorldWindow.width/3),
        newWorldWindow.top,
        newWorldWindow.left + (round(newWorldWindow.width/3)*2),
        newWorldWindow.top + newWorldWindow.height
    )

    camera = bettercam.create(region=region, output_color="BGRA", max_buffer_len=512)
    camera.start(target_fps=120, video_mode=True)
    # This should resolve issues with the first cast being short
    time.sleep(2)

    while win32api.GetAsyncKeyState(ord("Q")) == 0:

        npImg = np.array(camera.get_latest_frame())
        npImg = npImg[:, :, 0:3]

        sctImg = Image.fromarray(npImg)

        if visuals:
            cv2.imshow('Live Feed', npImg)
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                exit()

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

        time.sleep(2)

        c = 0
        while win32api.GetAsyncKeyState(ord("Q")) == 0:
            sctImg = Image.fromarray(np.array(camera.get_latest_frame()))
            try:
                # Looking for the fish icon, doing forced garbage collection
                if pyautogui.locate("imgs/fishIcon.png", sctImg, grayscale=True, confidence=.65) is not None:
                    break
            except Exception as e:
                # print("Fish not found")
                # print(c)
                c += 1
                continue

        # Hooking the fish
        print("Fish Hooked")
        pyautogui.click()
        time.sleep(2)

        # Keeps reeling into "HOLD Cast" text shows on screen
        while win32api.GetAsyncKeyState(ord("Q")) == 0:
            sctImg = Image.fromarray(np.array(camera.get_latest_frame()))

            try:
                if pyautogui.locate("imgs/fishHook.png", sctImg, grayscale=True, confidence=.55) is not None:
                    break
            except Exception as e:
                pass
            print("Reeling....")
            pyautogui.mouseDown()

            try:
                # If icon is in the orange area slack the line
                if pyautogui.locate("imgs/fishReelingOrange.png", sctImg, grayscale=True, confidence=.75) is not None:
                    print("Slacking line...")
                    pyautogui.mouseUp()
                    time.sleep(lineSlackTime)
            except Exception as e:
                pass

            # Uses a lot of memory if you don't force collection
            gc.collect()
            # Screenshot
            sctImg = Image.fromarray(npImg)

            # Reel down time
            time.sleep(animationSleepTime)


        pyautogui.mouseUp()
        time.sleep(animationSleepTime)
        print("Caught Fish")

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


# Runs the main function
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
    
    pydirectinput.keyUp('alt')
