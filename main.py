import ctypes
import win32api
import time
import win32process
import pyautogui

window_handle = 200542
velocity_addr = 0x5B86962C
speed_level_addr = 0x5A7BA8Ba
currentMouseX, currentMouseY = 0,0
speed_level = 0
target = 40

def keyboard_register():
    global currentMouseX, currentMouseY
    print("移动鼠标到游戏，保持3秒")
    input("准备好：")
    
    time.sleep(1)
    print("[鼠标保持] 1")
    time.sleep(1)
    print("[鼠标保持] 2")
    time.sleep(1)
    
    currentMouseX, currentMouseY = pyautogui.position()
    pyautogui.click()
    
def vehicle_speed_up(level):
    global speed_level
    level = int(level)
    level %= 4
    while True:
        fetch_speed_level()
        if speed_level < 4 and speed_level < level:
            pyautogui.keyDown('A')
            time.sleep(0.1)
            pyautogui.keyUp('A')
        else:
            break
        
def vehicle_speed_down(level):
    global speed_level
    level = int(level)
    level %= 4
    while True:
        fetch_speed_level()
        if speed_level > -4 and speed_level > level:
            pyautogui.keyDown('D')
            time.sleep(0.1)
            pyautogui.keyUp('D')
        else:
            break
        
def pid(expect, current):
    K = 10
    error = expect - current
    out = K * error
    if out > 0:
        vehicle_speed_up(out)
    elif out < 0:
        vehicle_speed_down(out)
    print("PID output: %.2f, Thres Level: %d" % (out, speed_level))

kernel32 = ctypes.windll.LoadLibrary(r"kernel32.dll")  # 核心文件
PROCESS_ALL_ACCESS = 0x000F0000 | 0x00100000 | 0xFFF  # 调用最高权限执行
process_id = win32process.GetWindowThreadProcessId(window_handle)[1]  # 获取进程ID
process_handle = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, process_id)  # 得到进程句柄

def fetch_speed_level():
    global speed_level
    speed_level_src = ctypes.c_int32()
    kernel32.ReadProcessMemory(
        int(process_handle), speed_level_addr, ctypes.byref(speed_level_src), 4, None
    )
    if speed_level_src.value & 0x00ff0000:
        tmp = ((speed_level_src.value & 0xff) - 48 ) * 10
        tmp += ((speed_level_src.value & 0x00ff0000) >> 16) - 48
        speed_level = - tmp / 25
    else:
        speed_level = (speed_level_src.value & 0xff) - 48

keyboard_register()

while True:
    velocity = ctypes.c_float()
    kernel32.ReadProcessMemory(
        int(process_handle), velocity_addr, ctypes.byref(velocity), 4, None
    )
    fetch_speed_level()
    print("列车时速：%.2f, 节流阀：%d" % (velocity.value, speed_level))
    pid(120, velocity.value)
    time.sleep(0.2)
