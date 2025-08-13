from PySide6.QtCore import QSize, QTimer
from PySide6.QtGui import QColor
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
    QColorDialog,
    QTabWidget,
)

from pyqttoast import Toast, ToastPreset, ToastIcon, ToastPosition, ToastButtonAlignment, ToastAnimationDirection


class Window(QMainWindow):
    """
    Main window for PyQt Toast demonstration.
    """

    def __init__(self):
        super().__init__(parent=None)

        # Window settings
        self.setFixedSize(1200, 900)
        self.setWindowTitle("PyQt Toast Demo")

        # Create UI layout
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the user interface."""
        # Create main layout
        main_layout = QVBoxLayout()

        # Create tab widget for better organization
        self.tab_widget = QTabWidget()

        # Basic Settings and Presets
        basic_tab = QWidget()
        basic_layout = QHBoxLayout(basic_tab)
        basic_layout.setSpacing(20)

        # Left column - Static Settings and Presets
        left_column = QVBoxLayout()
        left_column.setSpacing(15)
        left_column.addWidget(self.create_static_settings_group())
        left_column.addWidget(self.create_toast_preset_group())
        left_column.addStretch()

        # Right column - Custom Toast
        right_column = QVBoxLayout()
        right_column.setSpacing(15)
        right_column.addWidget(self.create_toast_custom_group())
        right_column.addStretch()

        basic_layout.addLayout(left_column, 1)
        basic_layout.addLayout(right_column, 1)

        # Add only the basic tab
        self.tab_widget.addTab(basic_tab, "Basic Features")

        main_layout.addWidget(self.tab_widget)

        # Apply layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.setFocus()

    def create_static_settings_group(self):
        self.static_settings_group = QGroupBox("Static Settings")

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

        self.always_on_main_screen_checkbox = QCheckBox("Always on Main Screen")

        self.position_dropdown = QComboBox()
        self._populate_position_dropdown()
        self.position_dropdown.setCurrentIndex(2)
        self.position_dropdown.setFixedHeight(26)

        # Animation direction dropdown
        self.animation_direction_dropdown = QComboBox()
        self._populate_animation_direction_dropdown()
        self.animation_direction_dropdown.setFixedHeight(26)

        # Content margins controls
        self.content_left_spinbox = QSpinBox()
        self.content_left_spinbox.setRange(0, 100)
        self.content_left_spinbox.setValue(10)
        self.content_left_spinbox.setFixedHeight(24)

        self.content_top_spinbox = QSpinBox()
        self.content_top_spinbox.setRange(0, 100)
        self.content_top_spinbox.setValue(10)
        self.content_top_spinbox.setFixedHeight(24)

        self.content_right_spinbox = QSpinBox()
        self.content_right_spinbox.setRange(0, 100)
        self.content_right_spinbox.setValue(10)
        self.content_right_spinbox.setFixedHeight(24)

        self.content_bottom_spinbox = QSpinBox()
        self.content_bottom_spinbox.setRange(0, 100)
        self.content_bottom_spinbox.setValue(10)
        self.content_bottom_spinbox.setFixedHeight(24)

        # Icon margins controls
        self.icon_left_spinbox = QSpinBox()
        self.icon_left_spinbox.setRange(0, 50)
        self.icon_left_spinbox.setValue(5)
        self.icon_left_spinbox.setFixedHeight(24)

        self.icon_right_spinbox = QSpinBox()
        self.icon_right_spinbox.setRange(0, 50)
        self.icon_right_spinbox.setValue(5)
        self.icon_right_spinbox.setFixedHeight(24)

        self.update_button = QPushButton("Update Settings")
        self.update_button.setFixedHeight(32)
        self.update_button.clicked.connect(self.update_static_settings)

        # Store labels for later updates
        self.max_on_screen_label = QLabel("Max on Screen:")
        self.spacing_label = QLabel("Spacing:")
        self.x_offset_label = QLabel("X Offset:")
        self.y_offset_label = QLabel("Y Offset:")
        self.position_label = QLabel("Position:")
        self.animation_direction_label = QLabel("Animation Direction:")
        self.content_margins_label = QLabel("Content Margins:")
        self.icon_margins_label = QLabel("Icon Margins:")
        self.left_label = QLabel("Left:")
        self.top_label = QLabel("Top:")
        self.right_label = QLabel("Right:")
        self.bottom_label = QLabel("Bottom:")
        self.icon_left_label = QLabel("Left:")
        self.icon_right_label = QLabel("Right:")

        # Add widgets to layout
        form_layout = QFormLayout()
        form_layout.addRow(self.max_on_screen_label, self.maximum_on_screen_spinbox)
        form_layout.addRow(self.spacing_label, self.spacing_spinbox)
        form_layout.addRow(self.x_offset_label, self.offset_x_spinbox)
        form_layout.addRow(self.y_offset_label, self.offset_y_spinbox)
        form_layout.addRow(self.position_label, self.position_dropdown)
        form_layout.addRow(self.animation_direction_label, self.animation_direction_dropdown)

        # Add layout and widgets to main layout
        vbox_layout = QVBoxLayout()
        vbox_layout.addLayout(form_layout)
        vbox_layout.addWidget(self.always_on_main_screen_checkbox)

        # Content margins section
        vbox_layout.addWidget(self.content_margins_label)
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.left_label)
        content_layout.addWidget(self.content_left_spinbox)
        content_layout.addWidget(self.top_label)
        content_layout.addWidget(self.content_top_spinbox)
        content_layout.addWidget(self.right_label)
        content_layout.addWidget(self.content_right_spinbox)
        content_layout.addWidget(self.bottom_label)
        content_layout.addWidget(self.content_bottom_spinbox)
        vbox_layout.addLayout(content_layout)

        # Icon margins section
        vbox_layout.addWidget(self.icon_margins_label)
        icon_layout = QHBoxLayout()
        icon_layout.addWidget(self.icon_left_label)
        icon_layout.addWidget(self.icon_left_spinbox)
        icon_layout.addWidget(self.icon_right_label)
        icon_layout.addWidget(self.icon_right_spinbox)
        icon_layout.addStretch()
        vbox_layout.addLayout(icon_layout)

        vbox_layout.addWidget(self.update_button)
        vbox_layout.addStretch(1)
        self.static_settings_group.setLayout(vbox_layout)

        # Set minimum size to ensure complete display
        self.static_settings_group.setMinimumHeight(350)
        self.static_settings_group.setMinimumWidth(400)

        return self.static_settings_group

    def _populate_position_dropdown(self):
        """Populate position dropdown with English text."""
        self.position_dropdown.clear()
        positions = ["Bottom Left", "Bottom Middle", "Bottom Right", "Top Left", "Top Middle", "Top Right", "Center"]
        for pos in positions:
            self.position_dropdown.addItem(pos)

    def _populate_animation_direction_dropdown(self):
        """Populate animation direction dropdown with English text."""
        self.animation_direction_dropdown.clear()
        directions = ["Auto", "From Top", "From Bottom", "From Left", "From Right", "Fade Only"]
        for direction in directions:
            self.animation_direction_dropdown.addItem(direction)

    def create_toast_preset_group(self):
        self.toast_preset_group = QGroupBox("Toast Presets")

        # Create widgets
        self.preset_dropdown = QComboBox()
        self._populate_preset_dropdown()
        self.preset_dropdown.setFixedHeight(26)

        self.show_preset_toast_button = QPushButton("Show Preset Toast")
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
        """Populate preset dropdown with English text."""
        self.preset_dropdown.clear()
        presets = [
            "Success",
            "Warning",
            "Error",
            "Information",
            "Success (Dark)",
            "Warning (Dark)",
            "Error (Dark)",
            "Information (Dark)",
        ]
        for preset in presets:
            self.preset_dropdown.addItem(preset)

    def create_toast_custom_group(self):
        self.custom_toast_group = QGroupBox("Custom Toast")

        # Create widgets
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(0, 50000)
        self.duration_spinbox.setValue(5000)
        self.duration_spinbox.setFixedHeight(24)

        self.title_input = QLineEdit("This is a title")
        self.title_input.setFixedHeight(24)

        self.text_input = QLineEdit(
            "This is a much longer text that demonstrates multiline functionality. It should wrap properly when the multiline checkbox is enabled."
        )
        self.text_input.setFixedHeight(24)

        self.border_radius_spinbox = QSpinBox()
        self.border_radius_spinbox.setRange(0, 20)
        self.border_radius_spinbox.setValue(8)
        self.border_radius_spinbox.setFixedHeight(24)

        self.show_icon_checkbox = QCheckBox("Show Icon")

        self.icon_dropdown = QComboBox()
        self._populate_icon_dropdown()
        self.icon_dropdown.setFixedHeight(24)

        self.icon_size_spinbox = QSpinBox()
        self.icon_size_spinbox.setRange(5, 50)
        self.icon_size_spinbox.setValue(18)
        self.icon_size_spinbox.setFixedHeight(24)

        self.show_duration_bar_checkbox = QCheckBox("Show Duration Bar")
        self.show_duration_bar_checkbox.setChecked(True)

        self.reset_on_hover_checkbox = QCheckBox("Reset Duration on Hover")
        self.reset_on_hover_checkbox.setChecked(True)

        self.multiline_checkbox = QCheckBox("Multiline Text")
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
        self.small_font_button = QPushButton("Small Font")
        self.small_font_button.setFixedHeight(28)
        self.small_font_button.clicked.connect(self.set_small_font)

        self.medium_font_button = QPushButton("Medium Font")
        self.medium_font_button.setFixedHeight(28)
        self.medium_font_button.clicked.connect(self.set_medium_font)

        self.large_font_button = QPushButton("Large Font")
        self.large_font_button.setFixedHeight(28)
        self.large_font_button.clicked.connect(self.set_large_font)

        # Test buttons for font features
        self.test_links_button = QPushButton("Test Clickable Links")
        self.test_links_button.setFixedHeight(28)
        self.test_links_button.clicked.connect(self.test_clickable_links)

        # Color customization controls (moved from advanced tab)
        self.custom_background_color = QColor(231, 244, 249)  # Default light blue
        self.custom_title_color = QColor(0, 0, 0)  # Black
        self.custom_text_color = QColor(92, 92, 92)  # Gray
        self.custom_icon_color = QColor(0, 127, 255)  # Blue
        self.custom_duration_bar_color = QColor(0, 127, 255)  # Blue

        # Color buttons
        self.background_color_button = QPushButton()
        self.background_color_button.setFixedHeight(28)
        self.background_color_button.clicked.connect(lambda: self.choose_color('background'))
        self._update_color_button(self.background_color_button, self.custom_background_color)

        self.title_color_button = QPushButton()
        self.title_color_button.setFixedHeight(28)
        self.title_color_button.clicked.connect(lambda: self.choose_color('title'))
        self._update_color_button(self.title_color_button, self.custom_title_color)

        self.text_color_button = QPushButton()
        self.text_color_button.setFixedHeight(28)
        self.text_color_button.clicked.connect(lambda: self.choose_color('text'))
        self._update_color_button(self.text_color_button, self.custom_text_color)

        self.icon_color_button = QPushButton()
        self.icon_color_button.setFixedHeight(28)
        self.icon_color_button.clicked.connect(lambda: self.choose_color('icon'))
        self._update_color_button(self.icon_color_button, self.custom_icon_color)

        self.duration_bar_color_button = QPushButton()
        self.duration_bar_color_button.setFixedHeight(28)
        self.duration_bar_color_button.clicked.connect(lambda: self.choose_color('duration_bar'))
        self._update_color_button(self.duration_bar_color_button, self.custom_duration_bar_color)

        # Reset colors button
        self.reset_colors_button = QPushButton("Reset Colors")
        self.reset_colors_button.setFixedHeight(28)
        self.reset_colors_button.clicked.connect(self.reset_colors)

        # Advanced features controls (moved from advanced tab)
        self.stay_on_top_checkbox = QCheckBox("Stay on Top")
        self.stay_on_top_checkbox.setChecked(True)  # Default to checked since Toast defaults to stay on top

        self.icon_separator_checkbox = QCheckBox("Icon Separator")
        self.icon_separator_checkbox.setChecked(True)

        self.separator_width_spinbox = QSpinBox()
        self.separator_width_spinbox.setRange(1, 10)
        self.separator_width_spinbox.setValue(2)
        self.separator_width_spinbox.setFixedHeight(24)

        # Separator color
        self.separator_color = QColor(217, 217, 217)  # Default gray
        self.separator_color_button = QPushButton()
        self.separator_color_button.setFixedHeight(28)
        self.separator_color_button.clicked.connect(lambda: self.choose_color('separator'))
        self._update_color_button(self.separator_color_button, self.separator_color)

        # Close button color
        self.close_button_color = QColor(0, 0, 0)  # Default black
        self.close_button_color_button = QPushButton()
        self.close_button_color_button.setFixedHeight(28)
        self.close_button_color_button.clicked.connect(lambda: self.choose_color('close_button'))
        self._update_color_button(self.close_button_color_button, self.close_button_color)

        # Demo buttons for advanced features (moved from advanced tab)
        self.test_callbacks_button = QPushButton("Test Callbacks")
        self.test_callbacks_button.setFixedHeight(28)
        self.test_callbacks_button.clicked.connect(self.test_callbacks)

        self.show_multiple_button = QPushButton("Show Multiple")
        self.show_multiple_button.setFixedHeight(28)
        self.show_multiple_button.clicked.connect(self.show_multiple_toasts)

        self.queue_demo_button = QPushButton("Queue Demo")
        self.queue_demo_button.setFixedHeight(28)
        self.queue_demo_button.clicked.connect(self.queue_demo)

        self.custom_toast_button = QPushButton("Show Custom Toast")
        self.custom_toast_button.setFixedHeight(32)
        self.custom_toast_button.clicked.connect(self.show_custom_toast)

        # Store labels for later updates
        self.duration_label = QLabel("Duration:")
        self.title_label = QLabel("Title:")
        self.text_label = QLabel("Text:")
        self.icon_size_label = QLabel("Icon Size:")
        self.border_radius_label = QLabel("Border Radius:")
        self.close_button_label = QLabel("Close Button:")
        self.min_width_label = QLabel("Min Width:")
        self.max_width_label = QLabel("Max Width:")
        self.min_height_label = QLabel("Min Height:")
        self.max_height_label = QLabel("Max Height:")
        self.fade_in_label = QLabel("Fade In Duration:")
        self.fade_out_label = QLabel("Fade Out Duration:")

        # Font customization labels
        self.title_font_size_label = QLabel("Title Font Size:")
        self.text_font_size_label = QLabel("Text Font Size:")
        self.font_family_label = QLabel("Font Family:")
        self.font_presets_label = QLabel("Font Presets:")

        # Color customization labels (moved from advanced tab)
        self.background_color_label = QLabel("Background Color:")
        self.title_color_label = QLabel("Title Color:")
        self.text_color_label = QLabel("Text Color:")
        self.icon_color_label = QLabel("Icon Color:")
        self.duration_bar_color_label = QLabel("Duration Bar Color:")

        # Advanced features labels (moved from advanced tab)
        self.separator_width_label = QLabel("Separator Width:")
        self.separator_color_label = QLabel("Separator Color:")
        self.close_button_color_label = QLabel("Close Button Color:")

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

        # Color customization layouts (moved from advanced tab)
        color_form_layout = QFormLayout()
        color_form_layout.addRow(self.background_color_label, self.background_color_button)
        color_form_layout.addRow(self.title_color_label, self.title_color_button)
        color_form_layout.addRow(self.text_color_label, self.text_color_button)
        color_form_layout.addRow(self.icon_color_label, self.icon_color_button)
        color_form_layout.addRow(self.duration_bar_color_label, self.duration_bar_color_button)

        # Advanced features layouts (moved from advanced tab)
        advanced_checkbox_layout = QHBoxLayout()
        advanced_checkbox_layout.addWidget(self.stay_on_top_checkbox)
        advanced_checkbox_layout.addWidget(self.icon_separator_checkbox)

        # Separator settings
        separator_layout = QHBoxLayout()
        separator_layout.addWidget(self.separator_width_label)
        separator_layout.addWidget(self.separator_width_spinbox)
        separator_layout.addStretch()

        # Additional color settings
        additional_color_layout = QFormLayout()
        additional_color_layout.addRow(self.separator_color_label, self.separator_color_button)
        additional_color_layout.addRow(self.close_button_color_label, self.close_button_color_button)

        # Action buttons layout - organized in rows
        action_buttons_layout_1 = QHBoxLayout()
        action_buttons_layout_1.addWidget(self.test_links_button)
        action_buttons_layout_1.addWidget(self.reset_colors_button)
        action_buttons_layout_1.addWidget(self.custom_toast_button)

        action_buttons_layout_2 = QHBoxLayout()
        action_buttons_layout_2.addWidget(self.test_callbacks_button)
        action_buttons_layout_2.addWidget(self.show_multiple_button)
        action_buttons_layout_2.addWidget(self.queue_demo_button)

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

        # Add color customization section
        vbox_layout.addLayout(color_form_layout)

        # Add advanced features section
        vbox_layout.addLayout(advanced_checkbox_layout)
        vbox_layout.addLayout(separator_layout)
        vbox_layout.addLayout(additional_color_layout)

        vbox_layout.addLayout(action_buttons_layout_1)
        vbox_layout.addLayout(action_buttons_layout_2)
        vbox_layout.addStretch(1)
        self.custom_toast_group.setLayout(vbox_layout)

        # Set minimum size to ensure complete display (increased for new content)
        self.custom_toast_group.setMinimumHeight(800)
        self.custom_toast_group.setMinimumWidth(500)

        return self.custom_toast_group

    def _update_color_button(self, button, color):
        """Update color button appearance."""
        button.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
        button.setText(color.name().upper())

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

        # Apply color customizations (moved from advanced tab)
        toast.setBackgroundColor(self.custom_background_color)
        toast.setTitleColor(self.custom_title_color)
        toast.setTextColor(self.custom_text_color)
        toast.setIconColor(self.custom_icon_color)
        toast.setDurationBarColor(self.custom_duration_bar_color)

        # Apply advanced settings (moved from advanced tab)
        toast.setStayOnTop(self.stay_on_top_checkbox.isChecked())
        toast.setShowIconSeparator(self.icon_separator_checkbox.isChecked())
        toast.setIconSeparatorWidth(self.separator_width_spinbox.value())
        toast.setIconSeparatorColor(self.separator_color)
        toast.setCloseButtonIconColor(self.close_button_color)

    def _populate_icon_dropdown(self):
        """Populate icon dropdown with English text."""
        self.icon_dropdown.clear()
        icons = ["Success", "Warning", "Error", "Information", "Close"]
        for icon in icons:
            self.icon_dropdown.addItem(icon)

    def _populate_close_button_dropdown(self):
        """Populate close button dropdown with English text."""
        self.close_button_settings_dropdown.clear()
        positions = ["Top", "Middle", "Bottom", "Disabled"]
        for pos in positions:
            self.close_button_settings_dropdown.addItem(pos)

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

        # Show a test toast with the updated settings including animation and margins
        self.test_static_settings_toast()

    def test_static_settings_toast(self):
        """Test toast with updated static settings, animation direction, and margins."""
        toast = Toast(self)
        toast.setDuration(4000)
        toast.setTitle("Static Settings")
        toast.setText("Settings updated! This toast demonstrates the new static settings, animation direction, and custom margins.")

        # Apply animation direction from static settings
        direction_index = self.animation_direction_dropdown.currentIndex()
        direction_map = [
            ToastAnimationDirection.AUTO,
            ToastAnimationDirection.FROM_TOP,
            ToastAnimationDirection.FROM_BOTTOM,
            ToastAnimationDirection.FROM_LEFT,
            ToastAnimationDirection.FROM_RIGHT,
            ToastAnimationDirection.FADE_ONLY,
        ]

        if 0 <= direction_index < len(direction_map):
            toast.setAnimationDirection(direction_map[direction_index])

        # Apply content margins from static settings
        content_margins = (
            self.content_left_spinbox.value(),
            self.content_top_spinbox.value(),
            self.content_right_spinbox.value(),
            self.content_bottom_spinbox.value()
        )
        toast.setMargins(content_margins, 'content')

        # Apply icon margins from static settings
        icon_margins = {
            'left': self.icon_left_spinbox.value(),
            'right': self.icon_right_spinbox.value()
        }
        toast.setMargins(icon_margins, 'icon')

        # Apply other custom settings if available
        self._apply_custom_toast_settings(toast)
        toast.applyPreset(ToastPreset.SUCCESS)
        toast.show()

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
                "Success! Confirmation email sent.",
                "Please check your email to complete registration.",
                ToastPreset.SUCCESS,
            ),
            # warning
            (
                "Warning! Passwords do not match.",
                "Please confirm your password again.",
                ToastPreset.WARNING,
            ),
            # error
            (
                "Error! Unable to complete request.",
                "Please try again in a few minutes.",
                ToastPreset.ERROR,
            ),
            # information
            (
                "Information: Restart required.",
                "Please restart the application.",
                ToastPreset.INFORMATION,
            ),
            # success_dark
            (
                "Success! Confirmation email sent.",
                "Please check your email to complete registration.",
                ToastPreset.SUCCESS_DARK,
            ),
            # warning_dark
            (
                "Warning! Passwords do not match.",
                "Please confirm your password again.",
                ToastPreset.WARNING_DARK,
            ),
            # error_dark
            (
                "Error! Unable to complete request.",
                "Please try again in a few minutes.",
                ToastPreset.ERROR_DARK,
            ),
            # information_dark
            (
                "Information: Restart required.",
                "Please restart the application.",
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
        toast.setTitle("Clickable Links Test")
        toast.setText("Click to test: https://www.google.com and www.github.com are clickable links!")

        # Apply all custom toast settings using the helper method
        self._apply_custom_toast_settings(toast)

        # Use Information preset as default for link testing
        toast.applyPreset(ToastPreset.INFORMATION)
        toast.show()

    def choose_color(self, color_type):
        """Open color dialog and update the selected color."""
        current_color = None
        if color_type == 'background':
            current_color = self.custom_background_color
        elif color_type == 'title':
            current_color = self.custom_title_color
        elif color_type == 'text':
            current_color = self.custom_text_color
        elif color_type == 'icon':
            current_color = self.custom_icon_color
        elif color_type == 'duration_bar':
            current_color = self.custom_duration_bar_color
        elif color_type == 'separator':
            current_color = self.separator_color
        elif color_type == 'close_button':
            current_color = self.close_button_color

        color = QColorDialog.getColor(current_color, self, "Choose Color")

        if color.isValid():
            if color_type == 'background':
                self.custom_background_color = color
                self._update_color_button(self.background_color_button, color)
            elif color_type == 'title':
                self.custom_title_color = color
                self._update_color_button(self.title_color_button, color)
            elif color_type == 'text':
                self.custom_text_color = color
                self._update_color_button(self.text_color_button, color)
            elif color_type == 'icon':
                self.custom_icon_color = color
                self._update_color_button(self.icon_color_button, color)
            elif color_type == 'duration_bar':
                self.custom_duration_bar_color = color
                self._update_color_button(self.duration_bar_color_button, color)
            elif color_type == 'separator':
                self.separator_color = color
                self._update_color_button(self.separator_color_button, color)
            elif color_type == 'close_button':
                self.close_button_color = color
                self._update_color_button(self.close_button_color_button, color)

    def reset_colors(self):
        """Reset all colors to defaults."""
        self.custom_background_color = QColor(231, 244, 249)
        self.custom_title_color = QColor(0, 0, 0)
        self.custom_text_color = QColor(92, 92, 92)
        self.custom_icon_color = QColor(0, 127, 255)
        self.custom_duration_bar_color = QColor(0, 127, 255)
        self.separator_color = QColor(217, 217, 217)
        self.close_button_color = QColor(0, 0, 0)

        # Update button appearances
        self._update_color_button(self.background_color_button, self.custom_background_color)
        self._update_color_button(self.title_color_button, self.custom_title_color)
        self._update_color_button(self.text_color_button, self.custom_text_color)
        self._update_color_button(self.icon_color_button, self.custom_icon_color)
        self._update_color_button(self.duration_bar_color_button, self.custom_duration_bar_color)
        self._update_color_button(self.separator_color_button, self.separator_color)
        self._update_color_button(self.close_button_color_button, self.close_button_color)

    def test_custom_colors(self):
        """Test toast with custom colors."""
        toast = Toast(self)
        toast.setDuration(self.duration_spinbox.value())
        toast.setTitle("This is a title")
        toast.setText("Click to test: https://www.google.com and www.github.com are clickable links!")

        # Apply custom colors
        toast.setBackgroundColor(self.custom_background_color)
        toast.setTitleColor(self.custom_title_color)
        toast.setTextColor(self.custom_text_color)
        toast.setIconColor(self.custom_icon_color)
        toast.setDurationBarColor(self.custom_duration_bar_color)

        # Apply other custom settings
        self._apply_custom_toast_settings(toast)

        toast.show()

    def test_animation_direction(self):
        """Test toast with selected animation direction."""
        toast = Toast(self)
        toast.setDuration(3000)
        toast.setTitle("Test Animation")

        # Get selected animation direction
        direction_index = self.animation_direction_dropdown.currentIndex()
        direction_map = [
            ToastAnimationDirection.AUTO,
            ToastAnimationDirection.FROM_TOP,
            ToastAnimationDirection.FROM_BOTTOM,
            ToastAnimationDirection.FROM_LEFT,
            ToastAnimationDirection.FROM_RIGHT,
            ToastAnimationDirection.FADE_ONLY,
        ]

        if 0 <= direction_index < len(direction_map):
            direction = direction_map[direction_index]
            toast.setAnimationDirection(direction)
            direction_name = self.animation_direction_dropdown.currentText()
            toast.setText(f"Animation Direction: {direction_name}")

        # Apply custom settings
        self._apply_custom_toast_settings(toast)
        toast.applyPreset(ToastPreset.SUCCESS)
        toast.show()

    def test_margins_demo(self):
        """Test toast with custom margins."""
        toast = Toast(self)
        toast.setDuration(4000)
        toast.setTitle("Margins Settings")
        toast.setText("This toast demonstrates custom margin settings using the modern margins API.")

        # Apply content margins using modern API
        content_margins = (
            self.content_left_spinbox.value(),
            self.content_top_spinbox.value(),
            self.content_right_spinbox.value(),
            self.content_bottom_spinbox.value()
        )
        toast.setMargins(content_margins, 'content')

        # Apply icon margins
        icon_margins = {
            'left': self.icon_left_spinbox.value(),
            'right': self.icon_right_spinbox.value()
        }
        toast.setMargins(icon_margins, 'icon')

        # Apply other custom settings
        self._apply_custom_toast_settings(toast)
        toast.applyPreset(ToastPreset.INFORMATION)
        toast.show()

    def test_callbacks(self):
        """Test toast with callback events and print callback records to console."""
        print("=== Toast Callbacks Test Started ===")

        toast = Toast(self)
        toast.setDuration(3000)
        toast.setTitle("Test Callbacks")
        toast.setText("This toast will show a message when it closes.")

        # Connect to closed signal with console logging
        toast.closed.connect(lambda: self.show_callback_message())

        # Print callback registration
        print(f"[CALLBACK] Registered 'closed' callback for toast: '{toast.getTitle()}'")

        # Apply advanced settings
        toast.setStayOnTop(self.stay_on_top_checkbox.isChecked())
        toast.setShowIconSeparator(self.icon_separator_checkbox.isChecked())
        toast.setIconSeparatorWidth(self.separator_width_spinbox.value())
        toast.setIconSeparatorColor(self.separator_color)
        toast.setCloseButtonIconColor(self.close_button_color)

        # Apply other custom settings
        self._apply_custom_toast_settings(toast)
        toast.applyPreset(ToastPreset.WARNING)

        print(f"[TOAST] Showing toast with title: '{toast.getTitle()}'")
        print(f"[TOAST] Duration: {toast.getDuration()}ms")
        toast.show()

    def show_callback_message(self):
        """Show a simple message when callback is triggered and log to console."""
        print("[CALLBACK] Toast 'closed' callback triggered!")
        print("[CALLBACK] Previous toast was closed by user or timeout")

        callback_toast = Toast(self)
        callback_toast.setDuration(2000)
        callback_toast.setTitle("Callback Event")
        callback_toast.setText("Previous toast was closed!")
        callback_toast.applyPreset(ToastPreset.SUCCESS)

        print(f"[CALLBACK] Showing callback toast: '{callback_toast.getTitle()}'")
        callback_toast.show()
        print("=== Toast Callbacks Test Completed ===")

    def show_multiple_toasts(self):
        """Show multiple toasts to demonstrate stacking."""
        presets = [ToastPreset.SUCCESS, ToastPreset.WARNING, ToastPreset.ERROR, ToastPreset.INFORMATION]
        titles = [
            "Success! Confirmation email sent.",
            "Warning! Passwords do not match.",
            "Error! Unable to complete request.",
            "Information: Restart required."
        ]

        for i in range(4):
            toast = Toast(self)
            toast.setDuration(5000)
            toast.setTitle(f"{i+1}. {titles[i]}")
            toast.setText(f"Multiple toast demonstration #{i+1}")

            # Apply advanced settings
            toast.setStayOnTop(self.stay_on_top_checkbox.isChecked())
            toast.setShowIconSeparator(self.icon_separator_checkbox.isChecked())
            toast.setIconSeparatorWidth(self.separator_width_spinbox.value())
            toast.setIconSeparatorColor(self.separator_color)
            toast.setCloseButtonIconColor(self.close_button_color)

            # Apply animation direction
            direction_index = self.animation_direction_dropdown.currentIndex()
            direction_map = [
                ToastAnimationDirection.AUTO,
                ToastAnimationDirection.FROM_TOP,
                ToastAnimationDirection.FROM_BOTTOM,
                ToastAnimationDirection.FROM_LEFT,
                ToastAnimationDirection.FROM_RIGHT,
                ToastAnimationDirection.FADE_ONLY,
            ]
            if 0 <= direction_index < len(direction_map):
                toast.setAnimationDirection(direction_map[direction_index])

            toast.applyPreset(presets[i])
            toast.show()

    def queue_demo(self):
        """Demonstrate queue management by showing many toasts."""
        # Set maximum on screen to 2 for demonstration
        original_max = Toast.getMaximumOnScreen()
        Toast.setMaximumOnScreen(2)

        for i in range(6):
            toast = Toast(self)
            toast.setDuration(3000)
            toast.setTitle(f"Queue Demo {i+1}")
            toast.setText(f"This is toast #{i+1} in the queue demonstration. Only 2 will show at once.")

            # Apply advanced settings
            toast.setStayOnTop(self.stay_on_top_checkbox.isChecked())

            # Alternate between presets
            presets = [ToastPreset.SUCCESS, ToastPreset.WARNING]
            toast.applyPreset(presets[i % 2])
            toast.show()

        # Restore original maximum after a delay
        QTimer.singleShot(10000, lambda: Toast.setMaximumOnScreen(original_max))
