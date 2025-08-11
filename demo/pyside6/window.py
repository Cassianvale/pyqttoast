from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QCheckBox,
    QWidget,
    QGroupBox,
    QSpinBox,
    QLineEdit,
    QHBoxLayout,
    QLabel,
    QFormLayout,
)

from pyqttoast import Toast, ToastPreset, ToastIcon, ToastPosition, ToastButtonAlignment
from language_manager import LanguageManager


class Window(QMainWindow):
    """
    Main window for PyQt Toast demonstration.
    """

    def __init__(self):
        super().__init__(parent=None)

        # Initialize language management system
        self.language_manager = LanguageManager()

        # Window settings
        self.setFixedSize(1000, 600)  # Reduced size since we removed progress demo
        self.setWindowTitle(self.language_manager.get_text("window_title"))

        # Create UI layout
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the user interface."""
        # Create main layout with language toggle
        main_layout = QVBoxLayout()

        # Add language toggle button at the top
        language_layout = QHBoxLayout()
        self.language_toggle_button = QPushButton(self.language_manager.get_text("toggle_language"))
        self.language_toggle_button.setFixedHeight(32)
        self.language_toggle_button.clicked.connect(self.toggle_language)
        language_layout.addStretch()
        language_layout.addWidget(self.language_toggle_button)
        main_layout.addLayout(language_layout)

        # Create horizontal layout for better space utilization
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Left column - Settings and Toast Presets
        left_column = QVBoxLayout()
        left_column.setSpacing(15)
        left_column.addWidget(self.create_static_settings_group())
        left_column.addWidget(self.create_toast_preset_group())
        left_column.addStretch()  # Add stretch to push content to top

        # Right column - Custom Toast
        right_column = QVBoxLayout()
        right_column.setSpacing(15)
        right_column.addWidget(self.create_toast_custom_group())
        right_column.addStretch()  # Add stretch to push content to top

        # Add columns to content layout with equal stretch
        content_layout.addLayout(left_column, 1)
        content_layout.addLayout(right_column, 1)

        main_layout.addLayout(content_layout)

        # Apply layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.setFocus()

    def toggle_language(self) -> None:
        """Toggle between Chinese and English languages and update all UI elements."""
        self.language_manager.toggle_language()
        self._update_all_ui_text()

    def _update_all_ui_text(self) -> None:
        """Update all UI text elements to reflect the current language."""
        # Update window title
        self.setWindowTitle(self.language_manager.get_text("window_title"))

        # Update language toggle button
        self.language_toggle_button.setText(self.language_manager.get_text("toggle_language"))

        # Update all group boxes and their contents
        self._update_static_settings_text()
        self._update_toast_preset_text()
        self._update_custom_toast_text()

    def create_static_settings_group(self):
        self.static_settings_group = QGroupBox(self.language_manager.get_text("static_settings"))

        # Create widgets
        self.maximum_on_screen_spinbox = QSpinBox()
        self.maximum_on_screen_spinbox.setRange(1, 10)
        self.maximum_on_screen_spinbox.setValue(Toast.getMaximumOnScreen())
        self.maximum_on_screen_spinbox.setFixedHeight(24)

        self.spacing_spinbox = QSpinBox()
        self.spacing_spinbox.setRange(0, 100)
        self.spacing_spinbox.setValue(Toast.getSpacing())
        self.spacing_spinbox.setFixedHeight(24)

        self.offset_x_spinbox = QSpinBox()
        self.offset_x_spinbox.setRange(0, 500)
        self.offset_x_spinbox.setValue(Toast.getOffsetX())
        self.offset_x_spinbox.setFixedHeight(24)

        self.offset_y_spinbox = QSpinBox()
        self.offset_y_spinbox.setRange(0, 500)
        self.offset_y_spinbox.setValue(Toast.getOffsetY())
        self.offset_y_spinbox.setFixedHeight(24)

        self.always_on_main_screen_checkbox = QCheckBox(self.language_manager.get_text("always_main_screen"))

        self.position_dropdown = QComboBox()
        self._populate_position_dropdown()
        self.position_dropdown.setCurrentIndex(2)
        self.position_dropdown.setFixedHeight(26)

        self.update_button = QPushButton(self.language_manager.get_text("update_button"))
        self.update_button.setFixedHeight(32)
        self.update_button.clicked.connect(self.update_static_settings)

        # Store labels for later updates
        self.max_on_screen_label = QLabel(self.language_manager.get_text("max_on_screen"))
        self.spacing_label = QLabel(self.language_manager.get_text("spacing"))
        self.x_offset_label = QLabel(self.language_manager.get_text("x_offset"))
        self.y_offset_label = QLabel(self.language_manager.get_text("y_offset"))
        self.position_label = QLabel(self.language_manager.get_text("position"))

        # Add widgets to layout
        form_layout = QFormLayout()
        form_layout.addRow(self.max_on_screen_label, self.maximum_on_screen_spinbox)
        form_layout.addRow(self.spacing_label, self.spacing_spinbox)
        form_layout.addRow(self.x_offset_label, self.offset_x_spinbox)
        form_layout.addRow(self.y_offset_label, self.offset_y_spinbox)
        form_layout.addRow(self.position_label, self.position_dropdown)

        # Add layout and widgets to main layout
        vbox_layout = QVBoxLayout()
        vbox_layout.addLayout(form_layout)
        vbox_layout.addWidget(self.always_on_main_screen_checkbox)
        vbox_layout.addWidget(self.update_button)
        vbox_layout.addStretch(1)
        self.static_settings_group.setLayout(vbox_layout)

        # Set minimum size to ensure complete display
        self.static_settings_group.setMinimumHeight(200)
        self.static_settings_group.setMinimumWidth(300)

        return self.static_settings_group

    def _populate_position_dropdown(self):
        """Populate position dropdown with localized text."""
        self.position_dropdown.clear()
        positions = ["bottom_left", "bottom_middle", "bottom_right", "top_left", "top_middle", "top_right", "center"]
        for pos in positions:
            self.position_dropdown.addItem(self.language_manager.get_text(pos))

    def _update_static_settings_text(self):
        """Update static settings group text elements."""
        self.static_settings_group.setTitle(self.language_manager.get_text("static_settings"))
        self.always_on_main_screen_checkbox.setText(self.language_manager.get_text("always_main_screen"))
        self.update_button.setText(self.language_manager.get_text("update_button"))

        # Update labels
        self.max_on_screen_label.setText(self.language_manager.get_text("max_on_screen"))
        self.spacing_label.setText(self.language_manager.get_text("spacing"))
        self.x_offset_label.setText(self.language_manager.get_text("x_offset"))
        self.y_offset_label.setText(self.language_manager.get_text("y_offset"))
        self.position_label.setText(self.language_manager.get_text("position"))

        # Update dropdown items
        current_index = self.position_dropdown.currentIndex()
        self._populate_position_dropdown()
        self.position_dropdown.setCurrentIndex(current_index)

    def create_toast_preset_group(self):
        self.toast_preset_group = QGroupBox(self.language_manager.get_text("toast_presets"))

        # Create widgets
        self.preset_dropdown = QComboBox()
        self._populate_preset_dropdown()
        self.preset_dropdown.setFixedHeight(26)

        self.show_preset_toast_button = QPushButton(self.language_manager.get_text("show_preset_toast"))
        self.show_preset_toast_button.clicked.connect(self.show_preset_toast)
        self.show_preset_toast_button.setFixedHeight(32)

        # Add widgets to layout
        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(self.preset_dropdown)
        vbox_layout.addWidget(self.show_preset_toast_button)
        vbox_layout.addStretch(1)
        self.toast_preset_group.setLayout(vbox_layout)

        # Set minimum size to ensure complete display
        self.toast_preset_group.setMinimumHeight(120)
        self.toast_preset_group.setMinimumWidth(300)

        return self.toast_preset_group

    def _populate_preset_dropdown(self):
        """Populate preset dropdown with localized text."""
        self.preset_dropdown.clear()
        presets = [
            "success",
            "warning",
            "error",
            "information",
            "success_dark",
            "warning_dark",
            "error_dark",
            "information_dark",
        ]
        for preset in presets:
            self.preset_dropdown.addItem(self.language_manager.get_text(preset))

    def _update_toast_preset_text(self):
        """Update toast preset group text elements."""
        self.toast_preset_group.setTitle(self.language_manager.get_text("toast_presets"))
        self.show_preset_toast_button.setText(self.language_manager.get_text("show_preset_toast"))

        # Update dropdown items
        current_index = self.preset_dropdown.currentIndex()
        self._populate_preset_dropdown()
        self.preset_dropdown.setCurrentIndex(current_index)

    def create_toast_custom_group(self):
        self.custom_toast_group = QGroupBox(self.language_manager.get_text("custom_toast"))

        # Create widgets
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(0, 50000)
        self.duration_spinbox.setValue(5000)
        self.duration_spinbox.setFixedHeight(24)

        self.title_input = QLineEdit(self.language_manager.get_text("default_title"))
        self.title_input.setFixedHeight(24)

        self.text_input = QLineEdit(
            "This is a much longer text that demonstrates multiline functionality. It should wrap properly when the multiline checkbox is enabled."
        )
        self.text_input.setFixedHeight(24)

        self.border_radius_spinbox = QSpinBox()
        self.border_radius_spinbox.setRange(0, 20)
        self.border_radius_spinbox.setValue(8)
        self.border_radius_spinbox.setFixedHeight(24)

        self.show_icon_checkbox = QCheckBox(self.language_manager.get_text("show_icon"))

        self.icon_dropdown = QComboBox()
        self._populate_icon_dropdown()
        self.icon_dropdown.setFixedHeight(24)

        self.icon_size_spinbox = QSpinBox()
        self.icon_size_spinbox.setRange(5, 50)
        self.icon_size_spinbox.setValue(18)
        self.icon_size_spinbox.setFixedHeight(24)

        self.show_duration_bar_checkbox = QCheckBox(self.language_manager.get_text("show_duration_bar"))
        self.show_duration_bar_checkbox.setChecked(True)

        self.reset_on_hover_checkbox = QCheckBox(self.language_manager.get_text("reset_on_hover"))
        self.reset_on_hover_checkbox.setChecked(True)

        self.multiline_checkbox = QCheckBox(self.language_manager.get_text("multiline_text"))
        self.multiline_checkbox.setChecked(False)

        self.close_button_settings_dropdown = QComboBox()
        self._populate_close_button_dropdown()
        self.close_button_settings_dropdown.setFixedHeight(24)

        self.min_width_spinbox = QSpinBox()
        self.min_width_spinbox.setRange(0, 1000)
        self.min_width_spinbox.setFixedHeight(24)

        self.max_width_spinbox = QSpinBox()
        self.max_width_spinbox.setRange(0, 1000)
        self.max_width_spinbox.setValue(1000)
        self.max_width_spinbox.setFixedHeight(24)

        self.min_height_spinbox = QSpinBox()
        self.min_height_spinbox.setRange(0, 1000)
        self.min_height_spinbox.setFixedHeight(24)

        self.max_height_spinbox = QSpinBox()
        self.max_height_spinbox.setRange(0, 1000)
        self.max_height_spinbox.setValue(1000)
        self.max_height_spinbox.setFixedHeight(24)

        self.fade_in_duration_spinbox = QSpinBox()
        self.fade_in_duration_spinbox.setRange(0, 1000)
        self.fade_in_duration_spinbox.setValue(250)
        self.fade_in_duration_spinbox.setFixedHeight(24)

        self.fade_out_duration_spinbox = QSpinBox()
        self.fade_out_duration_spinbox.setRange(0, 1000)
        self.fade_out_duration_spinbox.setValue(250)
        self.fade_out_duration_spinbox.setFixedHeight(24)

        # Font customization controls
        self.title_font_size_spinbox = QSpinBox()
        self.title_font_size_spinbox.setRange(6, 72)
        self.title_font_size_spinbox.setValue(12)
        self.title_font_size_spinbox.setFixedHeight(24)

        self.text_font_size_spinbox = QSpinBox()
        self.text_font_size_spinbox.setRange(6, 72)
        self.text_font_size_spinbox.setValue(10)
        self.text_font_size_spinbox.setFixedHeight(24)

        self.font_family_dropdown = QComboBox()
        self.font_family_dropdown.addItems(['Arial', 'Times New Roman', 'Courier New', 'Helvetica', 'Georgia', 'Verdana', 'Tahoma'])
        self.font_family_dropdown.setCurrentText('Arial')
        self.font_family_dropdown.setFixedHeight(24)

        # Font preset buttons
        self.small_font_button = QPushButton(self.language_manager.get_text("small_font"))
        self.small_font_button.setFixedHeight(28)
        self.small_font_button.clicked.connect(self.set_small_font)

        self.medium_font_button = QPushButton(self.language_manager.get_text("medium_font"))
        self.medium_font_button.setFixedHeight(28)
        self.medium_font_button.clicked.connect(self.set_medium_font)

        self.large_font_button = QPushButton(self.language_manager.get_text("large_font"))
        self.large_font_button.setFixedHeight(28)
        self.large_font_button.clicked.connect(self.set_large_font)

        # Test buttons for font features
        self.test_links_button = QPushButton(self.language_manager.get_text("test_clickable_links"))
        self.test_links_button.setFixedHeight(28)
        self.test_links_button.clicked.connect(self.test_clickable_links)

        self.custom_toast_button = QPushButton(self.language_manager.get_text("show_custom_toast"))
        self.custom_toast_button.setFixedHeight(32)
        self.custom_toast_button.clicked.connect(self.show_custom_toast)

        # Store labels for later updates
        self.duration_label = QLabel(self.language_manager.get_text("duration"))
        self.title_label = QLabel(self.language_manager.get_text("title"))
        self.text_label = QLabel(self.language_manager.get_text("text"))
        self.icon_size_label = QLabel(self.language_manager.get_text("icon_size"))
        self.border_radius_label = QLabel(self.language_manager.get_text("border_radius"))
        self.close_button_label = QLabel(self.language_manager.get_text("close_button"))
        self.min_width_label = QLabel(self.language_manager.get_text("min_width"))
        self.max_width_label = QLabel(self.language_manager.get_text("max_width"))
        self.min_height_label = QLabel(self.language_manager.get_text("min_height"))
        self.max_height_label = QLabel(self.language_manager.get_text("max_height"))
        self.fade_in_label = QLabel(self.language_manager.get_text("fade_in_duration"))
        self.fade_out_label = QLabel(self.language_manager.get_text("fade_out_duration"))

        # Font customization labels
        self.title_font_size_label = QLabel(self.language_manager.get_text("title_font_size"))
        self.text_font_size_label = QLabel(self.language_manager.get_text("text_font_size"))
        self.font_family_label = QLabel(self.language_manager.get_text("font_family"))
        self.font_presets_label = QLabel(self.language_manager.get_text("font_presets"))

        # Add widgets to layouts
        form_layout = QFormLayout()
        form_layout.addRow(self.duration_label, self.duration_spinbox)
        form_layout.addRow(self.title_label, self.title_input)
        form_layout.addRow(self.text_label, self.text_input)

        icon_size_layout = QFormLayout()
        icon_size_layout.addRow(self.icon_size_label, self.icon_size_spinbox)
        icon_size_layout.setContentsMargins(20, 0, 0, 0)

        icon_layout = QHBoxLayout()
        icon_layout.addWidget(self.show_icon_checkbox)
        icon_layout.addWidget(self.icon_dropdown)
        icon_layout.addLayout(icon_size_layout)
        icon_layout.setContentsMargins(0, 5, 0, 3)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(self.show_duration_bar_checkbox)
        checkbox_layout.addWidget(self.reset_on_hover_checkbox)
        checkbox_layout.addWidget(self.multiline_checkbox)
        checkbox_layout.setContentsMargins(0, 0, 0, 5)

        double_form_layout_1 = QHBoxLayout()
        double_form_layout_1.addWidget(self.border_radius_label)
        double_form_layout_1.addWidget(self.border_radius_spinbox)
        double_form_layout_1.addWidget(self.close_button_label)
        double_form_layout_1.addWidget(self.close_button_settings_dropdown)

        double_form_layout_2 = QHBoxLayout()
        double_form_layout_2.addWidget(self.min_width_label)
        double_form_layout_2.addWidget(self.min_width_spinbox)
        double_form_layout_2.addWidget(self.max_width_label)
        double_form_layout_2.addWidget(self.max_width_spinbox)

        double_form_layout_3 = QHBoxLayout()
        double_form_layout_3.addWidget(self.min_height_label)
        double_form_layout_3.addWidget(self.min_height_spinbox)
        double_form_layout_3.addWidget(self.max_height_label)
        double_form_layout_3.addWidget(self.max_height_spinbox)

        double_form_layout_4 = QHBoxLayout()
        double_form_layout_4.addWidget(self.fade_in_label)
        double_form_layout_4.addWidget(self.fade_in_duration_spinbox)
        double_form_layout_4.addWidget(self.fade_out_label)
        double_form_layout_4.addWidget(self.fade_out_duration_spinbox)
        double_form_layout_4.setContentsMargins(0, 0, 0, 3)

        # Font customization layouts
        font_size_layout = QHBoxLayout()
        font_size_layout.addWidget(self.title_font_size_label)
        font_size_layout.addWidget(self.title_font_size_spinbox)
        font_size_layout.addWidget(self.text_font_size_label)
        font_size_layout.addWidget(self.text_font_size_spinbox)

        font_family_layout = QHBoxLayout()
        font_family_layout.addWidget(self.font_family_label)
        font_family_layout.addWidget(self.font_family_dropdown)

        font_presets_layout = QHBoxLayout()
        font_presets_layout.addWidget(self.font_presets_label)
        font_presets_layout.addWidget(self.small_font_button)
        font_presets_layout.addWidget(self.medium_font_button)
        font_presets_layout.addWidget(self.large_font_button)

        # Action buttons layout - put test links and custom toast buttons side by side
        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.addWidget(self.test_links_button)
        action_buttons_layout.addWidget(self.custom_toast_button)

        # Add layouts and widgets to main layout
        vbox_layout = QVBoxLayout()
        vbox_layout.addLayout(form_layout)
        vbox_layout.addLayout(icon_layout)
        vbox_layout.addLayout(checkbox_layout)
        vbox_layout.addLayout(double_form_layout_1)
        vbox_layout.addLayout(double_form_layout_2)
        vbox_layout.addLayout(double_form_layout_3)
        vbox_layout.addLayout(double_form_layout_4)
        vbox_layout.addLayout(font_size_layout)
        vbox_layout.addLayout(font_family_layout)
        vbox_layout.addLayout(font_presets_layout)
        vbox_layout.addLayout(action_buttons_layout)
        vbox_layout.addStretch(1)
        self.custom_toast_group.setLayout(vbox_layout)

        # Set minimum size to ensure complete display
        self.custom_toast_group.setMinimumHeight(500)
        self.custom_toast_group.setMinimumWidth(400)

        return self.custom_toast_group

    def _apply_custom_toast_settings(self, toast: Toast) -> None:
        """Apply all custom toast settings from the UI controls to a toast instance."""
        # Apply basic settings
        toast.setBorderRadius(self.border_radius_spinbox.value())
        toast.setShowIcon(self.show_icon_checkbox.isChecked())
        toast.setIconSize(QSize(self.icon_size_spinbox.value(), self.icon_size_spinbox.value()))
        toast.setShowDurationBar(self.show_duration_bar_checkbox.isChecked())
        toast.setResetDurationOnHover(self.reset_on_hover_checkbox.isChecked())
        toast.setMinimumWidth(self.min_width_spinbox.value())
        toast.setMaximumWidth(self.max_width_spinbox.value())
        toast.setMinimumHeight(self.min_height_spinbox.value())
        toast.setMaximumHeight(self.max_height_spinbox.value())
        toast.setFadeInDuration(self.fade_in_duration_spinbox.value())
        toast.setFadeOutDuration(self.fade_out_duration_spinbox.value())
        toast.setMultiline(self.multiline_checkbox.isChecked())

        # Apply icon settings
        icon_index = self.icon_dropdown.currentIndex()
        icon_map = [ToastIcon.SUCCESS, ToastIcon.WARNING, ToastIcon.ERROR, ToastIcon.INFORMATION, ToastIcon.CLOSE]
        if 0 <= icon_index < len(icon_map):
            toast.setIcon(icon_map[icon_index])

        # Apply close button settings
        close_button_index = self.close_button_settings_dropdown.currentIndex()
        if close_button_index == 0:  # Top
            toast.setCloseButtonAlignment(ToastButtonAlignment.TOP)
        elif close_button_index == 1:  # Middle
            toast.setCloseButtonAlignment(ToastButtonAlignment.MIDDLE)
        elif close_button_index == 2:  # Bottom
            toast.setCloseButtonAlignment(ToastButtonAlignment.BOTTOM)
        elif close_button_index == 3:  # Disabled
            toast.setShowCloseButton(False)

        # Apply font customizations
        title_font_size = self.title_font_size_spinbox.value()
        text_font_size = self.text_font_size_spinbox.value()
        font_family = self.font_family_dropdown.currentText()
        toast.setFontFamily(font_family)
        toast.setFontSize(title_font_size, text_font_size)

    def _populate_icon_dropdown(self):
        """Populate icon dropdown with localized text."""
        self.icon_dropdown.clear()
        icons = ["success", "warning", "error", "information", "close"]
        for icon in icons:
            self.icon_dropdown.addItem(self.language_manager.get_text(icon))

    def _populate_close_button_dropdown(self):
        """Populate close button dropdown with localized text."""
        self.close_button_settings_dropdown.clear()
        positions = ["top", "middle", "bottom", "disabled"]
        for pos in positions:
            self.close_button_settings_dropdown.addItem(self.language_manager.get_text(pos))

    def _update_custom_toast_text(self):
        """Update custom toast group text elements."""
        self.custom_toast_group.setTitle(self.language_manager.get_text("custom_toast"))
        self.show_icon_checkbox.setText(self.language_manager.get_text("show_icon"))
        self.show_duration_bar_checkbox.setText(self.language_manager.get_text("show_duration_bar"))
        self.reset_on_hover_checkbox.setText(self.language_manager.get_text("reset_on_hover"))
        self.multiline_checkbox.setText(self.language_manager.get_text("multiline_text"))
        self.custom_toast_button.setText(self.language_manager.get_text("show_custom_toast"))
        self.title_input.setText(self.language_manager.get_text("default_title"))

        # Update labels
        self.duration_label.setText(self.language_manager.get_text("duration"))
        self.title_label.setText(self.language_manager.get_text("title"))
        self.text_label.setText(self.language_manager.get_text("text"))
        self.icon_size_label.setText(self.language_manager.get_text("icon_size"))
        self.border_radius_label.setText(self.language_manager.get_text("border_radius"))
        self.close_button_label.setText(self.language_manager.get_text("close_button"))
        self.min_width_label.setText(self.language_manager.get_text("min_width"))
        self.max_width_label.setText(self.language_manager.get_text("max_width"))
        self.min_height_label.setText(self.language_manager.get_text("min_height"))
        self.max_height_label.setText(self.language_manager.get_text("max_height"))
        self.fade_in_label.setText(self.language_manager.get_text("fade_in_duration"))
        self.fade_out_label.setText(self.language_manager.get_text("fade_out_duration"))

        # Update font customization labels
        self.title_font_size_label.setText(self.language_manager.get_text("title_font_size"))
        self.text_font_size_label.setText(self.language_manager.get_text("text_font_size"))
        self.font_family_label.setText(self.language_manager.get_text("font_family"))
        self.font_presets_label.setText(self.language_manager.get_text("font_presets"))

        # Update font preset buttons
        self.small_font_button.setText(self.language_manager.get_text("small_font"))
        self.medium_font_button.setText(self.language_manager.get_text("medium_font"))
        self.large_font_button.setText(self.language_manager.get_text("large_font"))
        self.test_links_button.setText(self.language_manager.get_text("test_clickable_links"))

        # Update dropdown items
        icon_index = self.icon_dropdown.currentIndex()
        self._populate_icon_dropdown()
        self.icon_dropdown.setCurrentIndex(icon_index)

        close_button_index = self.close_button_settings_dropdown.currentIndex()
        self._populate_close_button_dropdown()
        self.close_button_settings_dropdown.setCurrentIndex(close_button_index)

    def update_static_settings(self):
        # Update the static settings of the Toast class
        Toast.setMaximumOnScreen(self.maximum_on_screen_spinbox.value())
        Toast.setSpacing(self.spacing_spinbox.value())
        Toast.setOffset(self.offset_x_spinbox.value(), self.offset_y_spinbox.value())
        Toast.setAlwaysOnMainScreen(self.always_on_main_screen_checkbox.isChecked())

        # Map position dropdown index to position enum
        position_index = self.position_dropdown.currentIndex()
        position_map = [
            ToastPosition.BOTTOM_LEFT,
            ToastPosition.BOTTOM_MIDDLE,
            ToastPosition.BOTTOM_RIGHT,
            ToastPosition.TOP_LEFT,
            ToastPosition.TOP_MIDDLE,
            ToastPosition.TOP_RIGHT,
            ToastPosition.CENTER,
        ]

        if 0 <= position_index < len(position_map):
            Toast.setPosition(position_map[position_index])

    def show_preset_toast(self):
        # Show toast with selected preset using custom toast settings
        toast = Toast(self)

        # Use custom toast settings for duration and other properties
        toast.setDuration(self.duration_spinbox.value())

        # Apply all custom toast settings using the helper method
        self._apply_custom_toast_settings(toast)

        # Map preset dropdown index to preset type
        preset_index = self.preset_dropdown.currentIndex()
        preset_configs = [
            # success
            (
                self.language_manager.get_text("success_title"),
                self.language_manager.get_text("success_text"),
                ToastPreset.SUCCESS,
            ),
            # warning
            (
                self.language_manager.get_text("warning_title"),
                self.language_manager.get_text("warning_text"),
                ToastPreset.WARNING,
            ),
            # error
            (
                self.language_manager.get_text("error_title"),
                self.language_manager.get_text("error_text"),
                ToastPreset.ERROR,
            ),
            # information
            (
                self.language_manager.get_text("info_title"),
                self.language_manager.get_text("info_text"),
                ToastPreset.INFORMATION,
            ),
            # success_dark
            (
                self.language_manager.get_text("success_title"),
                self.language_manager.get_text("success_text"),
                ToastPreset.SUCCESS_DARK,
            ),
            # warning_dark
            (
                self.language_manager.get_text("warning_title"),
                self.language_manager.get_text("warning_text"),
                ToastPreset.WARNING_DARK,
            ),
            # error_dark
            (
                self.language_manager.get_text("error_title"),
                self.language_manager.get_text("error_text"),
                ToastPreset.ERROR_DARK,
            ),
            # information_dark
            (
                self.language_manager.get_text("info_title"),
                self.language_manager.get_text("info_text"),
                ToastPreset.INFORMATION_DARK,
            ),
        ]

        if 0 <= preset_index < len(preset_configs):
            title, text, preset = preset_configs[preset_index]
            toast.setTitle(title)
            toast.setText(text)
            toast.applyPreset(preset)

        toast.show()

    def show_custom_toast(self):
        # Show custom toast with selected settings
        toast = Toast(self)
        toast.setDuration(self.duration_spinbox.value())
        toast.setTitle(self.title_input.text())
        toast.setText(self.text_input.text())

        # Apply all custom toast settings using the helper method
        self._apply_custom_toast_settings(toast)

        toast.show()

    def set_small_font(self):
        """Set font sizes to small preset (10pt)"""
        self.title_font_size_spinbox.setValue(10)
        self.text_font_size_spinbox.setValue(10)

    def set_medium_font(self):
        """Set font sizes to medium preset (12pt)"""
        self.title_font_size_spinbox.setValue(12)
        self.text_font_size_spinbox.setValue(10)

    def set_large_font(self):
        """Set font sizes to large preset (18pt)"""
        self.title_font_size_spinbox.setValue(18)
        self.text_font_size_spinbox.setValue(16)

    def test_clickable_links(self):
        """Test clickable links functionality using all custom toast settings"""
        toast = Toast(self)

        # Use custom toast settings for duration, title, and special text for links
        toast.setDuration(self.duration_spinbox.value())
        toast.setTitle(self.language_manager.get_text("clickable_links_title"))
        toast.setText(self.language_manager.get_text("clickable_links_text"))

        # Apply all custom toast settings using the helper method
        self._apply_custom_toast_settings(toast)

        # Use Information preset as default for link testing
        toast.applyPreset(ToastPreset.INFORMATION)
        toast.show()
