import pyautogui
import pydirectinput
import time
import random
import gc

def main():
    """
    Main function for the program
    """
    # Max cast is 1.9 secs
    # Base time it will always cast at
    castingBaseTime = 1.0
    # Max random amount of time to add to the base
    castingRandom = .4

    # Base reeling time it will always do
    reelingBaseTime = .3
    # Max random amount of time to add to the base
    reelingRandom = .2

    # Adding randomness to the wait times for the animations
    animationSleepTime = .1 + (.1 * random.random())

    # Randomly will move right or left to keep from AFKing
    moveDirection = ["a", "d"]

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
    region = (newWorldWindow.left + round(newWorldWindow.width/3), newWorldWindow.top, round(newWorldWindow.width/3), newWorldWindow.height)

    while True:
        # Calculating those times
        castingTime = castingBaseTime + (castingRandom * random.random())
        reelingTime = reelingBaseTime + (reelingRandom * random.random())

        # Like it says, casting
        print("Casting Line")
        pyautogui.mouseDown()
        time.sleep(castingTime)
        pyautogui.mouseUp()

        # Looking for the fish icon, doing forced garbage collection
        while pyautogui.locateOnScreen("imgs/fishIcon.png", grayscale=True, confidence=.6, region=region) is None:
            gc.collect()

        # Hooking the fish
        print("Fish Hooked")
        pyautogui.click()
        time.sleep(animationSleepTime)

        # Keeps reeling into "HOLD Cast" text shows on screen
        while pyautogui.locateOnScreen("imgs/holdCast.png", grayscale=True, confidence=.55, region=region) is None:
            print("Reeling....")
            pyautogui.mouseDown()
            time.sleep(reelingTime)
            pyautogui.mouseUp()

            # Uses a lot of memory if you don't force collection
            gc.collect()

            # Uncomment below if you want more randomness in your reeling rest periods
            # time.sleep(animationSleepTime)

        print("Caught Fish")

        # 20% chance to move to avoid AFK timer
        if random.randint(1, 5) == 5:
            pyautogui.press(moveDirection[random.randint(0, 1)])

        time.sleep(animationSleepTime)


# Runs the main function
if __name__ == '__main__':
    main()
