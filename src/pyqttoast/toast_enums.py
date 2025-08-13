from enum import Enum


class ToastPreset(Enum):
    SUCCESS = 1
    WARNING = 2
    ERROR = 3
    INFORMATION = 4
    SUCCESS_DARK = 5
    WARNING_DARK = 6
    ERROR_DARK = 7
    INFORMATION_DARK = 8


class ToastIcon(Enum):
    SUCCESS = 1
    WARNING = 2
    ERROR = 3
    INFORMATION = 4
    CLOSE = 5


class ToastPosition(Enum):
    BOTTOM_LEFT = 1
    BOTTOM_MIDDLE = 2
    BOTTOM_RIGHT = 3
    TOP_LEFT = 4
    TOP_MIDDLE = 5
    TOP_RIGHT = 6
    CENTER = 7


class ToastButtonAlignment(Enum):
    TOP = 1
    MIDDLE = 2
    BOTTOM = 3


class ToastAnimationDirection(Enum):
    """Animation direction for toast show/hide animations"""
    AUTO = 0          # Automatic direction based on position (default, backward compatible)
    FROM_TOP = 1      # Slide in from top, slide out to top
    FROM_BOTTOM = 2   # Slide in from bottom, slide out to bottom
    FROM_LEFT = 3     # Slide in from left, slide out to left
    FROM_RIGHT = 4    # Slide in from right, slide out to right
    FADE_ONLY = 5     # Pure opacity animation, no position movement
