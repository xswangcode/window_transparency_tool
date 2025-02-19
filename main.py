import win32gui
import win32con
import logging
import os
import sys
import threading
import keyboard
from pystray import Icon, Menu, MenuItem
from PIL import Image
from tkinter import simpledialog
import tkinter as tk


# 日志配置
def setup_logger():
    log_file = os.path.join(os.path.dirname(__file__), "window_transparency_tool.log")
    logging.basicConfig(
        level=logging.ERROR,  # 将日志级别调整为DEBUG，以便开发时调试
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
        logger.debug(f"当前活动窗口句柄: {hwnd}")
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
            # logger.debug(f"已使用 SetLayeredWindowAttributes 设置窗口 {hwnd} 的透明度为 {transparency}")
            return True
        except Exception as e: 
            logger.error(f"使用 SetLayeredWindowAttributes 设置透明度失败: {e}")
        
        # 方法 2: 尝试直接操作窗口样式
        try:
            # 设置透明度时, 需要为窗口添加 WS_EX_LAYERED 样式
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            new_style = style | win32con.WS_EX_LAYERED
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)
            logger.debug(f"已使用 SetWindowLong 设置窗口 {hwnd} 为 WS_EX_LAYERED 样式")

            # 使用透明度值进行设置
            win32gui.SetLayeredWindowAttributes(hwnd, 0, transparency, win32con.LWA_ALPHA)
            logger.debug(f"已通过 SetWindowLong 设置窗口 {hwnd} 的透明度为 {transparency}")
            return True
        except Exception as e: 
            logger.error(f"使用 SetWindowLong 设置透明度失败: {e}")

        # 方法 3: 强制设置窗口为透明并显示
        try:
            # 直接设置窗口样式并尝试调整透明度
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
            # 将透明度设置到最小值
            win32gui.SetLayeredWindowAttributes(hwnd, 0, transparency, win32con.LWA_ALPHA)
            logger.debug(f"强制通过方法3设置透明度成功：窗口 {hwnd} 的透明度设置为 {transparency}")
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
        logger.debug(f"为窗口 {hwnd} 设置了 WS_EX_LAYERED 样式")

# 增加/减少透明度的统一处理函数
def adjust_transparency(increase=True):
    hwnd = get_active_window()
    if hwnd:
        try:
            set_window_layered(hwnd)
            current_transparency = win32gui.GetLayeredWindowAttributes(hwnd)[1] or 255  # 获取当前透明度
            logger.debug(f"当前透明度: {current_transparency}")

            delta = 5 if increase else -5
            new_transparency = max(25, min(255, current_transparency + delta))  # 限制在 25 到 255 之间
            success = set_window_transparency(hwnd, new_transparency)
            if success:
                logger.debug(f"透明度调整至: {new_transparency}")
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
                logger.debug(f"已恢复窗口透明度为默认值 {default_transparency}")
        except Exception as e:
            logger.error(f"恢复透明度失败: {e}")

# 显示帮助信息
def show_message_box():
    message = "使用说明：\nCtrl+Alt+0 - 恢复默认透明度\nCtrl+Alt+上箭头 - 增加透明度\nCtrl+Alt+下箭头 - 降低透明度"
    win32gui.MessageBox(None, message, "帮助", win32con.MB_OK)

def helper():
    threading.Thread(target=show_message_box, daemon=True).start()


# 托盘图标功能
def setup_tray_icon():
    def on_quit(icon):
        icon.stop()
        os._exit(0)

    icon_path = os.path.join(sys._MEIPASS, "icon.png") if hasattr(sys, '_MEIPASS') else "./icon.png"
    image = Image.open(icon_path)
    menu = Menu(
        MenuItem("帮助", helper),
        # MenuItem("自定义透明度", custom_transparency),
        # MenuItem("切换透明度模式", toggle_transparency_mode),
        MenuItem("退出", on_quit)
    )
    icon = Icon("窗口透明度工具", image, "窗口透明度工具", menu)
    return icon

# 主程序
def main():
    tray_icon = setup_tray_icon()
    threading.Thread(target=tray_icon.run, daemon=True).start()

    # 添加快捷键
    keyboard.add_hotkey('ctrl+alt+up', lambda: adjust_transparency(increase=True))
    keyboard.add_hotkey('ctrl+alt+down', lambda: adjust_transparency(increase=False))
    keyboard.add_hotkey('ctrl+alt+0', reset_transparency_to_default)

    logger.debug("程序正在运行，按 'CTRL+Esc' 退出。")
    keyboard.wait('ctrl+esc')
    tray_icon.stop()

if __name__ == "__main__":
    main()
