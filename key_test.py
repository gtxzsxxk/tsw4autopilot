import pyautogui
import time

print("移动鼠标到游戏，HOLD3秒")
input("准备好回车")
time.sleep(1)
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)
currentMouseX, currentMouseY = pyautogui.position()
print("鼠标坐标位置：", currentMouseX, currentMouseY)

print("通过点击获取焦点")
pyautogui.click()


print("加速1档")
pyautogui.keyDown('A')
time.sleep(0.1)
pyautogui.keyUp('A')
print("加速2档")
pyautogui.keyDown('A')
time.sleep(0.1)
pyautogui.keyUp('A')

print("减速1档")
pyautogui.keyDown('D')
time.sleep(0.1)
pyautogui.keyUp('D')

print("减速0档")
pyautogui.keyDown('D')
time.sleep(0.1)
pyautogui.keyUp('D')

print("减速-1档")
pyautogui.keyDown('D')
time.sleep(0.1)
pyautogui.keyUp('D')

print("加速0档")
pyautogui.keyDown('A')
time.sleep(0.1)
pyautogui.keyUp('A')

print("加速1档")
pyautogui.keyDown('A')
time.sleep(0.1)
pyautogui.keyUp('A')
