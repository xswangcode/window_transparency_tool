
---

# 窗口透明度工具

这是一个用于调整 Windows 窗口透明度的工具，支持通过快捷键和系统托盘图标操作。工具提供了多种方法来设置窗口透明度，并支持日志记录和错误处理。

## 功能特性

1. **调整窗口透明度**：
   - 支持通过快捷键调整当前活动窗口的透明度。
   - 支持恢复默认透明度。

2. **快捷键支持**：
   - `Ctrl + Alt + Up`：增加窗口透明度（窗口变得更透明）。
   - `Ctrl + Alt + Down`：降低窗口透明度（窗口变得更不透明）。
   - `Ctrl + Alt + 0`：恢复窗口默认透明度。

3. **系统托盘图标**：
   - 程序启动后最小化到系统托盘。
   - 右键点击托盘图标可退出程序。

4. **日志记录**：
   - 记录程序运行时的调试信息和错误日志。
   - 日志文件保存在 `logs/window_transparency_tool.log`。
   - 生产环境下并未记录日志

5. **打包支持**：
   - 支持通过 `pyinstaller` 打包为独立的 exe 文件。

---

## 使用方法

### 1. 安装依赖

确保已安装 Python 3.7 或更高版本，然后安装以下依赖库：

```bash
pip install pywin32 keyboard pystray Pillow pyinstaller
```

### 2. 运行程序

直接运行脚本：

```bash
python main.py
```

### 3. 使用快捷键

- **增加透明度**：`Ctrl + Alt + Up`
- **降低透明度**：`Ctrl + Alt + Down`
- **恢复默认透明度**：`Ctrl + Alt + 0`

### 4. 系统托盘操作

- 右键点击托盘图标，选择“退出”以关闭程序。

---

## 打包为 exe 文件

使用 `pyinstaller` 将脚本打包为 exe 文件：

```bash

pyinstaller --onefile --windowed --icon=icon.ico --add-data=".\icon.png;." --hidden-import pystray --clean main.py
```

- `--onefile`：打包为单个 exe 文件。
- `--windowed`：不显示控制台窗口。
- `--icon=icon.ico`：指定 exe 文件的图标。

打包完成后，exe 文件会出现在 `dist` 目录中。

---

## 项目结构

```
window_transparency_tool/
├── main.py  # 主程序脚本
├── icon.png                     # 托盘图标文件
├── icon.ico                     # exe 文件图标
├── README.md                    # 项目说明文件
├── window_transparency_tool.log # 日志文件
├── dist                         # 项目说明文件
      └── main.exe               # 最新编译后的文件
```

---

## 依赖项

- `pywin32`：用于与 Windows API 交互。
- `keyboard`：用于监听和响应快捷键。
- `pystray`：用于创建系统托盘图标。
- `Pillow`：用于加载托盘图标。

---

## 注意事项

1. **管理员权限**：
   - 某些窗口可能需要管理员权限才能修改透明度。可以通过右键点击 exe 文件并选择“以管理员身份运行”来解决。

2. **图标文件**：
   - 确保 `icon.png` 和 `icon.ico` 文件存在，并放在脚本同级目录下。

3. **日志文件**：
   - 日志文件默认保存在 `logs/window_transparency_tool.log`，方便排查问题。

---

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

---

## 作者

- **xswang  wxs_code@126.com**
- **deepseek** **https://www.deepseek.com/**



---
