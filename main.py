import ctypes
import win32api
import time
import win32process  # 进程模块

window_handle = 134634

kernel32 = ctypes.windll.LoadLibrary(r"kernel32.dll")  # 核心文件
PROCESS_ALL_ACCESS = 0x000F0000 | 0x00100000 | 0xFFF  # 调用最高权限执行
process_id = win32process.GetWindowThreadProcessId(window_handle)[1]  # 获取进程ID
process_handle = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, process_id)  # 得到进程句柄

while True:
    velocity = ctypes.c_float()
    kernel32.ReadProcessMemory(
        int(process_handle), 0x57B6882C, ctypes.byref(velocity), 4, None
    )
    print("列车时速：%.2f" % velocity.value)
    time.sleep(1)
