import win32gui
import win32con
import logging
import win32event
import winerror
import win32api
import os
import io
import base64
import sys
import time
import subprocess
import threading
import keyboard
from pystray import Icon, Menu, MenuItem
from PIL import Image


icon_base64  = "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"


# 日志配置
def setup_logger():
    log_file = os.path.join(os.path.dirname(__file__), "window_transparency_tool.log")
    logging.basicConfig(
        level=logging.NOTSET,  # 将日志级别调整为DEBUG，以便开发时调试
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger()

logger = setup_logger()

# 获取当前活动窗口
def get_active_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        logger.info(f"当前活动窗口句柄: {hwnd}")
        return hwnd
    except Exception as e:
        logger.error(f"获取活动窗口失败: {e}")
        return None

# 设置窗口透明度


def set_window_transparency(hwnd, transparency):
    try:
        # 方法 1: 使用 SetLayeredWindowAttributes
        try:
            # 强制为窗口设置 WS_EX_LAYERED 样式
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
            win32gui.SetLayeredWindowAttributes(hwnd, 0, transparency, win32con.LWA_ALPHA)
            # logger.info(f"已使用 SetLayeredWindowAttributes 设置窗口 {hwnd} 的透明度为 {transparency}")
            return True
        except Exception as e: 
            logger.error(f"使用 SetLayeredWindowAttributes 设置透明度失败: {e}")
        
        # 方法 2: 尝试直接操作窗口样式
        try:
            # 设置透明度时, 需要为窗口添加 WS_EX_LAYERED 样式
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            new_style = style | win32con.WS_EX_LAYERED
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)
            logger.info(f"已使用 SetWindowLong 设置窗口 {hwnd} 为 WS_EX_LAYERED 样式")

            # 使用透明度值进行设置
            win32gui.SetLayeredWindowAttributes(hwnd, 0, transparency, win32con.LWA_ALPHA)
            logger.info(f"已通过 SetWindowLong 设置窗口 {hwnd} 的透明度为 {transparency}")
            return True
        except Exception as e: 
            logger.error(f"使用 SetWindowLong 设置透明度失败: {e}")

        # 方法 3: 强制设置窗口为透明并显示
        try:
            # 直接设置窗口样式并尝试调整透明度
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
            # 将透明度设置到最小值
            win32gui.SetLayeredWindowAttributes(hwnd, 0, transparency, win32con.LWA_ALPHA)
            logger.info(f"强制通过方法3设置透明度成功：窗口 {hwnd} 的透明度设置为 {transparency}")
            return True
        except Exception as e: 
            logger.error(f"强制方法3设置透明度失败: {e}")

        return False  # 如果所有方法都失败，返回 False
    except Exception as e:
        logger.error(f"设置窗口透明度失败: {e}")
        return False

def set_window_layered(hwnd):
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    if not (style & win32con.WS_EX_LAYERED):
        new_style = style | win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)
        logger.info(f"为窗口 {hwnd} 设置了 WS_EX_LAYERED 样式")

# 增加/减少透明度的统一处理函数
def adjust_transparency(increase=True):
    hwnd = get_active_window()
    if hwnd:
        try:
            set_window_layered(hwnd)
            current_transparency = win32gui.GetLayeredWindowAttributes(hwnd)[1] or 255  # 获取当前透明度
            logger.info(f"当前透明度: {current_transparency}")

            delta = 5 if increase else -5
            new_transparency = max(25, min(255, current_transparency + delta))  # 限制在 25 到 255 之间
            success = set_window_transparency(hwnd, new_transparency)
            if success:
                logger.info(f"透明度调整至: {new_transparency}")
            else:
                logger.error("透明度调整失败")
        except Exception as e:
            logger.error(f"调整透明度失败: {e}")

# 恢复默认透明度
def reset_transparency_to_default():
    hwnd = get_active_window()
    if hwnd:
        try:
            set_window_layered(hwnd)
            default_transparency = 255  # 默认完全不透明
            success = set_window_transparency(hwnd, default_transparency)
            if success:
                logger.info(f"已恢复窗口透明度为默认值 {default_transparency}")
        except Exception as e:
            logger.error(f"恢复透明度失败: {e}")

# 显示帮助信息
def show_message_box(message):
    win32gui.MessageBox(None, message, "帮助", win32con.MB_OK)

def helper():
    message = "使用说明：\nCtrl + Alt  +0  -  恢复默认透明度\nCtrl + Alt + U - 降低透明度\nCtrl + Alt + D  -  增加透明度"
    threading.Thread(target=show_message_box,args=(message,), daemon=True).start()

# 重启程序
def restart(): 
    if sys.executable.endswith("python.exe"):
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        try:
            executable = sys.executable
            args = sys.argv
            keyboard.unhook_all_hotkeys()
            subprocess.Popen([executable] + args)
            os._exit(0)
        except Exception as e:
            restart()

# 修改托盘图标功能
def setup_tray_icon():
    def on_quit(icon):
        try:
            icon.stop()  # 停止系统托盘图标
            keyboard.unhook_all_hotkeys()  # 移除所有键盘钩子
        finally:
            os._exit(0)  # 强制终止进程

    # 使用嵌入的圖像數據
    icon_data = base64.b64decode(icon_base64)
    image = Image.open(io.BytesIO(icon_data))
    menu = Menu(
        MenuItem("帮助", helper),
        MenuItem("重启", restart),
        MenuItem("退出", on_quit)
    )
    return Icon("窗口透明度工具", image, "窗口透明度工具", menu)




def main():

    # 初始化系统托盘
    tray_icon = setup_tray_icon()
    tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
    tray_thread.start()

    # 注册热键
    keyboard.add_hotkey('ctrl+alt+u', lambda: adjust_transparency(increase=True))
    keyboard.add_hotkey('ctrl+alt+d', lambda: adjust_transparency(increase=False))
    keyboard.add_hotkey('ctrl+alt+0', reset_transparency_to_default)

    logger.info("程序正在运行，按 'CTRL+ESC' 退出。")
    
    try:
        keyboard.wait('ctrl+esc')
    finally:
        if tray_icon:
            tray_icon.stop()
        if tray_thread:
            tray_thread.join(timeout=1)
        keyboard.unhook_all_hotkeys()
        os._exit(0)  # 确保退出

# 保证只有一个实例正在运行

if __name__ == "__main__":
    try:
        mutex = win32event.CreateMutex(None, False, "WindowTransparencyToolMutex")

        # 检查互斥体是否已经存在
        if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
            # 如果互斥体已经存在，说明已经有另一个实例正在运行
            show_message_box("另一个实例正在运行，程序将退出。")
            sys.exit()
        main()
    except Exception as e:
        show_message_box(f"程序异常退出: {e}")
