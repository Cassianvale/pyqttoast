<div align="center">

# PyQt Toast

<img src="https://socialify.git.ci/Cassianvale/pyqttoast/image?font=Source+Code+Pro&language=1&name=1&pattern=Diagonal+Stripes&theme=Auto" alt="pyqttoast" width="640" height="320" />

[![PyPI](https://img.shields.io/badge/pypi-v1.4.0-blue)](https://pypi.org/project/pyqt-toast-enhanced/)
[![Python](https://img.shields.io/badge/python-3.7+-blue)](https://github.com/Cassianvale/pyqttoast)
[![Build](https://img.shields.io/badge/build-passing-neon)](https://github.com/Cassianvale/pyqttoast)
[![Coverage](https://img.shields.io/badge/coverage-94%25-green)](https://github.com/Cassianvale/pyqttoast)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/Cassianvale/pyqttoast/blob/master/LICENSE)

**Language:** ➡️*English* | [中文](README_CN.md)

An enhanced fork of pyqt-toast-notification with additional features and improvements

> **Note**: This is an enhanced fork of the original [pyqt-toast-notification](https://github.com/niklashenning/pyqttoast) by Niklas Henning.
> All credit for the original work goes to the original author.

</div>

![pyqttoast](https://github.com/niklashenning/pyqt-toast/assets/58544929/c104f10e-08df-4665-98d8-3785822a20dc)

## ✨ Key Features
* **Modern Margin API** - Flexible and efficient margin management with multiple input formats
* **Advanced Animation Control** - Independent position and animation direction control
* **Performance Optimized** - Cached stylesheets, regex patterns, and optimized rendering
* **Multi-toast Support** - Show multiple toasts simultaneously with intelligent queueing
* **7 Position Options** - Flexible positioning including screen center
* **Multi-screen Support** - Works seamlessly across multiple monitors
* **Widget-relative Positioning** - Position toasts relative to specific widgets
* **Modern UI** - Fully customizable appearance with preset styles
* **Cross-platform** - Works with `PyQt5`, `PyQt6`, `PySide2`, and `PySide6`

## Installation

### Enhanced Version (This Fork)
Install the enhanced version with additional features:
```bash
pip install pyqt-toast-enhanced
```

### Original Version (Stable)
If you want to use the original author's stable version:
```bash
pip install pyqt-toast-notification
```

### Development Installation
For development or to get the latest features:
```bash
git clone https://github.com/Cassianvale/pyqttoast.git
cd pyqttoast
pip install -e .

1. **Clone this repository:**
```bash
git clone https://github.com/Cassianvale/pyqttoast.git
cd pyqttoast
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install in development mode:**
```bash
pip install -e .
```

4. **Or run directly without installation:**
```python
# Add project root directory to Python path
import sys
sys.path.insert(0, '/path/to/pyqttoast')
from src.pyqttoast import Toast, ToastPreset
```

> **Note:** This project includes modern margin API, performance optimizations, and other enhancements not available in the original version.

## Usage
Import the `Toast` class, instantiate it, and show the toast notification with the `show()` method:

```python
from PyQt6.QtWidgets import QMainWindow, QPushButton
from pyqttoast import Toast, ToastPreset


class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        # Add button and connect click event
        self.button = QPushButton(self)
        self.button.setText('Show toast')
        self.button.clicked.connect(self.show_toast)
    
    # Shows a toast notification every time the button is clicked
    def show_toast(self):
        toast = Toast(self)
        toast.setDuration(5000)  # Hide after 5 seconds
        toast.setTitle('Success! Confirmation email sent.')
        toast.setText('Check your email to complete signup.')
        toast.applyPreset(ToastPreset.SUCCESS)  # Apply style preset
        toast.show()
```

> **IMPORTANT:** <br>An instance of `Toast` can only be shown **once**. If you want to show another one, even if the content is exactly the same, you have to create another instance.


## Customization

* **Setting the position of the toasts (<u>static</u>):**
```python
Toast.setPosition(ToastPosition.BOTTOM_MIDDLE)  # Default: ToastPosition.BOTTOM_RIGHT
```
> **AVAILABLE POSITIONS:** <br> `BOTTOM_LEFT`, `BOTTOM_MIDDLE`, `BOTTOM_RIGHT`, `TOP_LEFT`, `TOP_MIDDLE`, `TOP_RIGHT`, `CENTER`


* **Setting whether the toasts should always be shown on the main screen (<u>static</u>):**
```python
Toast.setAlwaysOnMainScreen(True)  # Default: False
```

* **Positioning the toasts relative to a widget instead of a screen (<u>static</u>):**
```python
Toast.setPositionRelativeToWidget(some_widget)  # Default: None
```

* **Setting a limit on how many toasts can be shown at the same time (<u>static</u>):**
```python
Toast.setMaximumOnScreen(5)  # Default: 3
```
> If you try to show more toasts than the maximum amount on screen, they will get added to a queue and get shown as soon as one of the currently showing toasts is closed.


* **Setting the vertical spacing between the toasts (<u>static</u>):**
```python
Toast.setSpacing(20)  # Default: 10
```

* **Setting the x and y offset of the toast position (<u>static</u>):**
```python
Toast.setOffset(30, 55)  # Default: 20, 45
```

* **Making the toast show forever until it is closed:**
```python
toast.setDuration(0)  # Default: 5000
```

* **Enabling or disabling the duration bar:**
```python
toast.setShowDurationBar(False)  # Default: True
```

* **Adding an icon:**
```python
toast.setIcon(ToastIcon.SUCCESS)  # Default: ToastIcon.INFORMATION
toast.setShowIcon(True)           # Default: False

# Or setting a custom icon:
toast.setIcon(QPixmap('path/to/your/icon.png'))

# If you want to show the icon without recoloring it, set the icon color to None:
toast.setIconColor(None)  # Default: #5C5C5C
```
> **AVAILABLE ICONS:** <br> `SUCCESS`, `WARNING`, `ERROR`, `INFORMATION`, `CLOSE`


* **Setting the icon size:**
```python
toast.setIconSize(QSize(14, 14))  # Default: QSize(18, 18)
```

* **Enabling or disabling the icon separator:**
```python
toast.setShowIconSeparator(False)  # Default: True
```

* **Setting the close button alignment:**
```python
toast.setCloseButtonAlignment(ToastButtonAlignment.MIDDLE)  # Default: ToastButtonAlignment.TOP
```
> **AVAILABLE ALIGNMENTS:** <br> `TOP`, `MIDDLE`, `BOTTOM`

* **Enabling or disabling the close button:**
```python
toast.setShowCloseButton(False)  # Default: True
```

* **Customizing the duration of the fade animations (milliseconds):**
```python
toast.setFadeInDuration(100)   # Default: 250
toast.setFadeOutDuration(150)  # Default: 250
```

* **Controlling animation direction:**
```python
toast.setAnimationDirection(ToastAnimationDirection.FROM_LEFT)  # Default: ToastAnimationDirection.AUTO
```
> **AVAILABLE DIRECTIONS:** <br>
> `AUTO` - Direction based on toast position (backward compatible) <br>
> `FROM_TOP` - Slide in/out from top <br>
> `FROM_BOTTOM` - Slide in/out from bottom <br>
> `FROM_LEFT` - Slide in/out from left <br>
> `FROM_RIGHT` - Slide in/out from right <br>
> `FADE_ONLY` - Pure opacity animation, no position movement

* **Enabling or disabling duration reset on hover:**

```python
toast.setResetDurationOnHover(False)  # Default: True
```

* **Making the corners rounded:**
```python
toast.setBorderRadius(3)  # Default: 0
```

* **Setting custom colors:**
```python
toast.setBackgroundColor(QColor('#292929'))       # Default: #E7F4F9
toast.setTitleColor(QColor('#FFFFFF'))            # Default: #000000
toast.setTextColor(QColor('#D0D0D0'))             # Default: #5C5C5C
toast.setDurationBarColor(QColor('#3E9141'))      # Default: #5C5C5C
toast.setIconColor(QColor('#3E9141'))             # Default: #5C5C5C
toast.setIconSeparatorColor(QColor('#585858'))    # Default: #D9D9D9
toast.setCloseButtonIconColor(QColor('#C9C9C9'))  # Default: #000000
```

* **Setting custom fonts:**
```python
# Init font
font = QFont('Times', 10, QFont.Weight.Bold)

# Set fonts
toast.setTitleFont(font)  # Default: QFont('Arial', 9, QFont.Weight.Bold)
toast.setTextFont(font)   # Default: QFont('Arial', 9)
```

* **Modern margin management (NEW):**
```python
# Simple - all margins the same
toast.setMargins(20)

# Precise - left, top, right, bottom
toast.setMargins((15, 10, 15, 20))

# Symmetric - horizontal, vertical
toast.setMargins((25, 15))

# Partial update - only specific margins
toast.setMargins({'left': 30, 'right': 35})

# Different component margins
toast.setMargins(10, 'icon')           # Icon margins
toast.setMargins(5, 'text_section')   # Text section margins
toast.setMargins(8, 'close_button')   # Close button margins

# Fine-tune existing margins
toast.adjustMargins(top=8, bottom=12)
toast.adjustMargins('icon', left=5, right=10)
```
> **MARGIN TYPES:** <br> `content` (default), `icon`, `icon_section`, `text_section`, `close_button`

* **Applying a style preset:**
```python
toast.applyPreset(ToastPreset.ERROR)
```
> **AVAILABLE PRESETS:** <br> `SUCCESS`, `WARNING`, `ERROR`, `INFORMATION`, `SUCCESS_DARK`, `WARNING_DARK`, `ERROR_DARK`, `INFORMATION_DARK`

* **Setting toast size constraints:**
```python
# Minimum and maximum size
toast.setMinimumWidth(100)
toast.setMaximumWidth(350)
toast.setMinimumHeight(50)
toast.setMaximumHeight(120)

# Fixed size (not recommended)
toast.setFixedSize(QSize(350, 80))
```


**<br>Other customization options:**

| Option                        | Description                                                                     | Default                    |
|-------------------------------|---------------------------------------------------------------------------------|----------------------------|
| `setFixedScreen()`            | Fixed screen where the toasts will be shown (static)                            | `None`                     |
| `setMovePositionWithWidget()` | Whether the toasts should move with widget if positioned relative to a widget   | `True`                     |
| `setIconSeparatorWidth()`     | Width of the icon separator that separates the icon and text section            | `2`                        |
| `setCloseButtonIcon()`        | Icon of the close button                                                        | `ToastIcon.CLOSE`          |
| `setCloseButtonIconSize()`    | Size of the close button icon                                                   | `QSize(10, 10)`            |
| `setCloseButtonSize()`        | Size of the close button                                                        | `QSize(24, 24)`            |
| `setStayOnTop()`              | Whether the toast stays on top of other windows even when they are focused      | `True`                     |
| `setTextSectionSpacing()`     | Vertical spacing between the title and the text                                 | `8`                        |

## API Documentation

For complete API reference and advanced usage examples, see:
- [Toast API Reference Table (English)](docs/Toast_API_Reference_Table.md) - Detailed documentation with examples

## Demo
https://github.com/niklashenning/pyqt-toast/assets/58544929/f4d7f4a4-6d69-4087-ae19-da54b6da499d

The demos for PyQt5, PyQt6, and PySide6 can be found in the [demo](demo) folder.

## Tests
Installing the required test dependencies [PyQt6](https://pypi.org/project/PyQt6/), [pytest](https://github.com/pytest-dev/pytest), and [coveragepy](https://github.com/nedbat/coveragepy):
```
pip install PyQt6 pytest coverage
```

To run the tests with coverage, clone this repository, go into the main directory and run:
```
coverage run -m pytest
coverage report --ignore-errors -m
```

## License
This software is licensed under the [MIT license](https://github.com/niklashenning/pyqttoast/blob/master/LICENSE).
