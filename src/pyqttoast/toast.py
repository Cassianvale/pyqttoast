from __future__ import annotations

import math
import re
import webbrowser
from qtpy.QtGui import QGuiApplication, QScreen
from qtpy.QtCore import Qt, QPropertyAnimation, QPoint, QTimer, QSize, QMargins, QRect, Signal
from qtpy.QtGui import QPixmap, QIcon, QFont, QFontMetrics
from qtpy.QtWidgets import QDialog, QPushButton, QLabel, QGraphicsOpacityEffect, QWidget
from .toast_enums import ToastPreset, ToastIcon, ToastPosition, ToastButtonAlignment
from .utils import Utils
from .icon_utils import IconUtils
from .drop_shadow import DropShadow
from .constants import *


class MarginManager:
    """Modern margin manager with flexible API for Toast margin settings"""

    def __init__(self, toast_instance):
        """Initialize the margin manager

        :param toast_instance: Toast instance
        """
        self.toast = toast_instance
        self._margin_attrs = {
            'content': '_Toast__margins',
            'icon': '_Toast__icon_margins',
            'icon_section': '_Toast__icon_section_margins',
            'text_section': '_Toast__text_section_margins',
            'close_button': '_Toast__close_button_margins'
        }

    def get(self, margin_type: str = 'content') -> QMargins:
        """Get margin object for specified type

        :param margin_type: Type of margin ('content', 'icon', 'icon_section', 'text_section', 'close_button')
        :return: QMargins object
        """
        attr_name = self._margin_attrs.get(margin_type, self._margin_attrs['content'])
        return getattr(self.toast, attr_name)

    def set(self, margins, margin_type: str = 'content'):
        """Set margins with flexible input types

        :param margins: Can be QMargins, int (all sides), tuple (left,top,right,bottom), or dict
        :param margin_type: Type of margin to set
        """
        if self.toast._Toast__used:
            return

        attr_name = self._margin_attrs.get(margin_type, self._margin_attrs['content'])

        # Convert various input types to QMargins
        if isinstance(margins, QMargins):
            new_margins = margins
        elif isinstance(margins, int):
            # Single value for all sides
            new_margins = QMargins(margins, margins, margins, margins)
        elif isinstance(margins, (tuple, list)) and len(margins) == 4:
            # (left, top, right, bottom)
            new_margins = QMargins(*margins)
        elif isinstance(margins, (tuple, list)) and len(margins) == 2:
            # (horizontal, vertical)
            h, v = margins
            new_margins = QMargins(h, v, h, v)
        elif isinstance(margins, dict):
            # {'left': 10, 'top': 5, 'right': 10, 'bottom': 5}
            current = getattr(self.toast, attr_name)
            new_margins = QMargins(
                margins.get('left', current.left()),
                margins.get('top', current.top()),
                margins.get('right', current.right()),
                margins.get('bottom', current.bottom())
            )
        else:
            raise ValueError(f"Invalid margins type: {type(margins)}")

        setattr(self.toast, attr_name, new_margins)

    def adjust(self, margin_type: str = 'content', **kwargs):
        """Adjust specific sides of margins

        :param margin_type: Type of margin to adjust
        :param kwargs: left, top, right, bottom values to adjust
        """
        if self.toast._Toast__used:
            return

        current = self.get(margin_type)
        new_margins = QMargins(
            kwargs.get('left', current.left()),
            kwargs.get('top', current.top()),
            kwargs.get('right', current.right()),
            kwargs.get('bottom', current.bottom())
        )

        attr_name = self._margin_attrs[margin_type]
        setattr(self.toast, attr_name, new_margins)


class ClickableLabel(QLabel):
    """A QLabel that supports clickable links"""

    # Class-level compiled regex pattern for better performance
    _URL_PATTERN = re.compile(
        r'(?i)\b(?:'
        r'(?:https?://|www\.)'  # http://, https://, or www.
        r'(?:[^\s<>"{}|\\^`\[\]]*)'  # domain and path
        r'|'
        r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}'  # domain.tld
        r'(?:/[^\s<>"{}|\\^`\[\]]*)?'  # optional path
        r')\b'
    )

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOpenExternalLinks(True)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.linkActivated.connect(self._open_link)

    def _open_link(self, url):
        """Open the clicked link in the default browser"""
        try:
            webbrowser.open(url)
        except Exception:
            # Fallback if webbrowser fails
            pass

    def setText(self, text):
        """Set text and automatically convert URLs to clickable links"""
        # Convert plain URLs to HTML links
        linked_text = self._convert_urls_to_links(text)
        super().setText(linked_text)

    def _convert_urls_to_links(self, text):
        """Convert URLs in text to HTML links"""

        def replace_url(match):
            url = match.group(0)
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                if url.startswith('www.'):
                    full_url = 'https://' + url
                else:
                    full_url = 'https://' + url
            else:
                full_url = url

            return f'<a href="{full_url}" style="color: #0066cc; text-decoration: underline;">{url}</a>'

        # Replace URLs with HTML links using the class-level compiled pattern
        return self._URL_PATTERN.sub(replace_url, text)


class Toast(QDialog):

    # Static attributes
    __maximum_on_screen = 3
    __spacing = 10
    __offset_x = 20
    __offset_y = 50
    __position_relative_to_widget = None
    __move_position_with_widget = True
    __always_on_main_screen = False
    __fixed_screen = None
    __position = ToastPosition.BOTTOM_RIGHT

    __currently_shown = []
    __queue = []

    # CSS cache for better performance
    __css_cache = None

    # Close event
    closed = Signal()

    def __init__(self, parent: QWidget | None = None):
        """Create a new Toast instance

        :param parent: the parent widget
        """

        super(Toast, self).__init__(parent)

        # Init attributes
        self.__duration = 5000
        self.__show_duration_bar = True
        self.__title = ''
        self.__text = ''
        self.__icon = IconUtils.get_icon_from_enum(ToastIcon.INFORMATION)
        self.__show_icon = False
        self.__icon_size = QSize(18, 18)
        self.__show_icon_separator = True
        self.__icon_separator_width = 2
        self.__close_button_icon = IconUtils.get_icon_from_enum(ToastIcon.CLOSE)
        self.__show_close_button = True
        self.__close_button_icon_size = QSize(10, 10)
        self.__close_button_size = QSize(24, 24)
        self.__close_button_alignment = ToastButtonAlignment.TOP
        self.__fade_in_duration = 250
        self.__fade_out_duration = 250
        self.__reset_duration_on_hover = True
        self.__stay_on_top = True
        self.__border_radius = 0
        self.__background_color = DEFAULT_BACKGROUND_COLOR
        self.__title_color = DEFAULT_TITLE_COLOR
        self.__text_color = DEFAULT_TEXT_COLOR
        self.__icon_color = DEFAULT_ACCENT_COLOR
        self.__icon_separator_color = DEFAULT_ICON_SEPARATOR_COLOR
        self.__close_button_icon_color = DEFAULT_CLOSE_BUTTON_ICON_COLOR
        self.__duration_bar_color = DEFAULT_ACCENT_COLOR
        self.__title_font = QFont('Arial', 9, QFont.Weight.Bold)
        self.__text_font = QFont('Arial', 9)
        self.__margins = QMargins(20, 18, 10, 18)
        self.__icon_margins = QMargins(0, 0, 15, 0)
        self.__icon_section_margins = QMargins(0, 0, 15, 0)
        self.__text_section_margins = QMargins(0, 0, 15, 0)
        self.__close_button_margins = QMargins(0, -8, 0, -8)
        self.__text_section_spacing = 8
        self.__multiline = False

        # Create modern margin manager
        self.margins = MarginManager(self)

        self.__elapsed_time = 0
        self.__fading_out = False
        self.__used = False
        self.__watched_widgets = []
        self.__manual_duration_bar_value = None  # Used to track manually set progress value
        self.__widget_event_filter_installed = False  # Track event filter state
        self.__watched_widgets_event_filters_installed = False  # Track watched widgets event filter state
        self.__cached_stylesheets = {}  # Cache for generated stylesheets

        # Animation and timer references for proper cleanup
        self.__pos_animation = None
        self.__fade_in_animation = None
        self.__fade_out_animation = None

        # Window settings
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Toast widget (QLabel because QWidget has weird behaviour with stylesheets)
        self.__toast_widget = QLabel(self)

        # Drop shadow
        self.__drop_shadow = DropShadow(self)

        # Opacity effect for fading animations
        self.__opacity_effect = QGraphicsOpacityEffect()
        self.__opacity_effect.setOpacity(1)
        self.setGraphicsEffect(self.__opacity_effect)

        # Close button
        self.__close_button = QPushButton(self.__toast_widget)
        self.__close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__close_button.clicked.connect(self.hide)
        self.__close_button.setObjectName('toast-close-button')

        # Title label
        self.__title_label = QLabel(self.__toast_widget)

        # Text label (using ClickableLabel for link support)
        self.__text_label = ClickableLabel(self.__toast_widget)

        # Icon (QPushButton instead of QLabel to get better icon quality)
        self.__icon_widget = QPushButton(self.__toast_widget)
        self.__icon_widget.setObjectName('toast-icon-widget')

        # Icon separator
        self.__icon_separator = QWidget(self.__toast_widget)

        # Duration bar container (used to make border radius possible on 4 px high widget)
        self.__duration_bar_container = QWidget(self.__toast_widget)
        self.__duration_bar_container.setFixedHeight(4)
        self.__duration_bar_container.setStyleSheet('background: transparent;')

        # Duration bar
        self.__duration_bar = QWidget(self.__duration_bar_container)
        self.__duration_bar.setFixedHeight(20)
        self.__duration_bar.move(0, -16)

        # Duration bar chunk
        self.__duration_bar_chunk = QWidget(self.__duration_bar_container)
        self.__duration_bar_chunk.setFixedHeight(20)
        self.__duration_bar_chunk.move(0, -16)

        # Set defaults
        self.setIcon(self.__icon)
        self.setIconSize(self.__icon_size)
        self.setIconColor(self.__icon_color)
        self.setIconSeparatorWidth(self.__icon_separator_width)
        self.setCloseButtonIcon(self.__close_button_icon)
        self.setCloseButtonIconSize(self.__close_button_icon_size)
        self.setCloseButtonSize(self.__close_button_size)
        self.setCloseButtonAlignment(self.__close_button_alignment)
        self.setStayOnTop(self.__stay_on_top)
        self.setBackgroundColor(self.__background_color)
        self.setTitleColor(self.__title_color)
        self.setTextColor(self.__text_color)
        self.setBorderRadius(self.__border_radius)
        self.setIconSeparatorColor(self.__icon_separator_color)
        self.setCloseButtonIconColor(self.__close_button_icon_color)
        self.setDurationBarColor(self.__duration_bar_color)
        self.setTitleFont(self.__title_font)
        self.setTextFont(self.__text_font)

        # Timer for hiding the notification after set duration
        self.__duration_timer = QTimer(self)
        self.__duration_timer.setSingleShot(True)
        self.__duration_timer.timeout.connect(self.hide)

        # Timer for updating the duration bar
        self.__duration_bar_timer = QTimer(self)
        self.__duration_bar_timer.timeout.connect(self.__update_duration_bar)

        # Apply stylesheet (with caching for better performance)
        if Toast.__css_cache is None:
            import os
            css_path = os.path.join(Utils.get_current_directory(), 'css', 'toast.css')
            with open(css_path, 'r') as css_file:
                Toast.__css_cache = css_file.read()
        self.setStyleSheet(Toast.__css_cache)

        # Install event filters if position relative to widget and moving with widget
        if Toast.__position_relative_to_widget and Toast.__move_position_with_widget:
            self.__install_widget_event_filter()
            self.__install_watched_widgets_event_filters()

    def eventFilter(self, watched, event):
        # If moved or resized, update toast position if shown
        if Toast.__position_relative_to_widget and Toast.__move_position_with_widget:
            if event.type() == event.Type.Move or event.type() == event.Type.Resize:
                if watched == Toast.__position_relative_to_widget or watched in self.__watched_widgets:
                    if self in Toast.__currently_shown:
                        self.__update_position_xy(animate=False)

        # One of the parents changed or deleted
        if event.type() == event.Type.ParentChange or event.type() == event.Type.DeferredDelete:
            self.__install_watched_widgets_event_filters()

        return False

    def enterEvent(self, event):
        """Event that happens every time the mouse enters this widget.
        If reset_duration_on_hover is enabled, reset the countdown

        :param event: the event sent by PyQt
        """

        # Reset timer if hovered and resetting is enabled
        if self.__duration != 0 and self.__duration_timer.isActive() and self.__reset_duration_on_hover:
            self.__duration_timer.stop()

            # Reset duration bar if enabled
            if self.__show_duration_bar:
                self.__duration_bar_timer.stop()
                self.__duration_bar_chunk.setFixedWidth(self.width())
                self.__elapsed_time = 0

    def leaveEvent(self, event):
        """Event that happens every time the mouse leaves this widget.
        If reset_duration_on_hover is enabled, restart the countdown

        :param event: the event sent by PyQt
        """

        # Start timer again when leaving notification and reset is enabled
        if self.__duration != 0 and not self.__duration_timer.isActive() and self.__reset_duration_on_hover:
            self.__duration_timer.start(self.__duration)

            # Restart duration bar animation if enabled
            if self.__show_duration_bar:
                self.__duration_bar_timer.start(DURATION_BAR_UPDATE_INTERVAL)

    def show(self):
        """Show the toast notification"""

        # Check if already used
        if self.__used:
            return

        # If max notifications on screen not reached, show notification
        if Toast.__maximum_on_screen > len(Toast.__currently_shown):
            self.__used = True
            Toast.__currently_shown.append(self)

            # Setup UI
            self.__setup_ui()

            # Start duration timer
            if self.__duration != 0:
                self.__duration_timer.start(self.__duration)

            # Start duration bar update timer
            if self.__duration != 0 and self.__show_duration_bar:
                self.__duration_bar_timer.start(DURATION_BAR_UPDATE_INTERVAL)

            # Calculate position and show (animate position too if not first notification)
            x, y = self.__calculate_position()

            # If not first toast on screen, also do a fade down/up animation
            if len(Toast.__currently_shown) > 1:
                # Calculate offset if predecessor toast is still in fade down / up animation
                predecessor_toast = Toast.__currently_shown[Toast.__currently_shown.index(self) - 1]
                predecessor_target_x, predecessor_target_y = predecessor_toast.__calculate_position()
                predecessor_target_difference_y = abs(predecessor_toast.y() - predecessor_target_y)

                # Calculate start position of fade down / up animation based on position
                if (Toast.__position == ToastPosition.BOTTOM_RIGHT
                        or Toast.__position == ToastPosition.BOTTOM_LEFT
                        or Toast.__position == ToastPosition.BOTTOM_MIDDLE):
                    self.move(x, y - int(self.height() / 1.5) - predecessor_target_difference_y)

                elif (Toast.__position == ToastPosition.TOP_RIGHT
                      or Toast.__position == ToastPosition.TOP_LEFT
                      or Toast.__position == ToastPosition.TOP_MIDDLE
                      or Toast.__position == ToastPosition.CENTER):
                    self.move(x, y + int(self.height() / 1.5) + predecessor_target_difference_y)

                # Start fade down / up animation
                self.__cleanup_animation('pos')
                self.__pos_animation = QPropertyAnimation(self, b"pos")
                self.__pos_animation.setEndValue(QPoint(x, y))
                self.__pos_animation.setDuration(self.__fade_in_duration)
                self.__pos_animation.start()
            else:
                self.move(x, y)

            # Fade in
            super().show()
            self.__cleanup_animation('fade_in')
            self.__fade_in_animation = QPropertyAnimation(self.__opacity_effect, b"opacity")
            self.__fade_in_animation.setDuration(self.__fade_in_duration)
            self.__fade_in_animation.setStartValue(0)
            self.__fade_in_animation.setEndValue(1)
            self.__fade_in_animation.start()

            # Update every other currently shown notification
            for toast in Toast.__currently_shown:
                toast.__update_position_xy()
        else:
            # Add notification to queue instead
            Toast.__queue.append(self)

    def hide(self):
        """Start hiding process of the toast notification"""

        self.__used = True

        if not self.__fading_out:
            self.__fading_out = True
            if self.__duration != 0:
                self.__duration_timer.stop()
            self.__fade_out()

    def __cleanup_animation(self, animation_type):
        """Clean up existing animation to prevent memory leaks"""
        if animation_type == 'pos' and self.__pos_animation:
            self.__pos_animation.stop()
            self.__pos_animation.deleteLater()
            self.__pos_animation = None
        elif animation_type == 'fade_in' and self.__fade_in_animation:
            self.__fade_in_animation.stop()
            self.__fade_in_animation.deleteLater()
            self.__fade_in_animation = None
        elif animation_type == 'fade_out' and self.__fade_out_animation:
            self.__fade_out_animation.stop()
            self.__fade_out_animation.deleteLater()
            self.__fade_out_animation = None

    def __fade_out(self):
        """Start the fade out animation"""

        self.__cleanup_animation('fade_out')
        self.__fade_out_animation = QPropertyAnimation(self.__opacity_effect, b"opacity")
        self.__fade_out_animation.setDuration(self.__fade_out_duration)
        self.__fade_out_animation.setStartValue(1)
        self.__fade_out_animation.setEndValue(0)
        self.__fade_out_animation.finished.connect(self.__hide)
        self.__fade_out_animation.start()

    def __cleanup_resources(self):
        """Clean up all resources to prevent memory leaks"""
        # Clean up animations
        self.__cleanup_animation('pos')
        self.__cleanup_animation('fade_in')
        self.__cleanup_animation('fade_out')

        # Stop timers
        if self.__duration_timer.isActive():
            self.__duration_timer.stop()
        if self.__duration_bar_timer.isActive():
            self.__duration_bar_timer.stop()

        # Remove event filters
        self.__remove_widget_event_filter()
        self.__remove_watched_widgets_event_filters()

    def __hide(self):
        """Hide the toast notification"""

        self.__cleanup_resources()
        self.close()

        if self in Toast.__currently_shown:
            Toast.__currently_shown.remove(self)
            self.__elapsed_time = 0
            self.__fading_out = False

            # Update every other currently shown notification
            for toast in Toast.__currently_shown:
                toast.__update_position_y()

            # Show next item from queue after updating
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(Toast.__show_next_in_queue)
            timer.start(self.__fade_in_duration)

            # Emit signal
            self.closed.emit()

    def __update_duration_bar(self):
        """Update the duration bar chunk with the elapsed time"""

        # Clear manually set progress value
        self.__manual_duration_bar_value = None

        self.__elapsed_time += DURATION_BAR_UPDATE_INTERVAL

        if self.__elapsed_time >= self.__duration:
            self.__duration_bar_timer.stop()
            return

        new_chunk_width = math.floor(
            self.__duration_bar_container.width()
            - self.__elapsed_time / self.__duration * self.__duration_bar_container.width()
        )
        self.__duration_bar_chunk.setFixedWidth(new_chunk_width)

    def __set_duration_bar(self, fraction):
        """Set the width of the duration bar chunk with the specified fraction"""

        if self.__duration_bar_timer.isActive():
            self.__duration_bar_timer.stop()

        # Save manually set progress value
        self.__manual_duration_bar_value = fraction

        new_chunk_width = math.floor(fraction * self.__duration_bar_container.width())
        self.__duration_bar_chunk.setFixedWidth(new_chunk_width)

    def __update_position_xy(self, animate: bool = True):
        """Update the x and y position of the toast with an optional animation

        :param animate: whether the position change should be animated
        """

        x, y = self.__calculate_position()
        position = QPoint(x, y)

        # Animate position change
        self.__cleanup_animation('pos')
        self.__pos_animation = QPropertyAnimation(self, b"pos")
        self.__pos_animation.setEndValue(position)
        self.__pos_animation.setDuration(UPDATE_POSITION_DURATION if animate else 0)
        self.__pos_animation.start()

    def __update_position_x(self, animate: bool = True):
        """Update the x position of the toast with an optional animation

        :param animate: whether the position change should be animated
        """

        x, y = self.__calculate_position()
        position = QPoint(x, self.y())

        # Animate position change
        self.__cleanup_animation('pos')
        self.__pos_animation = QPropertyAnimation(self, b"pos")
        self.__pos_animation.setEndValue(position)
        self.__pos_animation.setDuration(UPDATE_POSITION_DURATION if animate else 0)
        self.__pos_animation.start()

    def __update_position_y(self, animate: bool = True):
        """Update the y position of the toast with an optional animation

        :param animate: whether the position change should be animated
        """

        x, y = self.__calculate_position()
        position = QPoint(self.x(), y)

        # Animate position change
        self.__cleanup_animation('pos')
        self.__pos_animation = QPropertyAnimation(self, b"pos")
        self.__pos_animation.setEndValue(position)
        self.__pos_animation.setDuration(UPDATE_POSITION_DURATION if animate else 0)
        self.__pos_animation.start()

    def __get_bounds(self) -> QRect:
        """Get the bounds (QRect) of the target screen or widget

        :return: rect of the target screen or widget
        """

        # Get primary screen
        primary_screen = QGuiApplication.primaryScreen()
        current_screen = None

        # Calculate target screen / widget
        if Toast.__position_relative_to_widget is not None:
            top_level_parent = Utils.get_top_level_parent(Toast.__position_relative_to_widget)
            if top_level_parent == Toast.__position_relative_to_widget:
                return Toast.__position_relative_to_widget.geometry()

            global_pos = top_level_parent.mapToGlobal(Toast.__position_relative_to_widget.pos())
            return QRect(
                global_pos.x(), global_pos.y(), Toast.__position_relative_to_widget.width(),
                Toast.__position_relative_to_widget.height()
            )
        elif Toast.__fixed_screen is not None:
            current_screen = Toast.__fixed_screen
        elif Toast.__always_on_main_screen or self.parent() is None:
            current_screen = primary_screen
        else:
            screens = QGuiApplication.screens()
            for screen in screens:
                if self.parent().geometry().intersects(screen.geometry()):
                    if current_screen is None:
                        current_screen = screen
                    else:
                        current_screen = primary_screen
                        break

        return current_screen.geometry()

    def __calculate_position(self):
        """Calculate x and y position of the toast

        :return: x and y position
        """

        # Calculate vertical space taken up by all the currently showing notifications
        y_offset = 0
        for toast in Toast.__currently_shown:
            if toast == self:
                break
            y_offset += toast.__toast_widget.height() + Toast.__spacing

        # Calculate x and y position of notification
        x = 0
        y = 0
        bounds = self.__get_bounds()

        if Toast.__position == ToastPosition.BOTTOM_RIGHT:
            x = (bounds.width() - self.__toast_widget.width()
                 - Toast.__offset_x + bounds.x())
            y = (bounds.height() - self.__toast_widget.height()
                 - Toast.__offset_y + bounds.y() - y_offset)

        elif Toast.__position == ToastPosition.BOTTOM_LEFT:
            x = bounds.x() + Toast.__offset_x
            y = (bounds.height() - self.__toast_widget.height()
                 - Toast.__offset_y + bounds.y() - y_offset)

        elif Toast.__position == ToastPosition.BOTTOM_MIDDLE:
            x = (bounds.x() + bounds.width() / 2 - self.__toast_widget.width() / 2)
            y = (bounds.height() - self.__toast_widget.height()
                 - Toast.__offset_y + bounds.y() - y_offset)

        elif Toast.__position == ToastPosition.TOP_RIGHT:
            x = (bounds.width() - self.__toast_widget.width()
                 - Toast.__offset_x + bounds.x())
            y = (bounds.y() + Toast.__offset_y + y_offset)

        elif Toast.__position == ToastPosition.TOP_LEFT:
            x = bounds.x() + Toast.__offset_x
            y = (bounds.y() + Toast.__offset_y + y_offset)

        elif Toast.__position == ToastPosition.TOP_MIDDLE:
            x = (bounds.x() + bounds.width() / 2 - self.__toast_widget.width() / 2)
            y = (bounds.y() + Toast.__offset_y + y_offset)

        elif Toast.__position == ToastPosition.CENTER:
            x = (bounds.x() + bounds.width() / 2 - self.__toast_widget.width() / 2)
            if y_offset == 0:
                y = (bounds.y() + bounds.height() / 2
                     - self.__toast_widget.height() / 2 + y_offset)
            else:
                y_start = (bounds.y() + bounds.height() / 2
                           - self.__currently_shown[0].__toast_widget.height() / 2)
                y = y_start + y_offset

        x = int(x - DROP_SHADOW_SIZE)
        y = int(y - DROP_SHADOW_SIZE)

        return x, y

    def __setup_ui(self):
        """Calculate best toast size and place and move everything correctly"""

        # Update stylesheet
        self.__update_stylesheet()

        # Cache font metrics to avoid repeated creation
        title_font_metrics = QFontMetrics(self.__title_font)
        text_font_metrics = QFontMetrics(self.__text_font)

        # Cache text content to avoid repeated method calls
        title_text = self.__title_label.text()
        text_text = self.__text_label.text()

        # Calculate title and text width and height
        title_width = title_font_metrics.width(title_text) if title_text else 0
        title_height = title_font_metrics.boundingRect(title_text).height() if title_text else 0
        text_width = text_font_metrics.width(text_text) if text_text else 0
        text_height = text_font_metrics.boundingRect(text_text).height() if text_text else 0

        text_section_spacing = self.__text_section_spacing if (self.__title and self.__text) else 0

        if self.__multiline:
            self.__title_label.setWordWrap(True)
            self.__text_label.setWordWrap(True)
            if self.__title:
                title_size_hint = self.__title_label.sizeHint()
                title_height = title_size_hint.height()
                title_width = title_size_hint.width()
            if self.__text:
                text_size_hint = self.__text_label.sizeHint()
                text_height = text_size_hint.height()
                text_width = text_size_hint.width()
        else:
            self.__title_label.setWordWrap(False)
            self.__text_label.setWordWrap(False)

        # Helper function to calculate text section height
        def calculate_text_section_height():
            return (self.__text_section_margins.top() + title_height +
                   text_section_spacing + text_height + self.__text_section_margins.bottom())

        text_section_height = calculate_text_section_height()

        # Calculate duration bar height
        duration_bar_height = self.__duration_bar_container.height() if self.__show_duration_bar else 0

        # Calculate icon section dimensions
        if self.__show_icon:
            icon_section_width = (self.__icon_section_margins.left() + self.__icon_margins.left() +
                                 self.__icon_widget.width() + self.__icon_margins.right() +
                                 self.__icon_separator.width() + self.__icon_section_margins.right())
            icon_section_height = (self.__icon_section_margins.top() + self.__icon_margins.top() +
                                  self.__icon_widget.height() + self.__icon_margins.bottom() +
                                  self.__icon_section_margins.bottom())
        else:
            icon_section_width = 0
            icon_section_height = 0

        # Calculate close button section dimensions
        if self.__show_close_button:
            close_button_width = self.__close_button.width()
            close_button_height = self.__close_button.height()
            close_button_margins = self.__close_button_margins
            close_button_section_height = (close_button_margins.top() + close_button_height +
                                         close_button_margins.bottom())
        else:
            close_button_width = 0
            close_button_height = 0
            close_button_margins = QMargins(0, 0, 0, 0)
            close_button_section_height = 0

        # Calculate needed width and height
        width = (self.__margins.left() + icon_section_width + self.__text_section_margins.left()
                 + max(title_width, text_width) + self.__text_section_margins.right()
                 + close_button_margins.left() + close_button_width
                 + close_button_margins.right() + self.__margins.right())

        height = (self.__margins.top()
                  + max(icon_section_height, text_section_height, close_button_section_height)
                  + self.__margins.bottom() + duration_bar_height)

        forced_additional_height = 0
        forced_reduced_height = 0

        # Handle width greater than maximum width
        if width > self.maximumWidth():
            # Enable line break for title and text and recalculate size
            new_title_text_width = max(title_width, text_width) - (width - self.maximumWidth())
            if new_title_text_width > 0:
                title_width = new_title_text_width
                text_width = new_title_text_width

            self.__title_label.setMinimumWidth(title_width)
            self.__title_label.setWordWrap(True)
            if self.__title != '':
                title_height = self.__title_label.sizeHint().height()
            self.__title_label.setFixedSize(title_width, title_height)

            self.__text_label.setMinimumWidth(text_width)
            self.__text_label.setWordWrap(True)
            if self.__text != '':
                text_height = self.__text_label.sizeHint().height()
            self.__text_label.setFixedSize(text_width, text_height)

            # Recalculate width and height
            width = self.maximumWidth()

            text_section_height = (self.__text_section_margins.top()
                                   + title_height + text_section_spacing
                                   + text_height + self.__text_section_margins.bottom())

            height = (self.__margins.top()
                      + max(icon_section_height, text_section_height, close_button_section_height)
                      + self.__margins.bottom() + duration_bar_height)

        # Handle height less than minimum height
        if height < self.minimumHeight():
            # Enable word wrap for title and text labels
            self.__title_label.setWordWrap(True)
            self.__text_label.setWordWrap(True)

            # Calculate height with initial label width
            title_width = (self.__title_label.fontMetrics().boundingRect(
                QRect(0, 0, 0, 0), Qt.TextFlag.TextWordWrap, self.__title_label.text()).width())
            text_width = (self.__text_label.fontMetrics().boundingRect(
                QRect(0, 0, 0, 0), Qt.TextFlag.TextWordWrap, self.__text_label.text()).width())
            temp_width = max(title_width, text_width)

            title_width = (self.__title_label.fontMetrics().boundingRect(
                QRect(0, 0, temp_width, 0), Qt.TextFlag.TextWordWrap, self.__title_label.text()).width())
            if self.__title != '':
                title_height = (self.__title_label.fontMetrics().boundingRect(
                    QRect(0, 0, temp_width, 0), Qt.TextFlag.TextWordWrap, self.__title_label.text()).height())

            text_width = (self.__text_label.fontMetrics().boundingRect(
                QRect(0, 0, temp_width, 0), Qt.TextFlag.TextWordWrap, self.__text_label.text()).width())
            if self.__text != '':
                text_height = (self.__text_label.fontMetrics().boundingRect(
                    QRect(0, 0, temp_width, 0), Qt.TextFlag.TextWordWrap, self.__text_label.text()).height())

            text_section_height = (self.__text_section_margins.top()
                                   + title_height + text_section_spacing
                                   + text_height + self.__text_section_margins.bottom())

            height = (self.__margins.top()
                      + max(icon_section_height, text_section_height, close_button_section_height)
                      + self.__margins.bottom() + duration_bar_height)

            while temp_width <= width:
                # Recalculate height with different text widths to find optimal value
                temp_title_width = (self.__title_label.fontMetrics().boundingRect(
                    QRect(0, 0, temp_width, 0), Qt.TextFlag.TextWordWrap, self.__title_label.text()).width())
                temp_title_height = (self.__title_label.fontMetrics().boundingRect(
                    QRect(0, 0, temp_width, 0), Qt.TextFlag.TextWordWrap, self.__title_label.text()).height())
                temp_text_width = (self.__text_label.fontMetrics().boundingRect(
                    QRect(0, 0, temp_width, 0), Qt.TextFlag.TextWordWrap, self.__text_label.text()).width())
                temp_text_height = (self.__text_label.fontMetrics().boundingRect(
                    QRect(0, 0, temp_width, 0), Qt.TextFlag.TextWordWrap, self.__text_label.text()).height())

                if self.__title == '':
                    temp_title_height = 0

                if self.__text == '':
                    temp_text_height = 0

                temp_text_section_height = (self.__text_section_margins.top()
                                            + temp_title_height + text_section_spacing
                                            + temp_text_height + self.__text_section_margins.bottom())

                temp_height = (self.__margins.top()
                               + max(icon_section_height, temp_text_section_height,
                                     close_button_section_height)
                               + self.__margins.bottom() + duration_bar_height)

                # Store values if calculated height is greater than or equal to min height
                if temp_height >= self.minimumHeight():
                    title_width = temp_title_width
                    title_height = temp_title_height
                    text_width = temp_text_width
                    text_height = temp_text_height
                    text_section_height = temp_text_section_height
                    height = temp_height
                    temp_width += 1

                # Exit loop if calculated height is less than min height
                else:
                    break

            # Recalculate width
            width = (self.__margins.left() + icon_section_width + self.__text_section_margins.left()
                     + max(title_width, text_width) + self.__text_section_margins.right()
                     + close_button_margins.left() + close_button_width
                     + close_button_margins.right() + self.__margins.right())

            # If min height not met, set height to min height
            if height < self.minimumHeight():
                forced_additional_height = self.minimumHeight() - height
                height = self.minimumHeight()

        # Handle width less than minimum width
        if width < self.minimumWidth():
            width = self.minimumWidth()

        # Handle height greater than maximum height
        if height > self.maximumHeight():
            forced_reduced_height = height - self.maximumHeight()
            height = self.maximumHeight()

        # Calculate width and height including space for drop shadow
        total_width = width + (DROP_SHADOW_SIZE * 2)
        total_height = height + (DROP_SHADOW_SIZE * 2)

        # Resize drop shadow
        self.__drop_shadow.resize(QSize(total_width, total_height))

        # Resize window
        super().setFixedSize(total_width, total_height)
        self.__toast_widget.setFixedSize(width, height)
        self.__toast_widget.move(DROP_SHADOW_SIZE, DROP_SHADOW_SIZE)
        self.__toast_widget.raise_()

        # Calculate max height of all sections
        max_section_height = max(icon_section_height, text_section_height, close_button_section_height)

        # Calculate difference between height and height of icon section and text section
        height_icon_section_height_difference = max_section_height - icon_section_height
        height_text_section_height_difference = max_section_height - text_section_height

        if self.__show_icon:
            # Move icon
            self.__icon_widget.move(self.__margins.left()
                                    + self.__icon_section_margins.left()
                                    + self.__icon_margins.left(),
                                    self.__margins.top()
                                    + self.__icon_section_margins.top()
                                    + self.__icon_margins.top()
                                    + math.ceil(height_icon_section_height_difference / 2)
                                    + math.ceil(forced_additional_height / 2)
                                    - math.floor(forced_reduced_height / 2))

            # Move and resize icon separator
            self.__icon_separator.setFixedHeight(text_section_height)
            self.__icon_separator.move(self.__margins.left()
                                       + self.__icon_section_margins.left()
                                       + self.__icon_margins.left()
                                       + self.__icon_widget.width()
                                       + self.__icon_margins.right(),
                                       self.__margins.top()
                                       + self.__icon_section_margins.top()
                                       + math.ceil(height_text_section_height_difference / 2)
                                       + math.ceil(forced_additional_height / 2)
                                       - math.floor(forced_reduced_height / 2))
        else:
            # Hide icon section
            self.__icon_widget.setVisible(False)
            self.__icon_separator.setVisible(False)

        # Resize title and text labels
        self.__title_label.setFixedSize(max(title_width, text_width), title_height)
        self.__text_label.setFixedSize(max(title_width, text_width), text_height)

        # Move title and text labels
        if self.__show_icon:
            self.__title_label.move(self.__margins.left()
                                    + self.__icon_section_margins.left()
                                    + self.__icon_margins.left()
                                    + self.__icon_widget.width()
                                    + self.__icon_margins.right()
                                    + self.__icon_separator.width()
                                    + self.__icon_section_margins.right()
                                    + self.__text_section_margins.left(),
                                    self.__margins.top()
                                    + self.__text_section_margins.top()
                                    + math.ceil(height_text_section_height_difference / 2)
                                    + math.ceil(forced_additional_height / 2)
                                    - math.floor(forced_reduced_height / 2))

            self.__text_label.move(self.__margins.left()
                                   + self.__icon_section_margins.left()
                                   + self.__icon_margins.left()
                                   + self.__icon_widget.width()
                                   + self.__icon_margins.right()
                                   + self.__icon_separator.width()
                                   + self.__icon_section_margins.right()
                                   + self.__text_section_margins.left(),
                                   self.__margins.top()
                                   + self.__text_section_margins.top()
                                   + title_height + self.__text_section_spacing
                                   + math.ceil(height_text_section_height_difference / 2)
                                   + math.ceil(forced_additional_height / 2)
                                   - math.floor(forced_reduced_height / 2))

        # Position is different if icon hidden
        else:
            self.__title_label.move(self.__margins.left()
                                    + self.__text_section_margins.left(),
                                    self.__margins.top()
                                    + self.__text_section_margins.top()
                                    + math.ceil(height_text_section_height_difference / 2)
                                    + math.ceil(forced_additional_height / 2)
                                    - math.floor(forced_reduced_height / 2))

            self.__text_label.move(self.__margins.left()
                                   + self.__text_section_margins.left(),
                                   self.__margins.top()
                                   + self.__text_section_margins.top()
                                   + title_height + self.__text_section_spacing
                                   + math.ceil(height_text_section_height_difference / 2)
                                   + math.ceil(forced_additional_height / 2)
                                   - math.floor(forced_reduced_height / 2))

        # Adjust label position if either title or text is empty
        if self.__title == '' and self.__text != '':
            self.__text_label.move(self.__text_label.x(),
                                   int((height - text_height - duration_bar_height) / 2))

        elif self.__title != '' and self.__text == '':
            self.__title_label.move(self.__title_label.x(),
                                    int((height - title_height - duration_bar_height) / 2))

        # Move close button to top, middle, or bottom position
        if self.__close_button_alignment == ToastButtonAlignment.TOP:
            self.__close_button.move(width - close_button_width
                                     - close_button_margins.right() - self.__margins.right(),
                                     self.__margins.top() + close_button_margins.top())
        elif self.__close_button_alignment == ToastButtonAlignment.MIDDLE:
            self.__close_button.move(width - close_button_width
                                     - close_button_margins.right() - self.__margins.right(),
                                     math.ceil((height - close_button_height
                                               - duration_bar_height) / 2))
        elif self.__close_button_alignment == ToastButtonAlignment.BOTTOM:
            self.__close_button.move(width - close_button_width
                                     - close_button_margins.right() - self.__margins.right(),
                                     height - close_button_height
                                     - self.__margins.bottom()
                                     - close_button_margins.bottom() - duration_bar_height)

        # Hide close button if disabled
        if not self.__show_close_button:
            self.__close_button.setVisible(False)

        # Resize, move, and show duration bar if enabled
        if self.__show_duration_bar:
            self.__duration_bar_container.setFixedWidth(width)
            self.__duration_bar_container.move(0, height - duration_bar_height)
            self.__duration_bar.setFixedWidth(width)

            # Set the width of the duration bar chunk
            if self.__manual_duration_bar_value is not None:
                # If there's a manually set progress value, use it
                chunk_width = math.floor(self.__manual_duration_bar_value * width)
                self.__duration_bar_chunk.setFixedWidth(chunk_width)
            else:
                # Otherwise set to full width (default behavior)
                self.__duration_bar_chunk.setFixedWidth(width)

            self.__duration_bar_container.setVisible(True)
        else:
            self.__duration_bar_container.setVisible(False)

    def __install_widget_event_filter(self):
        """Install an event filter on parent"""

        if Toast.__position_relative_to_widget and not self.__widget_event_filter_installed:
            Toast.__position_relative_to_widget.installEventFilter(self)
            self.__widget_event_filter_installed = True

    def __remove_widget_event_filter(self):
        """Remove an installed event filter on parent"""

        if Toast.__position_relative_to_widget and self.__widget_event_filter_installed:
            Toast.__position_relative_to_widget.removeEventFilter(self)
            self.__widget_event_filter_installed = False

    def __remove_watched_widgets_event_filters(self):
        """Remove installed event filters on watched widgets"""

        if self.__watched_widgets_event_filters_installed:
            for widget in self.__watched_widgets:
                widget.removeEventFilter(self)
            self.__watched_widgets.clear()
            self.__watched_widgets_event_filters_installed = False

    def __install_watched_widgets_event_filters(self):
        """Install / reinstall event filters on watched widgets"""

        # Only remove if already installed
        if self.__watched_widgets_event_filters_installed:
            self.__remove_watched_widgets_event_filters()

        if Toast.__position_relative_to_widget is None:
            return

        self.__watched_widgets = Utils.get_parents(Toast.__position_relative_to_widget)
        for widget in self.__watched_widgets:
            widget.installEventFilter(self)
        self.__watched_widgets_event_filters_installed = True

    def setFixedSize(self, size: QSize):
        """Set a fixed toast size

        :param size: fixed size
        """

        self.setMinimumSize(size)
        self.setMaximumSize(size)

    def setFixedWidth(self, width: int):
        """Set a fixed toast width

        :param width: fixed width
        """

        self.setMinimumWidth(width)
        self.setMaximumWidth(width)

    def setFixedHeight(self, height: int):
        """Set a fixed toast height

        :param height: fixed height
        """

        self.setMinimumHeight(height)
        self.setMaximumHeight(height)

    def getDuration(self) -> int:
        """Get the duration of the toast

        :return: duration in milliseconds
        """

        return self.__duration

    def setDuration(self, duration: int):
        """Set the duration of the toast

        :param duration: duration in milliseconds
        """

        if self.__used:
            return
        if duration < 0:
            raise ValueError("Duration must be non-negative")
        self.__duration = duration

    def isShowDurationBar(self) -> bool:
        """Get whether the duration bar is enabled

        :return: whether the duration bar is enabled
        """

        return self.__show_duration_bar

    def setShowDurationBar(self, on: bool):
        """Set whether the duration bar should be shown

        :param on: whether the duration bar should be shown
        """

        if self.__used:
            return
        self.__show_duration_bar = on

    def getTitle(self) -> str:
        """Get the title of the toast

        :return: title
        """

        return self.__title

    def setTitle(self, title: str):
        """Set the title of the toast

        :param title: new title
        """

        if self.__used:
            return
        self.__title = title
        self.__title_label.setText(title)

    def getText(self) -> str:
        """Get the text of the toast

        :return: text
        """

        return self.__text

    def setText(self, text: str):
        """Set the text of the toast

        :param text: new text
        """

        if self.__used:
            return
        self.__text = text
        self.__text_label.setText(text)

    def getIcon(self) -> QPixmap:
        """Get the icon of the toast

        :return: icon
        """

        return self.__icon

    def setIcon(self, icon: QPixmap | ToastIcon):
        """Set the icon of the toast

        :param icon: new icon
        """

        if self.__used:
            return

        if isinstance(icon, ToastIcon):
            self.__icon = IconUtils.get_icon_from_enum(icon)
        else:
            self.__icon = icon

        self.__icon_widget.setIcon(QIcon(self.__icon))
        self.setIconColor(self.__icon_color)

    def isShowIcon(self) -> bool:
        """Get whether the icon is enabled

        :return: whether the icon is enabled
        """

        return self.__show_icon

    def setShowIcon(self, on: bool):
        """Set whether the icon should be shown

        :param on: whether the icon should be shown
        """

        if self.__used:
            return
        self.__show_icon = on

    def getIconSize(self) -> QSize:
        """Get the size of the icon

        :return: size
        """

        return self.__icon_size

    def setIconSize(self, size: QSize):
        """Set the size of the icon

        :param size: new size
        """

        if self.__used:
            return
        self.__icon_size = size
        self.__icon_widget.setFixedSize(size)
        self.__icon_widget.setIconSize(size)
        self.setIcon(self.__icon)

    def isShowIconSeparator(self) -> bool:
        """Get whether the icon separator is enabled

        :return: whether the icon separator is enabled
        """

        return self.__show_icon_separator

    def setShowIconSeparator(self, on: bool):
        """Set whether the icon separator should be shown

        :param on: whether the icon separator should be shown
        """

        if self.__used:
            return
        self.__show_icon_separator = on

        if on:
            self.__icon_separator.setFixedWidth(self.__icon_separator_width)
        else:
            self.__icon_separator.setFixedWidth(0)

    def getIconSeparatorWidth(self) -> int:
        """Get the width of the icon separator

        :return: width
        """

        return self.__icon_separator_width

    def setIconSeparatorWidth(self, width: int):
        """Set the width of the icon separator

        :param width: new width
        """

        if self.__used:
            return
        self.__icon_separator_width = width

        if self.__show_icon_separator:
            self.__icon_separator.setFixedWidth(width)

    def getCloseButtonIcon(self) -> QPixmap:
        """Get the icon of the close button

        :return: icon
        """

        return self.__close_button_icon

    def setCloseButtonIcon(self, icon: QPixmap | ToastIcon):
        """Set the icon of the close button

        :param icon: new icon
        """

        if self.__used:
            return

        if type(icon) == ToastIcon:
            self.__close_button_icon = IconUtils.get_icon_from_enum(icon)
        else:
            self.__close_button_icon = icon

        self.__close_button.setIcon(QIcon(self.__close_button_icon))
        self.setCloseButtonIconColor(self.__close_button_icon_color)

    def isShowCloseButton(self) -> bool:
        """Get whether the close button is enabled

        :return: whether the close button is enabled
        """

        return self.__show_close_button

    def setShowCloseButton(self, show: bool):
        """Set whether the close button should be shown

        :param show: whether the close button should be shown
        """

        if self.__used:
            return
        self.__show_close_button = show

    def getCloseButtonIconSize(self) -> QSize:
        """Get the size of the close button icon

        :return: size
        """

        return self.__close_button_icon_size

    def setCloseButtonIconSize(self, size: QSize):
        """Get the size of the close button icon

        :param size: new size
        """

        if self.__used:
            return
        self.__close_button_icon_size = size
        self.__close_button.setIconSize(size)
        self.setCloseButtonIcon(self.__close_button_icon)

    def getCloseButtonSize(self) -> QSize:
        """Get the size of the close button

        :return: size
        """

        return self.__close_button_size

    def setCloseButtonSize(self, size: QSize):
        """Set the size of the close button

        :param size: new size
        """

        if self.__used:
            return
        self.__close_button_size = size
        self.__close_button.setFixedSize(size)

    def getCloseButtonWidth(self) -> int:
        """Get the width of the close button

        :return: width
        """

        return self.__close_button_size.width()

    def setCloseButtonWidth(self, width: int):
        """Set the width of the close button

        :param width: new width
        """

        if self.__used:
            return
        self.__close_button_size.setWidth(width)
        self.__close_button.setFixedSize(self.__close_button_size)

    def getCloseButtonHeight(self) -> int:
        """Get the height of the close button

        :return: height
        """

        return self.__close_button_size.height()

    def setCloseButtonHeight(self, height: int):
        """Set the height of the close button

        :param height: new height
        """

        if self.__used:
            return
        self.__close_button_size.setHeight(height)
        self.__close_button.setFixedSize(self.__close_button_size)

    def getCloseButtonAlignment(self) -> ToastButtonAlignment:
        """Get the alignment of the close button

        :return: alignment
        """

        return self.__close_button_alignment

    def setCloseButtonAlignment(self, alignment: ToastButtonAlignment):
        """Set the alignment of the close button

        :param alignment: new alignment
        """

        if self.__used:
            return
        self.__close_button_alignment = alignment

    def getFadeInDuration(self) -> int:
        """Get the fade in duration of the toast

        :return: fade in duration in milliseconds
        """

        return self.__fade_in_duration

    def setFadeInDuration(self, duration: int):
        """Set the fade in duration of the toast

        :param duration: new fade in duration in milliseconds
        """

        if self.__used:
            return
        self.__fade_in_duration = duration

    def getFadeOutDuration(self) -> int:
        """Get the fade out duration of the toast

        :return: fade out duration in milliseconds
        """

        return self.__fade_out_duration

    def setFadeOutDuration(self, duration: int):
        """Set the fade out duration of the toast

        :param duration: new fade out duration in milliseconds
        """

        if self.__used:
            return
        self.__fade_out_duration = duration

    def isResetDurationOnHover(self) -> bool:
        """Get whether the duration resets on hover

        :return: whether the duration resets on hover
        """

        return self.__reset_duration_on_hover

    def setResetDurationOnHover(self, on: bool):
        """Set whether the duration should reset on hover

        :param on: whether the duration should reset on hover
        """

        if self.__used:
            return
        self.__reset_duration_on_hover = on

    def isStayOnTop(self) -> bool:
        """Get whether the toast always stays on top of other windows

        :return: whether the stay on top option is enabled
        """

        return self.__stay_on_top

    def setStayOnTop(self, on: bool):
        """Set whether the toast should always stay on top of other windows

        :param on: whether the stay on top option should be enabled
        """

        if self.__used:
            return
        self.__stay_on_top = on

        if on:
            self.setWindowFlags(Qt.WindowType.ToolTip |
                                Qt.WindowType.CustomizeWindowHint |
                                Qt.WindowType.FramelessWindowHint |
                                Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.WindowType.ToolTip |
                                Qt.WindowType.CustomizeWindowHint |
                                Qt.WindowType.FramelessWindowHint)

    def getBorderRadius(self) -> int:
        """Get the border radius of the toast

        :return: border radius
        """

        return self.__border_radius

    def setBorderRadius(self, border_radius: int):
        """Set the border radius of the toast

        :param border_radius: new border radius
        """

        if self.__used:
            return
        self.__border_radius = border_radius

    def getBackgroundColor(self) -> QColor:
        """Get the background color of the toast

        :return: background color
        """

        return self.__background_color

    def setBackgroundColor(self, color: QColor):
        """Set the background color of the toast

        :param color: new background color
        """

        if self.__used:
            return
        self.__background_color = color

    def getTitleColor(self) -> QColor:
        """Get the color of the title

        :return: title color
        """

        return self.__title_color

    def setTitleColor(self, color: QColor):
        """Set the color of the title

        :param color: new title color
        """

        if self.__used:
            return
        self.__title_color = color

    def getTextColor(self) -> QColor:
        """Get the color of the text

        :return: text color
        """

        return self.__text_color

    def setTextColor(self, color: QColor):
        """Set the color of the text

        :param color: new text color
        """

        if self.__used:
            return
        self.__text_color = color

    def getIconColor(self) -> QColor | None:
        """Get the color of the icon

        :return: icon color (None if no color is set)
        """

        return self.__icon_color

    def setIconColor(self, color: QColor | None):
        """Set the color of the icon

        :param color: new icon color (None if the icon should not be recolored)
        """

        if self.__used:
            return

        self.__icon_color = color
        recolored_image = IconUtils.recolor_image(QIcon(self.__icon).pixmap(
                                                  self.__icon_widget.iconSize()).toImage(), color)
        self.__icon_widget.setIcon(QIcon(QPixmap(recolored_image)))

    def getIconSeparatorColor(self) -> QColor:
        """Get the color of the icon separator

        :return: new color
        """

        return self.__icon_separator_color

    def setIconSeparatorColor(self, color: QColor):
        """Set the color of the icon separator

        :param color: new color
        """

        if self.__used:
            return
        self.__icon_separator_color = color

    def getCloseButtonIconColor(self) -> QColor | None:
        """Get the color of the close button icon

        :return: icon color (None if no color is set)
        """

        return self.__close_button_icon_color

    def setCloseButtonIconColor(self, color: QColor | None):
        """Set the color of the close button icon

        :param color: new color (None if the icon should not be recolored)
        """

        if self.__used:
            return

        self.__close_button_icon_color = color
        recolored_image = IconUtils.recolor_image(QIcon(self.__close_button_icon).pixmap(
                                                  self.__close_button.iconSize()).toImage(), color)
        self.__close_button.setIcon(QIcon(QPixmap(recolored_image)))

    def getDurationBarColor(self) -> QColor:
        """Get the color of the duration bar

        :return: color
        """

        return self.__duration_bar_color

    def setDurationBarColor(self, color: QColor):
        """Set the color of the duration bar

        :param color: new color
        """

        if self.__used:
            return
        self.__duration_bar_color = color

    def setDurationBarValue(self, fraction: float):
        """Set the width of the duration bar with the specified fraction
        :param fraction: The fraction of the total width from 0.0 to 1.0
        """
        self.__set_duration_bar(fraction)

    def getTitleFont(self) -> QFont:
        """Get the font of the title

        :return: title font
        """

        return self.__title_font

    def setTitleFont(self, font: QFont):
        """Set the font of the title

        :param font: new title font
        """

        if self.__used:
            return
        self.__title_font = font
        self.__title_label.setFont(font)

    def getTextFont(self) -> QFont:
        """Get the font of the text

        :return: text font
        """

        return self.__text_font

    def setTextFont(self, font: QFont):
        """Set the font of the text

        :param font: new text font
        """

        if self.__used:
            return
        self.__text_font = font
        self.__text_label.setFont(font)

    def getTitleFontSize(self) -> int:
        """Get the font size of the title

        :return: title font size in points
        """
        return self.__title_font.pointSize()

    def setTitleFontSize(self, size: int):
        """Set the font size of the title

        :param size: new title font size in points
        """
        if self.__used:
            return
        self.__title_font.setPointSize(size)
        self.__title_label.setFont(self.__title_font)

    def getTextFontSize(self) -> int:
        """Get the font size of the text

        :return: text font size in points
        """
        return self.__text_font.pointSize()

    def setTextFontSize(self, size: int):
        """Set the font size of the text

        :param size: new text font size in points
        """
        if self.__used:
            return
        self.__text_font.setPointSize(size)
        self.__text_label.setFont(self.__text_font)

    def setFontSize(self, title_size: int, text_size: int = None):
        """Set the font size for both title and text

        :param title_size: title font size in points
        :param text_size: text font size in points (if None, uses title_size)
        """
        if self.__used:
            return

        if text_size is None:
            text_size = title_size

        self.setTitleFontSize(title_size)
        self.setTextFontSize(text_size)

    def setFontFamily(self, family: str):
        """Set the font family for both title and text

        :param family: font family name (e.g., 'Arial', 'Times New Roman')
        """
        if self.__used:
            return

        self.__title_font.setFamily(family)
        self.__text_font.setFamily(family)
        self.__title_label.setFont(self.__title_font)
        self.__text_label.setFont(self.__text_font)

    def getTitleFontFamily(self) -> str:
        """Get the font family of the title

        :return: title font family
        """
        return self.__title_font.family()

    def getTextFontFamily(self) -> str:
        """Get the font family of the text

        :return: text font family
        """
        return self.__text_font.family()

    # ========== Modern Margin API (Replaces 50 individual methods) ==========

    def setMargins(self, margins, margin_type: str = 'content'):
        """Set margins with flexible input types

        :param margins: Can be QMargins, int (all sides), tuple (left,top,right,bottom), or dict
        :param margin_type: 'content', 'icon', 'icon_section', 'text_section', 'close_button'

        Examples:
            toast.setMargins(20)  # All sides 20px
            toast.setMargins((10, 5, 10, 5))  # left, top, right, bottom
            toast.setMargins((15, 10))  # horizontal, vertical
            toast.setMargins({'left': 20, 'right': 10})  # Partial update
            toast.setMargins(QMargins(10, 5, 10, 5))  # QMargins object
            toast.setMargins(15, 'icon')  # Icon margins
        """
        self.margins.set(margins, margin_type)

    def getMargins(self, margin_type: str = 'content') -> QMargins:
        """Get margins for specified type

        :param margin_type: 'content', 'icon', 'icon_section', 'text_section', 'close_button'
        :return: QMargins object
        """
        return self.margins.get(margin_type)

    def adjustMargins(self, margin_type: str = 'content', **kwargs):
        """Adjust specific sides of margins

        :param margin_type: Type of margin to adjust
        :param kwargs: left, top, right, bottom values

        Examples:
            toast.adjustMargins(left=20, right=10)  # Adjust content margins
            toast.adjustMargins('icon', top=5, bottom=5)  # Adjust icon margins
        """
        self.margins.adjust(margin_type, **kwargs)

    # Legacy compatibility methods (simplified)
    def setMarginLeft(self, margin: int):
        """Set left margin of content (legacy compatibility)"""
        self.adjustMargins(left=margin)

    def setMarginTop(self, margin: int):
        """Set top margin of content (legacy compatibility)"""
        self.adjustMargins(top=margin)

    def setMarginRight(self, margin: int):
        """Set right margin of content (legacy compatibility)"""
        self.adjustMargins(right=margin)

    def setMarginBottom(self, margin: int):
        """Set bottom margin of content (legacy compatibility)"""
        self.adjustMargins(bottom=margin)

    def getMarginLeft(self) -> int:
        """Get left margin of content (legacy compatibility)"""
        return self.getMargins().left()

    def getMarginTop(self) -> int:
        """Get top margin of content (legacy compatibility)"""
        return self.getMargins().top()

    def getMarginRight(self) -> int:
        """Get right margin of content (legacy compatibility)"""
        return self.getMargins().right()

    def getMarginBottom(self) -> int:
        """Get bottom margin of content (legacy compatibility)"""
        return self.getMargins().bottom()

    def getTextSectionSpacing(self) -> int:
        """Get the spacing between the title and the text

        :return: spacing
        """

        return self.__text_section_spacing

    def setTextSectionSpacing(self, spacing: int):
        """Set the spacing between the title and the text

        :param spacing: new spacing
        """

        if self.__used:
            return
        self.__text_section_spacing = spacing

    def isMultiline(self) -> bool:
        """Get whether multiline text is enabled
        :return: whether multiline text is enabled
        """

        return self.__multiline

    def setMultiline(self, on: bool):
        """Set whether multiline text should be enabled
        :param on: whether multiline text should be enabled
        """

        if self.__used:
            return
        self.__multiline = on

    def applyPreset(self, preset: ToastPreset):
        """Apply a style preset to the toast

        :param preset: style preset
        """

        if self.__used:
            return

        if preset == ToastPreset.SUCCESS or preset == ToastPreset.SUCCESS_DARK:
            self.setIcon(ToastIcon.SUCCESS)
            self.setIconColor(SUCCESS_ACCENT_COLOR)
            self.setDurationBarColor(SUCCESS_ACCENT_COLOR)

        elif preset == ToastPreset.WARNING or preset == ToastPreset.WARNING_DARK:
            self.setIcon(ToastIcon.WARNING)
            self.setIconColor(WARNING_ACCENT_COLOR)
            self.setDurationBarColor(WARNING_ACCENT_COLOR)

        elif preset == ToastPreset.ERROR or preset == ToastPreset.ERROR_DARK:
            self.setIcon(ToastIcon.ERROR)
            self.setIconColor(ERROR_ACCENT_COLOR)
            self.setDurationBarColor(ERROR_ACCENT_COLOR)

        elif preset == ToastPreset.INFORMATION or preset == ToastPreset.INFORMATION_DARK:
            self.setIcon(ToastIcon.INFORMATION)
            self.setIconColor(INFORMATION_ACCENT_COLOR)
            self.setDurationBarColor(INFORMATION_ACCENT_COLOR)

        if (preset == ToastPreset.SUCCESS
                or preset == ToastPreset.WARNING
                or preset == ToastPreset.ERROR
                or preset == ToastPreset.INFORMATION):
            self.setBackgroundColor(DEFAULT_BACKGROUND_COLOR)
            self.setCloseButtonIconColor(DEFAULT_CLOSE_BUTTON_ICON_COLOR)
            self.setIconSeparatorColor(DEFAULT_ICON_SEPARATOR_COLOR)
            self.setTitleColor(DEFAULT_TITLE_COLOR)
            self.setTextColor(DEFAULT_TEXT_COLOR)

        elif (preset == ToastPreset.SUCCESS_DARK
                or preset == ToastPreset.WARNING_DARK
                or preset == ToastPreset.ERROR_DARK
                or preset == ToastPreset.INFORMATION_DARK):
            self.setBackgroundColor(DEFAULT_BACKGROUND_COLOR_DARK)
            self.setCloseButtonIconColor(DEFAULT_CLOSE_BUTTON_ICON_COLOR_DARK)
            self.setIconSeparatorColor(DEFAULT_ICON_SEPARATOR_COLOR_DARK)
            self.setTitleColor(DEFAULT_TITLE_COLOR_DARK)
            self.setTextColor(DEFAULT_TEXT_COLOR_DARK)

        self.setShowDurationBar(True)
        self.setShowIcon(True)
        self.setShowIconSeparator(True)
        self.setIconSeparatorWidth(2)

    def __update_stylesheet(self):
        """Update the stylesheet of the toast"""

        # Generate cache keys for each stylesheet
        toast_key = f"toast_{self.__background_color.name()}_{self.__border_radius}"
        duration_bar_key = f"duration_bar_{self.__duration_bar_color.red()}_{self.__duration_bar_color.green()}_{self.__duration_bar_color.blue()}_{self.__border_radius}"
        duration_bar_chunk_key = f"duration_bar_chunk_{self.__duration_bar_color.red()}_{self.__duration_bar_color.green()}_{self.__duration_bar_color.blue()}_{self.__border_radius}_{self.__duration == 0}"
        icon_separator_key = f"icon_separator_{self.__icon_separator_color.name()}"
        title_key = f"title_{self.__title_color.name()}"
        text_key = f"text_{self.__text_color.name()}"

        # Toast widget stylesheet
        if toast_key not in self.__cached_stylesheets:
            self.__cached_stylesheets[toast_key] = f'background: {self.__background_color.name()};border-radius: {self.__border_radius}px;'
        self.__toast_widget.setStyleSheet(self.__cached_stylesheets[toast_key])

        # Duration bar stylesheet
        if duration_bar_key not in self.__cached_stylesheets:
            self.__cached_stylesheets[duration_bar_key] = f'background: rgba({self.__duration_bar_color.red()}, {self.__duration_bar_color.green()}, {self.__duration_bar_color.blue()}, 100);border-radius: {self.__border_radius}px;'
        self.__duration_bar.setStyleSheet(self.__cached_stylesheets[duration_bar_key])

        # Duration bar chunk stylesheet
        if duration_bar_chunk_key not in self.__cached_stylesheets:
            right_radius = self.__border_radius if self.__duration == 0 else 0
            self.__cached_stylesheets[duration_bar_chunk_key] = f'background: rgba({self.__duration_bar_color.red()}, {self.__duration_bar_color.green()}, {self.__duration_bar_color.blue()}, 255);border-bottom-left-radius: {self.__border_radius}px;border-bottom-right-radius: {right_radius}px;'
        self.__duration_bar_chunk.setStyleSheet(self.__cached_stylesheets[duration_bar_chunk_key])

        # Icon separator stylesheet
        if icon_separator_key not in self.__cached_stylesheets:
            self.__cached_stylesheets[icon_separator_key] = f'background: {self.__icon_separator_color.name()};'
        self.__icon_separator.setStyleSheet(self.__cached_stylesheets[icon_separator_key])

        # Title label stylesheet
        if title_key not in self.__cached_stylesheets:
            self.__cached_stylesheets[title_key] = f'color: {self.__title_color.name()};'
        self.__title_label.setStyleSheet(self.__cached_stylesheets[title_key])

        # Text label stylesheet
        if text_key not in self.__cached_stylesheets:
            self.__cached_stylesheets[text_key] = f'color: {self.__text_color.name()};'
        self.__text_label.setStyleSheet(self.__cached_stylesheets[text_key])

    @staticmethod
    def __update_currently_showing_position_xy(animate: bool = True):
        """Update the x and y position of every currently showing toast

        :param animate: whether the position change should be animated
        """

        for toast in Toast.__currently_shown:
            toast.__update_position_xy(animate)

    @staticmethod
    def __update_currently_showing_position_x(animate: bool = True):
        """Update the x position of every currently showing toast

        :param animate: whether the position change should be animated
        """

        for toast in Toast.__currently_shown:
            toast.__update_position_x(animate)

    @staticmethod
    def __update_currently_showing_position_y(animate: bool = True):
        """Update the y position of every currently showing toast

        :param animate: whether the position change should be animated
        """

        for toast in Toast.__currently_shown:
            toast.__update_position_y(animate)

    @staticmethod
    def __show_next_in_queue():
        """Show next toast in queue"""

        if len(Toast.__queue) > 0:
            next_toast = Toast.__queue.pop(0)
            next_toast.show()

    @staticmethod
    def getMaximumOnScreen():
        """Get the maximum amount of toasts allowed
        to be shown at the same time

        :return: maximum toast amount
        """

        return Toast.__maximum_on_screen

    @staticmethod
    def setMaximumOnScreen(maximum_on_screen: int):
        """Set the maximum amount of toasts allowed
        to be shown at the same time

        :param maximum_on_screen: new maximum toast amount
        """
        freed_spaces = maximum_on_screen - Toast.__maximum_on_screen
        Toast.__maximum_on_screen = maximum_on_screen

        if freed_spaces > 0:
            for i in range(freed_spaces):
                Toast.__show_next_in_queue()

    @staticmethod
    def getSpacing() -> int:
        """Get the spacing between toast notifications

        :return: spacing
        """

        return Toast.__spacing

    @staticmethod
    def setSpacing(spacing: int):
        """Set the spacing between toast notifications

        :param spacing: new spacing
        """

        Toast.__spacing = spacing
        Toast.__update_currently_showing_position_y()

    @staticmethod
    def getOffsetX() -> int:
        """Get the offset for the toasts on the x-axis

        :return: x-axis offset
        """

        return Toast.__offset_x

    @staticmethod
    def setOffsetX(offset_x: int):
        """Set the offset for the toasts on the x-axis

        :param offset_x: new x-axis offset
        """

        Toast.__offset_x = offset_x
        Toast.__update_currently_showing_position_x()

    @staticmethod
    def getOffsetY() -> int:
        """Get the offset for the toasts on the y-axis

        :return: y-axis offset
        """

        return Toast.__offset_y

    @staticmethod
    def setOffsetY(offset_y: int):
        """Set the offset for the toasts on the y-axis

        :param offset_y: new y-axis offset
        """

        Toast.__offset_y = offset_y
        Toast.__update_currently_showing_position_y()

    @staticmethod
    def getOffset() -> tuple[int, int]:
        """Get the offset for the toasts on the x and y-axis

        :return: x and y-axis offset
        """

        return Toast.__offset_x, Toast.__offset_y

    @staticmethod
    def setOffset(offset_x: int, offset_y: int):
        """Set the offset for the toasts on the x and y-axis

        :param offset_x: new x-axis offset
        :param offset_y: new y-axis offset
        """

        Toast.__offset_x = offset_x
        Toast.__offset_y = offset_y
        Toast.__update_currently_showing_position_xy()

    @staticmethod
    def getPositionRelativeToWidget() -> QWidget | None:
        """Get the widget that the position is relative to (if any)

        :return: widget that the position is relative to or None
        """

        return Toast.__position_relative_to_widget

    @staticmethod
    def setPositionRelativeToWidget(widget: QWidget | None):
        """Set the widget that the position is relative to

        :param widget: widget that the position is relative to
        """

        if widget is None:
            # Remove event filters
            for toast in Toast.__currently_shown + Toast.__queue:
                toast.__remove_widget_event_filter()
                toast.__remove_watched_widgets_event_filters()

        Toast.__position_relative_to_widget = widget

        if widget is not None:
            # Install event filters
            for toast in Toast.__currently_shown + Toast.__queue:
                toast.__install_widget_event_filter()
                toast.__install_watched_widgets_event_filters()

        Toast.__update_currently_showing_position_xy()

    @staticmethod
    def isMovePositionWithWidget() -> bool:
        """Get whether the position is moving with the widget when it moves or resizes

        :return: whether the position is moving with the widget
        """

        return Toast.__move_position_with_widget

    @staticmethod
    def setMovePositionWithWidget(on: bool):
        """Set whether the position should move with the widget when it moves or resizes

        :param on: whether the position should move with the widget
        """

        Toast.__move_position_with_widget = on

        if on:
            # Install event filters
            for toast in Toast.__currently_shown + Toast.__queue:
                toast.__install_widget_event_filter()
                toast.__install_watched_widgets_event_filters()
        else:
            # Remove event filters
            for toast in Toast.__currently_shown + Toast.__queue:
                toast.__remove_widget_event_filter()
                toast.__remove_watched_widgets_event_filters()

    @staticmethod
    def isAlwaysOnMainScreen() -> bool:
        """Get whether the toasts are always being shown on the main screen

        :return: whether the always on main screen option is enabled
        """

        return Toast.__always_on_main_screen

    @staticmethod
    def setAlwaysOnMainScreen(on: bool):
        """Set whether the toasts should always be shown on the main screen

        :param on: whether the always on main screen option should be enabled
        """

        Toast.__always_on_main_screen = on
        Toast.__update_currently_showing_position_xy()

    @staticmethod
    def getFixedScreen() -> QScreen | None:
        """Get the fixed screen where the toasts are shown

        :return: screen if fixed screen is set, else None
        """

        return Toast.__fixed_screen

    @staticmethod
    def setFixedScreen(screen: QScreen | None):
        """Set a fixed screen where the toasts will be shown

        :param screen: fixed screen (or None to unset)
        """

        Toast.__fixed_screen = screen
        Toast.__update_currently_showing_position_xy()

    @staticmethod
    def getPosition() -> ToastPosition:
        """Get the position where the toasts are shown

        :return: position
        """

        return Toast.__position

    @staticmethod
    def setPosition(position: ToastPosition):
        """Set the position where the toasts will be shown

        :param position: new position
        """

        Toast.__position = position
        Toast.__update_currently_showing_position_xy()

    @staticmethod
    def getCount() -> int:
        """Get the amount of toasts that are either currently visible
        or queued to be shown

        :return: the amount of visible and queued toasts
        """

        return len(Toast.__currently_shown) + len(Toast.__queue)

    @staticmethod
    def getVisibleCount() -> int:
        """Get the amount of toasts that are currently visible

        :return: the amount of visible toasts
        """

        return len(Toast.__currently_shown)

    @staticmethod
    def getQueuedCount() -> int:
        """Get the amount of toasts in the queue to be shown

        :return: the amount of toasts in the queue
        """

        return len(Toast.__queue)

    @staticmethod
    def reset():
        """Reset the Toast class completely (reset static attributes
         to defaults, hide all toasts instantly, and clear queue)"""

        # Reset static attributes
        Toast.__maximum_on_screen = 3
        Toast.__spacing = 10
        Toast.__offset_x = 20
        Toast.__offset_y = 50
        Toast.__position_relative_to_widget = None
        Toast.__move_position_with_widget = True
        Toast.__always_on_main_screen = False
        Toast.__fixed_screen = None
        Toast.__position = ToastPosition.BOTTOM_RIGHT

        # Hide currently showing toasts and clear queue
        for toast in Toast.__currently_shown:
            toast.setVisible(False)
            toast.deleteLater()

        # Remove event filters on watched widgets
        for toast in Toast.__currently_shown + Toast.__queue:
            toast.__remove_watched_widgets_event_filters()

        Toast.__currently_shown.clear()
        Toast.__queue.clear()
