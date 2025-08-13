# PyQt Toast

<img src="https://socialify.git.ci/Cassianvale/pyqttoast/image?font=Source+Code+Pro&language=1&name=1&pattern=Diagonal+Stripes&theme=Auto" alt="pyqttoast" width="640" height="320" />

[![PyPI](https://img.shields.io/badge/pypi-v1.3.3-blue)](https://pypi.org/project/pyqt-toast-notification/)
[![Python](https://img.shields.io/badge/python-3.7+-blue)](https://github.com/niklashenning/pyqttoast)
[![Build](https://img.shields.io/badge/build-passing-neon)](https://github.com/niklashenning/pyqttoast)
[![Coverage](https://img.shields.io/badge/coverage-94%25-green)](https://github.com/niklashenning/pyqttoast)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/niklashenning/pyqttoast/blob/master/LICENSE)

**语言:** [English](README.md) | ➡️*中文*

一个完全可定制的现代化 PyQt 和 PySide 通知库

![pyqttoast](https://github.com/niklashenning/pyqt-toast/assets/58544929/c104f10e-08df-4665-98d8-3785822a20dc)

## ✨ 主要特性
* **现代边距API** - 灵活高效的边距管理，支持多种输入格式
* **高级动画控制** - 独立的位置和动画方向控制
* **性能优化** - 缓存样式表、正则表达式和优化渲染
* **多通知支持** - 同时显示多个通知，智能队列管理
* **7种位置选项** - 灵活定位，包括屏幕中央
* **多屏幕支持** - 在多个显示器间无缝工作
* **组件相对定位** - 相对于特定组件定位通知
* **现代UI** - 完全可定制的外观，预设样式
* **跨平台** - 支持 `PyQt5`、`PyQt6`、`PySide2` 和 `PySide6`

## 安装
```
pip install pyqt-toast-notification
```

## 使用方法
导入 `Toast` 类，实例化它，然后使用 `show()` 方法显示通知：

```python
from PyQt6.QtWidgets import QMainWindow, QPushButton
from pyqttoast import Toast, ToastPreset


class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        # 添加按钮并连接点击事件
        self.button = QPushButton(self)
        self.button.setText('显示通知')
        self.button.clicked.connect(self.show_toast)
    
    # 每次点击按钮时显示通知
    def show_toast(self):
        toast = Toast(self)
        toast.setDuration(5000)  # 5秒后隐藏
        toast.setTitle('成功！确认邮件已发送。')
        toast.setText('请检查您的邮箱以完成注册。')
        toast.applyPreset(ToastPreset.SUCCESS)  # 应用样式预设
        toast.show()
```

> **重要提示：** <br>`Toast` 实例只能显示**一次**。如果您想显示另一个通知，即使内容完全相同，也必须创建另一个实例。


## 自定义设置

* **设置通知位置（<u>静态</u>）：**
```python
Toast.setPosition(ToastPosition.BOTTOM_MIDDLE)  # 默认：ToastPosition.BOTTOM_RIGHT
```
> **可用位置：** <br> `BOTTOM_LEFT`、`BOTTOM_MIDDLE`、`BOTTOM_RIGHT`、`TOP_LEFT`、`TOP_MIDDLE`、`TOP_RIGHT`、`CENTER`


* **设置通知是否始终显示在主屏幕上（<u>静态</u>）：**
```python
Toast.setAlwaysOnMainScreen(True)  # 默认：False
```

* **相对于组件而不是屏幕定位通知（<u>静态</u>）：**
```python
Toast.setPositionRelativeToWidget(some_widget)  # 默认：None
```

* **设置同时显示的通知数量限制（<u>静态</u>）：**
```python
Toast.setMaximumOnScreen(5)  # 默认：3
```
> 如果您尝试显示超过最大数量的通知，它们将被添加到队列中，并在当前显示的通知关闭后立即显示。


* **设置通知之间的垂直间距（<u>静态</u>）：**
```python
Toast.setSpacing(20)  # 默认：10
```

* **设置通知位置的 x 和 y 偏移（<u>静态</u>）：**
```python
Toast.setOffset(30, 55)  # 默认：20, 45
```

* **使通知永久显示直到关闭：**
```python
toast.setDuration(0)  # 默认：5000
```

* **启用或禁用持续时间条：**
```python
toast.setShowDurationBar(False)  # 默认：True
```

* **添加图标：**
```python
toast.setIcon(ToastIcon.SUCCESS)  # 默认：ToastIcon.INFORMATION
toast.setShowIcon(True)           # 默认：False

# 或设置自定义图标：
toast.setIcon(QPixmap('path/to/your/icon.png'))

# 如果您想显示图标而不重新着色，请将图标颜色设置为 None：
toast.setIconColor(None)  # 默认：#5C5C5C
```
> **可用图标：** <br> `SUCCESS`、`WARNING`、`ERROR`、`INFORMATION`、`CLOSE`


* **设置图标大小：**
```python
toast.setIconSize(QSize(14, 14))  # 默认：QSize(18, 18)
```

* **启用或禁用图标分隔符：**
```python
toast.setShowIconSeparator(False)  # 默认：True
```

* **设置关闭按钮对齐方式：**
```python
toast.setCloseButtonAlignment(ToastButtonAlignment.MIDDLE)  # 默认：ToastButtonAlignment.TOP
```
> **可用对齐方式：** <br> `TOP`、`MIDDLE`、`BOTTOM`

* **启用或禁用关闭按钮：**
```python
toast.setShowCloseButton(False)  # 默认：True
```

* **自定义淡入淡出动画持续时间（毫秒）：**
```python
toast.setFadeInDuration(100)   # 默认：250
toast.setFadeOutDuration(150)  # 默认：250
```

* **控制动画方向：**
```python
toast.setAnimationDirection(ToastAnimationDirection.FROM_LEFT)  # 默认：ToastAnimationDirection.AUTO
```
> **可用方向：** <br>
> `AUTO` - 基于通知位置的方向（向后兼容） <br>
> `FROM_TOP` - 从顶部滑入/滑出 <br>
> `FROM_BOTTOM` - 从底部滑入/滑出 <br>
> `FROM_LEFT` - 从左侧滑入/滑出 <br>
> `FROM_RIGHT` - 从右侧滑入/滑出 <br>
> `FADE_ONLY` - 纯透明度动画，无位置移动

* **启用或禁用悬停时重置持续时间：**

```python
toast.setResetDurationOnHover(False)  # 默认：True
```

* **使角落变圆：**
```python
toast.setBorderRadius(3)  # 默认：0
```

* **设置自定义颜色：**
```python
toast.setBackgroundColor(QColor('#292929'))       # 默认：#E7F4F9
toast.setTitleColor(QColor('#FFFFFF'))            # 默认：#000000
toast.setTextColor(QColor('#D0D0D0'))             # 默认：#5C5C5C
toast.setDurationBarColor(QColor('#3E9141'))      # 默认：#5C5C5C
toast.setIconColor(QColor('#3E9141'))             # 默认：#5C5C5C
toast.setIconSeparatorColor(QColor('#585858'))    # 默认：#D9D9D9
toast.setCloseButtonIconColor(QColor('#C9C9C9'))  # 默认：#000000
```

* **设置自定义字体：**
```python
# 初始化字体
font = QFont('Times', 10, QFont.Weight.Bold)

# 设置字体
toast.setTitleFont(font)  # 默认：QFont('Arial', 9, QFont.Weight.Bold)
toast.setTextFont(font)   # 默认：QFont('Arial', 9)
```

* **现代边距管理（新功能）：**
```python
# 简单设置 - 所有边距相同
toast.setMargins(20)

# 精确设置 - 左、上、右、下
toast.setMargins((15, 10, 15, 20))

# 对称设置 - 水平、垂直
toast.setMargins((25, 15))

# 部分更新 - 仅特定边距
toast.setMargins({'left': 30, 'right': 35})

# 不同组件边距
toast.setMargins(10, 'icon')           # 图标边距
toast.setMargins(5, 'text_section')   # 文本区域边距
toast.setMargins(8, 'close_button')   # 关闭按钮边距

# 微调现有边距
toast.adjustMargins(top=8, bottom=12)
toast.adjustMargins('icon', left=5, right=10)
```
> **边距类型：** <br> `content`（默认）、`icon`、`icon_section`、`text_section`、`close_button`

* **应用样式预设：**
```python
toast.applyPreset(ToastPreset.ERROR)
```
> **可用预设：** <br> `SUCCESS`、`WARNING`、`ERROR`、`INFORMATION`、`SUCCESS_DARK`、`WARNING_DARK`、`ERROR_DARK`、`INFORMATION_DARK`

* **设置通知大小约束：**
```python
# 最小和最大大小
toast.setMinimumWidth(100)
toast.setMaximumWidth(350)
toast.setMinimumHeight(50)
toast.setMaximumHeight(120)

# 固定大小（不推荐）
toast.setFixedSize(QSize(350, 80))
```


**<br>其他自定义选项：**

| 选项                          | 描述                                                                     | 默认值                     |
|-------------------------------|--------------------------------------------------------------------------|----------------------------|
| `setFixedScreen()`            | 通知将显示的固定屏幕（静态）                                              | `None`                     |
| `setMovePositionWithWidget()` | 当相对于组件定位时，通知是否应随组件移动                                  | `True`                     |
| `setIconSeparatorWidth()`     | 分隔图标和文本区域的图标分隔符宽度                                        | `2`                        |
| `setCloseButtonIcon()`        | 关闭按钮的图标                                                           | `ToastIcon.CLOSE`          |
| `setCloseButtonIconSize()`    | 关闭按钮图标的大小                                                       | `QSize(10, 10)`            |
| `setCloseButtonSize()`        | 关闭按钮的大小                                                           | `QSize(24, 24)`            |
| `setStayOnTop()`              | 通知是否保持在其他窗口之上，即使其他窗口获得焦点                          | `True`                     |
| `setTextSectionSpacing()`     | 标题和文本之间的垂直间距                                                 | `8`                        |

## API 文档

完整的API参考和高级使用示例，请参阅：
- [Toast API 文档 (中文)](docs/Toast_API_Reference_Table_CN.md) - 详细文档和示例

## 演示
https://github.com/niklashenning/pyqt-toast/assets/58544929/f4d7f4a4-6d69-4087-ae19-da54b6da499d

PyQt5、PyQt6 和 PySide6 的演示可以在 [demo](demo) 文件夹中找到。

## 测试
安装所需的测试依赖项 [PyQt6](https://pypi.org/project/PyQt6/)、[pytest](https://github.com/pytest-dev/pytest) 和 [coveragepy](https://github.com/nedbat/coveragepy)：
```
pip install PyQt6 pytest coverage
```

要运行带覆盖率的测试，请克隆此仓库，进入主目录并运行：
```
coverage run -m pytest
coverage report --ignore-errors -m
```

## 许可证
此软件根据 [MIT 许可证](https://github.com/niklashenning/pyqttoast/blob/master/LICENSE) 授权。
