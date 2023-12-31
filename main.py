import ctypes
import win32api
import time
import win32process
import pyautogui

window_handle = 200542
velocity_addr = 0x5B86962C
speed_level_addr = 0x5A7BA8BA
screenMouseX, screenMouseY = 0, 0
speed_level = 0
target = 40


def game_focus():
    pyautogui.click(screenMouseX, screenMouseY)


def keyboard_register():
    global screenMouseX, screenMouseY
    print("移动鼠标到游戏，保持3秒")
    input("准备好：")

    time.sleep(1)
    print("[鼠标保持] 1")
    time.sleep(1)
    print("[鼠标保持] 2")
    time.sleep(1)

    screenMouseX, screenMouseY = pyautogui.position()
    pyautogui.click()


def vehicle_speed_up(level):
    # TODO: 操作前，控制鼠标点击游戏，控制完后，将鼠标还原
    global speed_level
    level = int(level)
    while True:
        fetch_speed_level()
        if speed_level < 4 and speed_level < level:
            game_focus()
            pyautogui.keyDown("A")
            time.sleep(0.1)
            pyautogui.keyUp("A")
        else:
            break


def vehicle_speed_down(level):
    global speed_level
    level = int(level)
    while True:
        fetch_speed_level()
        if speed_level > -4 and speed_level > level:
            game_focus()
            pyautogui.keyDown("D")
            time.sleep(0.1)
            pyautogui.keyUp("D")
        else:
            break


def pid(expect, current):
    K = 10
    error = expect - current
    out = K * error
    if out > 0:
        vehicle_speed_up(out)
    elif out < 0:
        # deacceleration use -1
        vehicle_speed_down(-1)
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
    if speed_level_src.value & 0x00FF0000:
        tmp = ((speed_level_src.value & 0xFF) - 48) * 10
        tmp += ((speed_level_src.value & 0x00FF0000) >> 16) - 48
        if tmp == 10:
            tmp = 100
        speed_level = -tmp / 25
    else:
        speed_level = (speed_level_src.value & 0xFF) - 48


keyboard_register()

while True:
    velocity = ctypes.c_float()
    kernel32.ReadProcessMemory(
        int(process_handle), velocity_addr, ctypes.byref(velocity), 4, None
    )
    fetch_speed_level()
    print("列车时速：%.2f, 节流阀：%d" % (velocity.value, speed_level))
    fp = open("speed", "r")
    target_vec = float(fp.read())
    fp.close()
    pid(target_vec, velocity.value)
    time.sleep(0.2)
