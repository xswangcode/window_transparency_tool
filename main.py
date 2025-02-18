import win32gui
import win32con
import win32api
import logging
import os
import sys
import time
import subprocess
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading

# 日志配置
# def setup_logger.():
#     log_dir = "logs"
#     if not os.path.exists(log_dir):
#         os.makedirs(log_dir)
#     log_file = os.path.join(log_dir, "window_transparency_tool.log")
#     logging.basicConfig(
#         level=logging.DEBUG,
#         format="%(asctime)s - %(levelname)s - %(message)s",
#         handlers=[
#             logging.FileHandler(log_file),
#             logging.StreamHandler(sys.stdout)
#         ]
#     )
#     return logging.get# logger.()

# logger = setup_logger()

# 获取当前活动窗口
def get_active_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        # logger..debug(f"当前活动窗口句柄: {hwnd}")
        return hwnd
    except Exception as e:
        # logger..error(f"获取活动窗口失败: {e}")
        return None

# 通过 nircmd 执行 DOS 命令修改透明度
def set_window_transparency_with_nircmd(hwnd, transparency):
    try:
        # 计算透明度值 (0到255之间)
        transparency_value = int((transparency / 255) * 100)  # 将透明度值转换为 0 到 100 之间的百分比

        # 使用 nircmd 命令来设置透明度
        nircmd_command = f"nircmd.exe win transparency {hwnd} {transparency_value}"
        result = subprocess.run(nircmd_command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            # logger..info(f"已使用 nircmd 设置窗口 {hwnd} 的透明度为 {transparency}")
            return True
        else:
            # logger..error(f"nircmd 执行失败: {result.stderr}")
            return False
    except Exception as e:
        # logger..error(f"通过 nircmd 设置透明度失败: {e}")
        return False

# 设置窗口透明度的多种方法
def set_window_transparency(hwnd, transparency):
    try:
        # 方法 1: 使用 SetLayeredWindowAttributes
        try:
            # 强制为窗口设置 WS_EX_LAYERED 样式
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                                   win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
            win32gui.SetLayeredWindowAttributes(hwnd, 0, transparency, win32con.LWA_ALPHA)
            # logger..info(f"已使用 SetLayeredWindowAttributes 设置窗口 {hwnd} 的透明度为 {transparency}")
            return True
        except Exception as e:
            pass
            # logger..error(f"使用 SetLayeredWindowAttributes 设置透明度失败: {e}")
        
        # 方法 2: 尝试直接操作窗口样式
        try:
            # 设置透明度时, 需要为窗口添加 WS_EX_LAYERED 样式
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            new_style = style | win32con.WS_EX_LAYERED
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)
            # logger..info(f"已使用 SetWindowLong 设置窗口 {hwnd} 为 WS_EX_LAYERED 样式")

            # 使用透明度值进行设置
            win32gui.SetLayeredWindowAttributes(hwnd, 0, transparency, win32con.LWA_ALPHA)
            # logger..info(f"已通过 SetWindowLong 设置窗口 {hwnd} 的透明度为 {transparency}")
            return True
        except Exception as e:
            pass
            # logger..error(f"使用 SetWindowLong 设置透明度失败: {e}")

        # 方法 3: 强制设置窗口为透明并显示
        try:
            # 直接设置窗口样式并尝试调整透明度
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                                   win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
            # 将透明度设置到最小值
            win32gui.SetLayeredWindowAttributes(hwnd, 0, transparency, win32con.LWA_ALPHA)
            # logger..info(f"强制通过方法3设置透明度成功：窗口 {hwnd} 的透明度设置为 {transparency}")
            return True
        except Exception as e:
            pass
            # logger..error(f"强制方法3设置透明度失败: {e}")

        return False  # 如果所有方法都失败，返回 False
    except Exception as e:
        # logger..error(f"设置窗口透明度失败: {e}")
        return False

 
def set_window_layered(hwnd):
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    if not (style & win32con.WS_EX_LAYERED):
        new_style = style | win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)
        # logger..info(f"为窗口 {hwnd} 设置了 WS_EX_LAYERED 样式")
# 增加透明度 
def increase_transparency():
    hwnd = get_active_window()
    if hwnd:
        try:
            set_window_layered(hwnd)  # Ensure the window is layered
            current_transparency = win32gui.GetLayeredWindowAttributes(hwnd)[1]
            # alert弹框提示当前透明度
            # print(win32gui.GetLayeredWindowAttributes(hwnd))
            # print(f"当前透明度: {current_transparency}")  # Add this line for debugging
            new_transparency = min(255, current_transparency + 10)  # Decrease transparency
            success = set_window_transparency(hwnd, new_transparency)
            # if not success:
            #     # Try using nircmd if win32 method fails
            #     set_window_transparency_with_nircmd(hwnd, new_transparency)
        except Exception as e:
            pass
            # logger..error(f"增加透明度失败: {e}")


# 降低透明度
def decrease_transparency():
    hwnd = get_active_window()
    if hwnd:
        try:
            set_window_layered(hwnd)  # Ensure the window is layered
            current_transparency = win32gui.GetLayeredWindowAttributes(hwnd)[1]
            new_transparency = max(25, current_transparency - 10)  # Increase transparency
            success = set_window_transparency(hwnd, new_transparency)
            # if not success:
            #     # Try using nircmd if win32 method fails
            #     set_window_transparency_with_nircmd(hwnd, new_transparency)
        except Exception as e:
            pass
            # logger..error(f"降低透明度失败: {e}")

# 恢复默认透明度
def reset_transparency_to_default():
    hwnd = get_active_window()
    if hwnd:
        try:
            set_window_layered(hwnd)  # 确保窗口是分层的
            default_transparency = 255  # 默认完全不透明
            success = set_window_transparency(hwnd, default_transparency)
            # if not success:
            #     # 如果 win32 方法失败，尝试使用 nircmd
            #     set_window_transparency_with_nircmd(hwnd, default_transparency)
            # # logger..info(f"已将窗口 {hwnd} 的透明度恢复为默认值 {default_transparency}")
        except Exception as e:
            pass
            # print(f"恢复默认透明度失败: {e}")




# 托盘图标功能
def setup_tray_icon():
    # 定义退出函数
    def on_quit(icon):
        # logger..info("程序退出中...")
        icon.stop()
        os._exit(0)

    # 创建托盘图标
    icon_path = os.path.join(sys._MEIPASS, "icon.png") if hasattr(sys, '_MEIPASS') else "./icon.png"
    image = Image.open(icon_path)  # 你需要准备一个图标文件 icon.png
    menu = Menu(
        # MenuItem("增加透明度", increase_transparency),
        # MenuItem("降低透明度", decrease_transparency),
        MenuItem("退出", on_quit)
    )
    icon = Icon("窗口透明度工具", image, "窗口透明度工具", menu)
    return icon

# 主程序
def main():
    # logger..info("启动窗口透明度工具...")

    # 启动托盘图标
    tray_icon = setup_tray_icon()
    threading.Thread(target=tray_icon.run, daemon=True).start()

    # 添加快捷键
    import keyboard
    keyboard.add_hotkey('ctrl+alt+up', increase_transparency)
    keyboard.add_hotkey('ctrl+alt+down', decrease_transparency)
    keyboard.add_hotkey('ctrl+alt+0', reset_transparency_to_default)  # 新增快捷键

    # 保持程序运行
    # logger..info("程序正在运行，按 'CTR + Esc' 退出。")
    keyboard.wait('ctrl+esc')
    # logger..info("程序退出中...")
    tray_icon.stop()

if __name__ == "__main__":
    main()
