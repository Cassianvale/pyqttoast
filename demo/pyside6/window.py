import random
import logging
import time
from enum import Enum
from typing import Dict, Optional, List, Callable, Any, Union
from dataclasses import dataclass, field
from contextlib import contextmanager

from PySide6.QtCore import Qt, QSize, QTimer, Signal, QObject
from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QCheckBox,
    QWidget,
    QGroupBox,
    QGridLayout,
    QSpinBox,
    QLineEdit,
    QHBoxLayout,
    QLabel,
    QFormLayout,
    QSlider,
    QMessageBox,
    QProgressBar,
    QRadioButton,
    QButtonGroup,
)
from PySide6.QtGui import QColor

from pyqttoast import Toast, ToastPreset, ToastIcon, ToastPosition, ToastButtonAlignment
from language_manager import LanguageManager
import uuid

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class TaskStatus(Enum):
    """Task status enumeration for better type safety."""

    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProgressMode(Enum):
    """Progress mode enumeration for task control."""

    MANUAL = "manual"  # User controls progress manually
    AUTOMATIC = "automatic"  # Progress advances automatically


@dataclass
class ProgressTask:
    """
    Enhanced progress task data class with comprehensive state management.

    This class represents a single progress task with full lifecycle support,
    progress mode control, error handling, and performance tracking.
    """

    task_id: str
    name: str
    progress: float = 0.0  # 0.0 to 1.0
    toast: Optional[Toast] = None
    timer: Optional[QTimer] = None
    status: TaskStatus = TaskStatus.CREATED
    progress_mode: ProgressMode = ProgressMode.MANUAL
    is_auto_running: bool = False
    created_time: float = field(default_factory=time.time)
    start_time: Optional[float] = None
    completion_time: Optional[float] = None
    error_message: Optional[str] = None
    update_count: int = 0
    auto_progress_interval: int = 100  # milliseconds for automatic progress
    auto_progress_increment_range: tuple[float, float] = (0.005, 0.02)  # 0.5% to 2%

    @property
    def is_completed(self) -> bool:
        """Check if task is completed."""
        return self.status == TaskStatus.COMPLETED

    @property
    def is_running(self) -> bool:
        """Check if task is currently running."""
        return self.status == TaskStatus.RUNNING

    @property
    def is_manual_mode(self) -> bool:
        """Check if task is in manual progress mode."""
        return self.progress_mode == ProgressMode.MANUAL

    @property
    def is_automatic_mode(self) -> bool:
        """Check if task is in automatic progress mode."""
        return self.progress_mode == ProgressMode.AUTOMATIC

    @property
    def duration(self) -> Optional[float]:
        """Get task duration in seconds."""
        if self.start_time is None:
            return None
        end_time = self.completion_time or time.time()
        return end_time - self.start_time

    @property
    def progress_percentage(self) -> int:
        """Get progress as percentage (0-100)."""
        return int(self.progress * 100)

    def get_display_name(self) -> str:
        """Get formatted display name with status and progress."""
        mode_icon = "🎛️" if self.is_manual_mode else "🤖"
        status_icon = self._get_status_icon()
        return f"{mode_icon}{status_icon} {self.name} ({self.progress_percentage}%)"

    def _get_status_icon(self) -> str:
        """Get appropriate status icon for task."""
        if self.is_auto_running:
            return "🔄"
        elif self.status == TaskStatus.RUNNING:
            return "▶️"
        elif self.status == TaskStatus.PAUSED:
            return "⏸️"
        elif self.status == TaskStatus.COMPLETED:
            return "✅"
        elif self.status == TaskStatus.CANCELLED:
            return "❌"
        elif self.status == TaskStatus.FAILED:
            return "💥"
        else:
            return "⏹️"


class ProgressManager(QObject):
    """
    Enhanced multi-progress task manager with comprehensive error handling,
    performance optimization, and support for both manual and automatic progress modes.
    """

    # Signals for better event handling
    taskCreated = Signal(str)  # task_id
    taskUpdated = Signal(str, float)  # task_id, progress
    taskCompleted = Signal(str)  # task_id
    taskFailed = Signal(str, str)  # task_id, error_message
    taskModeChanged = Signal(str, str)  # task_id, new_mode
    allTasksCompleted = Signal()

    def __init__(self):
        super().__init__()
        self.tasks: Dict[str, ProgressTask] = {}
        self.active_toasts: Dict[str, Toast] = {}
        self.task_counter: int = 0
        self._update_batch_size: int = 10  # Performance optimization
        self._last_cleanup_time: float = time.time()
        self._cleanup_interval: float = 30.0  # seconds

        # Setup periodic cleanup timer
        self._cleanup_timer = QTimer()
        self._cleanup_timer.timeout.connect(self._periodic_cleanup)
        self._cleanup_timer.start(int(self._cleanup_interval * 1000))

    def create_task(
        self, name: Optional[str] = None, progress_mode: ProgressMode = ProgressMode.MANUAL, auto_start: bool = False
    ) -> str:
        """
        Create a new progress task with enhanced error handling and mode support.

        Args:
            name: Task name. If None, generates a default name.
            progress_mode: Whether task uses manual or automatic progress
            auto_start: Whether to automatically start the task.

        Returns:
            Task ID string

        Raises:
            ValueError: If task creation fails
        """
        try:
            self.task_counter += 1
            task_id = str(uuid.uuid4())[:8]
            task_name = name or f"Task {self.task_counter}"

            task = ProgressTask(task_id=task_id, name=task_name, progress_mode=progress_mode)

            if auto_start:
                task.status = TaskStatus.RUNNING
                task.start_time = time.time()

            self.tasks[task_id] = task
            self.taskCreated.emit(task_id)

            logging.info(f"Created {progress_mode.value} task: {task_name} (ID: {task_id})")
            return task_id

        except Exception as e:
            logging.error(f"Failed to create task: {e}")
            raise ValueError(f"Task creation failed: {e}")

    def get_task(self, task_id: str) -> Optional[ProgressTask]:
        """
        Get task by ID with error handling.

        Args:
            task_id: Task identifier

        Returns:
            ProgressTask instance or None if not found
        """
        return self.tasks.get(task_id)

    def set_task_mode(self, task_id: str, progress_mode: ProgressMode) -> bool:
        """
        Change the progress mode of an existing task.

        Args:
            task_id: Task identifier
            progress_mode: New progress mode

        Returns:
            True if mode was changed successfully, False otherwise
        """
        try:
            task = self.get_task(task_id)
            if not task:
                logging.warning(f"Task {task_id} not found for mode change")
                return False

            if task.is_completed:
                logging.warning(f"Cannot change mode of completed task {task_id}")
                return False

            old_mode = task.progress_mode
            task.progress_mode = progress_mode

            # Stop automatic progress if switching to manual
            if progress_mode == ProgressMode.MANUAL and task.is_auto_running:
                self._stop_auto_progress(task_id)

            # Start automatic progress if switching to automatic and task is running
            elif progress_mode == ProgressMode.AUTOMATIC and task.is_running:
                self._start_auto_progress(task_id)

            self.taskModeChanged.emit(task_id, progress_mode.value)
            logging.info(f"Changed task {task_id} mode from {old_mode.value} to {progress_mode.value}")
            return True

        except Exception as e:
            logging.error(f"Failed to change task mode for {task_id}: {e}")
            return False

    def is_manual_mode(self, task_id: str) -> bool:
        """Check if task is in manual mode."""
        task = self.get_task(task_id)
        return task.is_manual_mode if task else False

    def is_auto_mode(self, task_id: str) -> bool:
        """Check if task is in automatic mode."""
        task = self.get_task(task_id)
        return task.is_automatic_mode if task else False

    def update_progress(
        self, task_id: str, progress: Union[int, float], animated: bool = True, force: bool = False
    ) -> bool:
        """
        Update task progress with comprehensive validation and mode checking.

        Args:
            task_id: Task identifier
            progress: Progress value (0.0 to 1.0)
            animated: Whether to animate the progress change
            force: Force update even for automatic mode tasks

        Returns:
            True if update was successful, False otherwise
        """
        try:
            task = self.get_task(task_id)
            if not task:
                logging.warning(f"Task {task_id} not found for progress update")
                return False

            # Validate mode - only allow manual updates for manual mode tasks
            if not force and task.is_automatic_mode:
                logging.warning(f"Cannot manually update automatic mode task {task_id}")
                return False

            # Validate and clamp progress value
            old_progress = task.progress
            task.progress = max(0.0, min(1.0, float(progress)))
            task.update_count += 1

            # Update task status
            if task.status == TaskStatus.CREATED and task.progress > 0:
                task.status = TaskStatus.RUNNING
                task.start_time = time.time()

            # Update toast if available
            if task.toast:
                try:
                    if hasattr(task.toast, "setProgress"):
                        task.toast.setProgress(task.progress, animated)
                    else:
                        task.toast.setDurationBarValue(task.progress)
                except Exception as e:
                    logging.error(f"Failed to update toast progress for task {task_id}: {e}")

            # Emit progress update signal
            if abs(old_progress - task.progress) > 0.001:
                self.taskUpdated.emit(task_id, task.progress)

            # Check for completion
            if task.progress >= 1.0 and not task.is_completed:
                self.complete_task(task_id)

            return True

        except Exception as e:
            logging.error(f"Failed to update progress for task {task_id}: {e}")
            self._handle_task_error(task_id, str(e))
            return False

    def _start_auto_progress(self, task_id: str) -> bool:
        """
        Start automatic progress for a task.

        Args:
            task_id: Task identifier

        Returns:
            True if auto progress was started successfully
        """
        try:
            task = self.get_task(task_id)
            if not task or task.is_completed:
                return False

            if not task.is_automatic_mode:
                logging.warning(f"Cannot start auto progress for manual mode task {task_id}")
                return False

            if task.is_auto_running:
                logging.info(f"Auto progress already running for task {task_id}")
                return True

            # Create and configure timer
            timer = QTimer()
            timer.timeout.connect(lambda: self._update_auto_progress(task_id))

            # Set task state
            task.timer = timer
            task.is_auto_running = True
            task.status = TaskStatus.RUNNING
            if task.start_time is None:
                task.start_time = time.time()

            # Start timer with task-specific interval
            timer.start(task.auto_progress_interval)

            logging.info(f"Started auto progress for task {task.name}")
            return True

        except Exception as e:
            logging.error(f"Failed to start auto progress for task {task_id}: {e}")
            return False

    def _stop_auto_progress(self, task_id: str) -> bool:
        """
        Stop automatic progress for a task.

        Args:
            task_id: Task identifier

        Returns:
            True if auto progress was stopped successfully
        """
        try:
            task = self.get_task(task_id)
            if not task:
                return False

            if task.timer:
                task.timer.stop()
                task.timer = None

            task.is_auto_running = False

            logging.info(f"Stopped auto progress for task {task.name}")
            return True

        except Exception as e:
            logging.error(f"Failed to stop auto progress for task {task_id}: {e}")
            return False

    def _update_auto_progress(self, task_id: str) -> None:
        """
        Automatic progress update callback with realistic simulation.

        Args:
            task_id: Task identifier
        """
        try:
            task = self.get_task(task_id)
            if not task or task.is_completed or not task.is_auto_running:
                return

            # Generate realistic progress increment
            min_inc, max_inc = task.auto_progress_increment_range
            increment = random.uniform(min_inc, max_inc)

            # Add some variability - occasionally pause or speed up
            rand_factor = random.random()
            if rand_factor < 0.05:  # 5% chance to pause briefly
                increment = 0
            elif rand_factor > 0.95:  # 5% chance to speed up
                increment *= 2

            new_progress = min(1.0, task.progress + increment)

            # Force update since this is automatic progress
            self.update_progress(task_id, new_progress, animated=True, force=True)

        except Exception as e:
            logging.error(f"Error in auto progress update for task {task_id}: {e}")
            self._handle_task_error(task_id, str(e))

    def start_auto_progress_for_task(self, task_id: str) -> bool:
        """Public method to start automatic progress for a specific task."""
        return self._start_auto_progress(task_id)

    def stop_auto_progress_for_task(self, task_id: str) -> bool:
        """Public method to stop automatic progress for a specific task."""
        return self._stop_auto_progress(task_id)

    def start_auto_progress_for_all(self) -> int:
        """
        Start automatic progress for all automatic mode tasks.

        Returns:
            Number of tasks that started auto progress
        """
        started_count = 0
        for task_id, task in self.tasks.items():
            if task.is_automatic_mode and not task.is_completed and not task.is_auto_running:
                if self._start_auto_progress(task_id):
                    started_count += 1

        logging.info(f"Started auto progress for {started_count} tasks")
        return started_count

    def stop_auto_progress_for_all(self) -> int:
        """
        Stop automatic progress for all running automatic tasks.

        Returns:
            Number of tasks that stopped auto progress
        """
        stopped_count = 0
        for task_id, task in self.tasks.items():
            if task.is_auto_running:
                if self._stop_auto_progress(task_id):
                    stopped_count += 1

        logging.info(f"Stopped auto progress for {stopped_count} tasks")
        return stopped_count

    def complete_task(self, task_id: str) -> bool:
        """
        Mark task as completed with enhanced feedback and cleanup.

        Args:
            task_id: Task identifier

        Returns:
            True if completion was successful, False otherwise
        """
        try:
            task = self.get_task(task_id)
            if not task:
                logging.warning(f"Task {task_id} not found for completion")
                return False

            if task.is_completed:
                logging.info(f"Task {task_id} already completed")
                return True

            # Update task state
            task.status = TaskStatus.COMPLETED
            task.progress = 1.0
            task.completion_time = time.time()
            task.is_auto_running = False

            # Stop any running timers
            if task.timer:
                task.timer.stop()
                task.timer = None

            # Update toast with completion feedback
            if task.toast:
                try:
                    task.toast.setTitle(f"✅ {task.name} - Completed!")
                    task.toast.setText("Task completed successfully")
                    if hasattr(task.toast, "setProgress"):
                        task.toast.setProgress(1.0, animated=True)
                    else:
                        task.toast.setDurationBarValue(1.0)
                    task.toast.applyPreset(ToastPreset.SUCCESS)

                    # Auto-hide completed toast after delay
                    QTimer.singleShot(3000, task.toast.hide)

                except Exception as e:
                    logging.error(f"Failed to update completion toast for task {task_id}: {e}")

            # Emit completion signal
            self.taskCompleted.emit(task_id)

            # Check if all tasks are completed
            if self._all_tasks_completed():
                self.allTasksCompleted.emit()

            logging.info(f"Task {task.name} (ID: {task_id}) completed in {task.duration:.2f}s")
            return True

        except Exception as e:
            logging.error(f"Failed to complete task {task_id}: {e}")
            self._handle_task_error(task_id, str(e))
            return False

    def remove_task(self, task_id: str) -> bool:
        """
        Remove task with proper cleanup and resource management.

        Args:
            task_id: Task identifier

        Returns:
            True if removal was successful, False otherwise
        """
        try:
            task = self.get_task(task_id)
            if not task:
                logging.warning(f"Task {task_id} not found for removal")
                return False

            # Stop any running operations
            if task.timer:
                task.timer.stop()
                task.timer = None

            # Hide and cleanup toast
            if task.toast:
                try:
                    task.toast.hide()
                    task.toast = None
                except Exception as e:
                    logging.error(f"Failed to hide toast for task {task_id}: {e}")

            # Remove from collections
            if task_id in self.active_toasts:
                del self.active_toasts[task_id]

            del self.tasks[task_id]

            logging.info(f"Removed task: {task.name} (ID: {task_id})")
            return True

        except Exception as e:
            logging.error(f"Failed to remove task {task_id}: {e}")
            return False

    def get_active_tasks(self) -> Dict[str, ProgressTask]:
        """Get all active (non-completed) tasks."""
        return {tid: task for tid, task in self.tasks.items() if not task.is_completed}

    def get_completed_tasks(self) -> Dict[str, ProgressTask]:
        """Get all completed tasks."""
        return {tid: task for tid, task in self.tasks.items() if task.is_completed}

    def get_manual_tasks(self) -> Dict[str, ProgressTask]:
        """Get all manual mode tasks."""
        return {tid: task for tid, task in self.tasks.items() if task.is_manual_mode}

    def get_automatic_tasks(self) -> Dict[str, ProgressTask]:
        """Get all automatic mode tasks."""
        return {tid: task for tid, task in self.tasks.items() if task.is_automatic_mode}

    def clear_completed(self) -> int:
        """
        Clear all completed tasks with proper cleanup.

        Returns:
            Number of tasks cleared
        """
        completed_ids = list(self.get_completed_tasks().keys())
        cleared_count = 0

        for task_id in completed_ids:
            if self.remove_task(task_id):
                cleared_count += 1

        logging.info(f"Cleared {cleared_count} completed tasks")
        return cleared_count

    def _handle_task_error(self, task_id: str, error_message: str) -> None:
        """Handle task errors with proper logging and user feedback."""
        task = self.get_task(task_id)
        if task:
            task.status = TaskStatus.FAILED
            task.error_message = error_message
            task.is_auto_running = False

            if task.timer:
                task.timer.stop()

            if task.toast:
                task.toast.setTitle(f"❌ {task.name} - Error")
                task.toast.setText(f"Error: {error_message}")
                task.toast.applyPreset(ToastPreset.ERROR)

            self.taskFailed.emit(task_id, error_message)

    def _all_tasks_completed(self) -> bool:
        """Check if all tasks are completed."""
        return len(self.get_active_tasks()) == 0

    def _periodic_cleanup(self) -> None:
        """Perform periodic cleanup of old completed tasks."""
        current_time = time.time()
        if current_time - self._last_cleanup_time < self._cleanup_interval:
            return

        # Remove old completed tasks (older than 5 minutes)
        old_threshold = current_time - 300  # 5 minutes
        old_tasks = [
            task_id
            for task_id, task in self.get_completed_tasks().items()
            if task.completion_time and task.completion_time < old_threshold
        ]

        for task_id in old_tasks:
            self.remove_task(task_id)

        if old_tasks:
            logging.info(f"Cleaned up {len(old_tasks)} old completed tasks")

        self._last_cleanup_time = current_time


class Window(QMainWindow):
    """
    Enhanced main window with comprehensive progress management demo.

    This window demonstrates both manual and automatic progress modes,
    showing when each approach is appropriate for different use cases.
    """

    def __init__(self):
        super().__init__(parent=None)

        # Initialize language management system
        self.language_manager = LanguageManager()

        # Window settings
        self.setFixedSize(1000, 700)  # Increased size for enhanced UI
        self.setWindowTitle(self.language_manager.get_text("window_title"))

        # Initialize progress management system
        self._init_progress_management()

        # Create enhanced UI layout
        self._setup_ui()

        # Connect signals for better event handling
        self._connect_signals()

    def _init_progress_management(self) -> None:
        """Initialize the enhanced progress management system."""
        self.progress_manager = ProgressManager()
        self.selected_task_id: Optional[str] = None
        self._updating_slider: bool = False  # Prevent signal loops

    def _setup_ui(self) -> None:
        """Setup the enhanced user interface."""
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

        # Create grid layout with better spacing
        grid = QGridLayout()
        grid.setSpacing(15)

        # Add widget groups with improved layout
        grid.addWidget(self.create_static_settings_group(), 0, 0)
        grid.addWidget(self.create_toast_preset_group(), 1, 0)
        grid.addWidget(self.create_enhanced_progress_demo_group(), 2, 0)
        grid.addWidget(self.create_toast_custom_group(), 0, 1, 3, 1, Qt.AlignmentFlag.AlignTop)

        main_layout.addLayout(grid)

        # Apply layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.setFocus()

    def _connect_signals(self) -> None:
        """Connect progress manager signals to UI update methods."""
        self.progress_manager.taskCreated.connect(self._on_task_created)
        self.progress_manager.taskUpdated.connect(self._on_task_updated)
        self.progress_manager.taskCompleted.connect(self._on_task_completed)
        self.progress_manager.taskFailed.connect(self._on_task_failed)
        self.progress_manager.taskModeChanged.connect(self._on_task_mode_changed)
        self.progress_manager.allTasksCompleted.connect(self._on_all_tasks_completed)

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
        self._update_progress_demo_text()
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

    def create_enhanced_progress_demo_group(self) -> QGroupBox:
        """Create enhanced progress demonstration group with manual/automatic mode support."""
        self.progress_demo_group = QGroupBox(self.language_manager.get_text("progress_demo"))

        # Progress mode selection
        self.mode_group = QButtonGroup()
        self.manual_mode_radio = QRadioButton(self.language_manager.get_text("manual_mode"))
        self.automatic_mode_radio = QRadioButton(self.language_manager.get_text("automatic_mode"))
        self.manual_mode_radio.setChecked(True)  # Default to manual
        self.mode_group.addButton(self.manual_mode_radio, 0)
        self.mode_group.addButton(self.automatic_mode_radio, 1)

        # Task selection dropdown with enhanced display
        self.task_selector = QComboBox()
        self.task_selector.setFixedHeight(24)
        self.task_selector.currentTextChanged.connect(self.on_task_selected)

        # Manual progress controls
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setRange(0, 100)
        self.progress_slider.setValue(0)
        self.progress_slider.setFixedHeight(24)
        self.progress_slider.valueChanged.connect(self.update_selected_progress)

        self.progress_label = QLabel(self.language_manager.get_text("progress_text").format("0"))
        self.progress_label.setFixedWidth(100)

        # Animation toggle
        self.animation_checkbox = QCheckBox(self.language_manager.get_text("animated_progress"))
        self.animation_checkbox.setChecked(True)

        # Task creation buttons
        self.create_manual_task_button = QPushButton(self.language_manager.get_text("create_manual_task"))
        self.create_manual_task_button.clicked.connect(self.create_manual_task)
        self.create_manual_task_button.setFixedHeight(32)

        self.create_auto_task_button = QPushButton(self.language_manager.get_text("create_auto_task"))
        self.create_auto_task_button.clicked.connect(self.create_automatic_task)
        self.create_auto_task_button.setFixedHeight(32)

        self.create_bulk_tasks_button = QPushButton(self.language_manager.get_text("create_bulk_tasks"))
        self.create_bulk_tasks_button.clicked.connect(self.create_bulk_mixed_tasks)
        self.create_bulk_tasks_button.setFixedHeight(32)

        # Control buttons
        self.start_auto_all_button = QPushButton(self.language_manager.get_text("start_all_auto"))
        self.start_auto_all_button.clicked.connect(self.start_auto_progress_all)
        self.start_auto_all_button.setFixedHeight(32)

        self.stop_auto_all_button = QPushButton(self.language_manager.get_text("stop_all_auto"))
        self.stop_auto_all_button.clicked.connect(self.stop_auto_progress_all)
        self.stop_auto_all_button.setFixedHeight(32)

        self.start_auto_selected_button = QPushButton(self.language_manager.get_text("start_selected_auto"))
        self.start_auto_selected_button.clicked.connect(self.start_auto_progress_selected)
        self.start_auto_selected_button.setFixedHeight(32)

        self.stop_auto_selected_button = QPushButton(self.language_manager.get_text("stop_selected_auto"))
        self.stop_auto_selected_button.clicked.connect(self.stop_auto_progress_selected)
        self.stop_auto_selected_button.setFixedHeight(32)

        # Mode switching button
        self.switch_mode_button = QPushButton(self.language_manager.get_text("switch_mode"))
        self.switch_mode_button.clicked.connect(self.switch_selected_task_mode)
        self.switch_mode_button.setFixedHeight(32)

        # Cleanup button
        self.clear_completed_button = QPushButton(self.language_manager.get_text("clear_completed"))
        self.clear_completed_button.clicked.connect(self.clear_completed_tasks)
        self.clear_completed_button.setFixedHeight(32)

        # Store labels for later updates
        self.progress_mode_label = QLabel(self.language_manager.get_text("progress_mode"))
        self.select_task_label = QLabel(self.language_manager.get_text("select_task"))
        self.manual_progress_label = QLabel(self.language_manager.get_text("manual_progress"))

        # Enhanced layouts with logical grouping
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.progress_mode_label)
        mode_layout.addWidget(self.manual_mode_radio)
        mode_layout.addWidget(self.automatic_mode_radio)
        mode_layout.addStretch()

        task_layout = QHBoxLayout()
        task_layout.addWidget(self.select_task_label)
        task_layout.addWidget(self.task_selector)
        task_layout.addWidget(self.switch_mode_button)

        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.manual_progress_label)
        progress_layout.addWidget(self.progress_slider)
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.animation_checkbox)

        # Button layouts with logical grouping
        create_layout = QHBoxLayout()
        create_layout.addWidget(self.create_manual_task_button)
        create_layout.addWidget(self.create_auto_task_button)
        create_layout.addWidget(self.create_bulk_tasks_button)

        auto_control_layout = QHBoxLayout()
        auto_control_layout.addWidget(self.start_auto_all_button)
        auto_control_layout.addWidget(self.stop_auto_all_button)

        selected_control_layout = QHBoxLayout()
        selected_control_layout.addWidget(self.start_auto_selected_button)
        selected_control_layout.addWidget(self.stop_auto_selected_button)

        cleanup_layout = QHBoxLayout()
        cleanup_layout.addWidget(self.clear_completed_button)
        cleanup_layout.addStretch()

        # Main layout with improved spacing
        vbox_layout = QVBoxLayout()
        vbox_layout.setSpacing(10)
        vbox_layout.addLayout(mode_layout)
        vbox_layout.addLayout(task_layout)
        vbox_layout.addLayout(progress_layout)
        vbox_layout.addLayout(create_layout)
        vbox_layout.addLayout(auto_control_layout)
        vbox_layout.addLayout(selected_control_layout)
        vbox_layout.addLayout(cleanup_layout)
        vbox_layout.addStretch(1)
        self.progress_demo_group.setLayout(vbox_layout)

        return self.progress_demo_group

    def _update_progress_demo_text(self):
        """Update progress demo group text elements."""
        self.progress_demo_group.setTitle(self.language_manager.get_text("progress_demo"))

        # Update radio buttons
        self.manual_mode_radio.setText(self.language_manager.get_text("manual_mode"))
        self.automatic_mode_radio.setText(self.language_manager.get_text("automatic_mode"))

        # Update labels
        self.progress_mode_label.setText(self.language_manager.get_text("progress_mode"))
        self.select_task_label.setText(self.language_manager.get_text("select_task"))
        self.manual_progress_label.setText(self.language_manager.get_text("manual_progress"))
        self.animation_checkbox.setText(self.language_manager.get_text("animated_progress"))

        # Update buttons
        self.create_manual_task_button.setText(self.language_manager.get_text("create_manual_task"))
        self.create_auto_task_button.setText(self.language_manager.get_text("create_auto_task"))
        self.create_bulk_tasks_button.setText(self.language_manager.get_text("create_bulk_tasks"))
        self.start_auto_all_button.setText(self.language_manager.get_text("start_all_auto"))
        self.stop_auto_all_button.setText(self.language_manager.get_text("stop_all_auto"))
        self.start_auto_selected_button.setText(self.language_manager.get_text("start_selected_auto"))
        self.stop_auto_selected_button.setText(self.language_manager.get_text("stop_selected_auto"))
        self.switch_mode_button.setText(self.language_manager.get_text("switch_mode"))
        self.clear_completed_button.setText(self.language_manager.get_text("clear_completed"))

    # Signal handlers for progress manager events
    def _on_task_created(self, task_id: str) -> None:
        """Handle task creation event."""
        self._update_task_selector()
        logging.info(f"UI: Task created - {task_id}")

    def _on_task_updated(self, task_id: str, progress: float) -> None:
        """Handle task progress update event."""
        if task_id == self.selected_task_id:
            progress_percent = int(progress * 100)
            self._update_slider_safely(progress_percent)
        self._update_task_selector()

    def _on_task_completed(self, task_id: str) -> None:
        """Handle task completion event."""
        self._update_task_selector()
        task = self.progress_manager.get_task(task_id)
        if task:
            self._show_completion_message(task.name)

    def _on_task_failed(self, task_id: str, error_message: str) -> None:
        """Handle task failure event."""
        self._update_task_selector()
        task = self.progress_manager.get_task(task_id)
        if task:
            self._show_error_message(task.name, error_message)

    def _on_task_mode_changed(self, task_id: str, new_mode: str) -> None:
        """Handle task mode change event."""
        self._update_task_selector()
        self._update_ui_for_selected_task()
        logging.info(f"UI: Task {task_id} mode changed to {new_mode}")

    def _on_all_tasks_completed(self) -> None:
        """Handle all tasks completion event."""
        self._show_info_message("All Tasks Completed", "All tasks have been completed successfully!")

    def _update_task_selector(self) -> None:
        """Update task selection dropdown with enhanced display showing modes and status."""
        self.task_selector.clear()

        # Add active tasks with enhanced display
        active_tasks = self.progress_manager.get_active_tasks()
        for task_id, task in active_tasks.items():
            display_name = task.get_display_name()
            self.task_selector.addItem(display_name, task_id)

        # Add completed tasks
        completed_tasks = self.progress_manager.get_completed_tasks()
        for task_id, task in completed_tasks.items():
            mode_icon = "🎛️" if task.is_manual_mode else "🤖"
            display_name = f"{mode_icon}✅ {task.name} (100%)"
            self.task_selector.addItem(display_name, task_id)

        # Add placeholder if no tasks
        if not active_tasks and not completed_tasks:
            self.task_selector.addItem(self.language_manager.get_text("no_tasks"), None)

    def on_task_selected(self) -> None:
        """Handle task selection with enhanced mode-aware UI updates."""
        try:
            current_index = self.task_selector.currentIndex()
            if current_index >= 0:
                task_id = self.task_selector.itemData(current_index)
                self.selected_task_id = task_id

                if task_id:
                    task = self.progress_manager.get_task(task_id)
                    if task:
                        # Update UI based on task mode and status
                        self._update_ui_for_selected_task()
        except Exception as e:
            logging.error(f"Error in task selection: {e}")

    def _update_slider_safely(self, value: int) -> None:
        """Safely update slider value to prevent signal loops."""
        self._updating_slider = True
        try:
            self.progress_slider.setValue(value)
            self.progress_label.setText(self.language_manager.get_text("progress_text").format(value))
        finally:
            self._updating_slider = False

    def update_selected_progress(self, value: int) -> None:
        """Update selected task progress with enhanced validation and mode checking."""
        if self._updating_slider:
            return

        try:
            self.progress_label.setText(self.language_manager.get_text("progress_text").format(value))

            if self.selected_task_id:
                task = self.progress_manager.get_task(self.selected_task_id)
                if not task:
                    self._show_error_message("Task Not Found", "Selected task no longer exists")
                    return

                if not task.is_manual_mode:
                    self._show_info_message(
                        "Wrong Mode", "Cannot manually control automatic mode tasks. Switch to manual mode first."
                    )
                    return

                progress = value / 100.0
                animated = self.animation_checkbox.isChecked()
                success = self.progress_manager.update_progress(self.selected_task_id, progress, animated)

                if success:
                    self._update_task_selector()
                else:
                    self._show_error_message("Update Failed", "Failed to update progress for selected task")
        except Exception as e:
            logging.error(f"Error updating progress: {e}")
            self._show_error_message("Progress Update Error", str(e))

    def create_new_task(self):
        """Create a new progress task (legacy method - kept for compatibility)"""
        # Create task
        task_id = self.progress_manager.create_task()
        task = self.progress_manager.get_task(task_id)

        # Create Toast
        toast = Toast(self)
        toast.setDuration(0)  # Don't auto-hide
        toast.setTitle(f"📁 {task.name}")
        toast.setText("Use slider to control progress or click 'Simulate All Tasks'")
        toast.setShowDurationBar(True)
        toast.setResetDurationOnHover(False)
        toast.applyPreset(ToastPreset.INFORMATION)

        # Connect close signal
        toast.closed.connect(lambda: self._on_task_toast_closed(task_id))

        # Associate Toast with task
        task.toast = toast
        self.progress_manager.active_toasts[task_id] = toast

        # Show Toast
        toast.show()

        # Set initial progress (0%)
        toast.setDurationBarValue(0.0)

        # Update interface
        self._update_task_selector()

        # Auto-select newly created task
        for i in range(self.task_selector.count()):
            if self.task_selector.itemData(i) == task_id:
                self.task_selector.setCurrentIndex(i)
                break

        print(f"Created new task: {task.name} (ID: {task_id})")

    def simulate_all_tasks(self):
        """Simulate automatic progress for all active tasks (legacy method)"""
        active_tasks = self.progress_manager.get_active_tasks()

        if not active_tasks:
            print("No active tasks to simulate")
            return

        for task_id, task in active_tasks.items():
            if not task.is_auto_running and not task.is_completed:
                self._start_auto_progress(task_id)

        print(f"Started simulating automatic progress for {len(active_tasks)} tasks")

    def _start_auto_progress(self, task_id: str):
        """Start automatic progress for specified task (legacy method)"""
        task = self.progress_manager.get_task(task_id)
        if not task or task.is_completed:
            return

        # Create timer
        timer = QTimer()
        timer.timeout.connect(lambda: self._update_auto_progress(task_id))

        # Set task state
        task.timer = timer
        task.is_auto_running = True

        # Start timer (update every 100ms with random speed)
        interval = random.randint(50, 200)
        timer.start(interval)

        # Update interface
        self._update_task_selector()

    def _update_auto_progress(self, task_id: str):
        """Automatic progress update callback (legacy method)"""
        task = self.progress_manager.get_task(task_id)
        if not task or task.is_completed:
            return

        # Randomly increase progress (0.5% - 2%)
        increment = random.uniform(0.005, 0.02)
        new_progress = task.progress + increment

        # Update progress
        self.progress_manager.update_progress(task_id, new_progress)

        # If this is the currently selected task, safely update slider
        if self.selected_task_id == task_id:
            progress_percent = int(task.progress * 100)
            self._update_slider_safely(progress_percent)

        # Update task selector
        self._update_task_selector()

        # If task is completed, stop timer
        if task.is_completed:
            if task.timer:
                task.timer.stop()
                task.timer = None
            task.is_auto_running = False
            print(f"Task {task.name} completed automatically")

    def clear_completed_tasks(self):
        """Clear all completed tasks"""
        completed_count = len(self.progress_manager.get_completed_tasks())
        self.progress_manager.clear_completed()
        self._update_task_selector()

        # If currently selected task was cleared, reset selection
        if self.selected_task_id and not self.progress_manager.get_task(self.selected_task_id):
            self.selected_task_id = None
            self._update_slider_safely(0)

        print(f"Cleared {completed_count} completed tasks")

    def _on_task_toast_closed(self, task_id: str):
        """Callback when task Toast is closed"""
        print(f"Task {task_id} Toast closed")
        self.progress_manager.remove_task(task_id)
        self._update_task_selector()

        # If the closed task was currently selected, reset selection
        if self.selected_task_id == task_id:
            self.selected_task_id = None
            self._update_slider_safely(0)

    # Enhanced task creation methods
    def create_manual_task(self) -> None:
        """Create a new manual progress task."""
        try:
            task_id = self.progress_manager.create_task(
                name=f"Manual Task {self.progress_manager.task_counter}", progress_mode=ProgressMode.MANUAL
            )
            self._create_task_toast(task_id, "🎛️ Manual Progress Task", "Use the slider to control progress manually")
            logging.info(f"Created manual task: {task_id}")
        except Exception as e:
            self._show_error_message("Task Creation Failed", str(e))

    def create_automatic_task(self) -> None:
        """Create a new automatic progress task."""
        try:
            task_id = self.progress_manager.create_task(
                name=f"Auto Task {self.progress_manager.task_counter}", progress_mode=ProgressMode.AUTOMATIC
            )
            self._create_task_toast(task_id, "🤖 Automatic Progress Task", "Progress will advance automatically")
            logging.info(f"Created automatic task: {task_id}")
        except Exception as e:
            self._show_error_message("Task Creation Failed", str(e))

    def create_bulk_mixed_tasks(self) -> None:
        """Create multiple tasks with mixed modes for demonstration."""
        try:
            task_types = [
                ("File Upload", ProgressMode.MANUAL, "📤"),
                ("Data Processing", ProgressMode.AUTOMATIC, "🔄"),
                ("Download", ProgressMode.MANUAL, "📥"),
            ]

            created_count = 0
            for name, mode, icon in task_types:
                task_id = self.progress_manager.create_task(
                    name=f"{name} {self.progress_manager.task_counter}", progress_mode=mode
                )
                self._create_task_toast(
                    task_id,
                    f"{icon} {name}",
                    f"{'Manual' if mode == ProgressMode.MANUAL else 'Automatic'} progress mode",
                )
                created_count += 1

            logging.info(f"Created {created_count} mixed tasks")
            self._show_info_message("Bulk Creation", f"Created {created_count} mixed tasks successfully!")

        except Exception as e:
            self._show_error_message("Bulk Creation Failed", str(e))

    def _create_task_toast(self, task_id: str, title: str, text: str) -> None:
        """Create and configure a toast for a task."""
        task = self.progress_manager.get_task(task_id)
        if not task:
            return

        # Create Toast
        toast = Toast(self)
        toast.setDuration(0)  # Don't auto-hide for progress tasks
        toast.setTitle(title)
        toast.setText(text)
        toast.setShowDurationBar(True)
        toast.setDurationBarValue(0.0)  # Initial progress 0%
        toast.setIcon(ToastIcon.INFORMATION)
        toast.setShowIcon(True)

        # Connect close signal
        toast.closed.connect(lambda: self._on_task_toast_closed(task_id))

        # Associate Toast with task
        task.toast = toast
        self.progress_manager.active_toasts[task_id] = toast

        # Show Toast
        toast.show()

        # Update UI
        self._update_task_selector()

    # Automatic progress control methods
    def start_auto_progress_all(self) -> None:
        """Start automatic progress for all automatic mode tasks."""
        try:
            started_count = self.progress_manager.start_auto_progress_for_all()
            if started_count > 0:
                self._show_info_message(
                    "Auto Progress Started", f"Started automatic progress for {started_count} tasks"
                )
            else:
                self._show_info_message("No Tasks", "No automatic tasks available to start")
        except Exception as e:
            self._show_error_message("Start Failed", str(e))

    def stop_auto_progress_all(self) -> None:
        """Stop automatic progress for all running automatic tasks."""
        try:
            stopped_count = self.progress_manager.stop_auto_progress_for_all()
            if stopped_count > 0:
                self._show_info_message(
                    "Auto Progress Stopped", f"Stopped automatic progress for {stopped_count} tasks"
                )
            else:
                self._show_info_message("No Tasks", "No automatic tasks are currently running")
        except Exception as e:
            self._show_error_message("Stop Failed", str(e))

    def start_auto_progress_selected(self) -> None:
        """Start automatic progress for the selected task."""
        if not self.selected_task_id:
            self._show_info_message("No Selection", "Please select a task first")
            return

        try:
            task = self.progress_manager.get_task(self.selected_task_id)
            if not task:
                self._show_error_message("Task Not Found", "Selected task no longer exists")
                return

            if not task.is_automatic_mode:
                self._show_info_message("Wrong Mode", "Selected task is not in automatic mode")
                return

            success = self.progress_manager.start_auto_progress_for_task(self.selected_task_id)
            if success:
                self._show_info_message("Started", f"Started automatic progress for {task.name}")
            else:
                self._show_error_message("Start Failed", "Failed to start automatic progress")

        except Exception as e:
            self._show_error_message("Start Failed", str(e))

    def stop_auto_progress_selected(self) -> None:
        """Stop automatic progress for the selected task."""
        if not self.selected_task_id:
            self._show_info_message("No Selection", "Please select a task first")
            return

        try:
            task = self.progress_manager.get_task(self.selected_task_id)
            if not task:
                self._show_error_message("Task Not Found", "Selected task no longer exists")
                return

            success = self.progress_manager.stop_auto_progress_for_task(self.selected_task_id)
            if success:
                self._show_info_message("Stopped", f"Stopped automatic progress for {task.name}")
            else:
                self._show_error_message("Stop Failed", "Failed to stop automatic progress")

        except Exception as e:
            self._show_error_message("Stop Failed", str(e))

    def switch_selected_task_mode(self) -> None:
        """Switch the progress mode of the selected task."""
        if not self.selected_task_id:
            self._show_info_message("No Selection", "Please select a task first")
            return

        try:
            task = self.progress_manager.get_task(self.selected_task_id)
            if not task:
                self._show_error_message("Task Not Found", "Selected task no longer exists")
                return

            if task.is_completed:
                self._show_info_message("Task Completed", "Cannot change mode of completed task")
                return

            # Switch to opposite mode
            new_mode = ProgressMode.AUTOMATIC if task.is_manual_mode else ProgressMode.MANUAL
            success = self.progress_manager.set_task_mode(self.selected_task_id, new_mode)

            if success:
                mode_name = "automatic" if new_mode == ProgressMode.AUTOMATIC else "manual"
                self._show_info_message("Mode Changed", f"Switched {task.name} to {mode_name} mode")
                self._update_ui_for_selected_task()
            else:
                self._show_error_message("Mode Change Failed", "Failed to change task mode")

        except Exception as e:
            self._show_error_message("Mode Change Failed", str(e))

    # UI helper methods
    def _update_ui_for_selected_task(self) -> None:
        """Update UI elements based on the selected task."""
        if not self.selected_task_id:
            self.progress_slider.setEnabled(False)
            return

        task = self.progress_manager.get_task(self.selected_task_id)
        if not task:
            self.progress_slider.setEnabled(False)
            return

        # Enable/disable slider based on task mode
        self.progress_slider.setEnabled(task.is_manual_mode and not task.is_completed)

        # Update progress display
        progress_percent = task.progress_percentage
        self._update_slider_safely(progress_percent)

    def _show_info_message(self, title: str, message: str) -> None:
        """Show an information message box."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def _show_error_message(self, title: str, message: str) -> None:
        """Show an error message box."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def _show_completion_message(self, task_name: str) -> None:
        """Show a completion message for a task."""
        self._show_info_message("Task Completed", f"Task '{task_name}' has been completed successfully!")

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
        self.border_radius_spinbox.setValue(2)
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

        # Add layouts and widgets to main layout
        vbox_layout = QVBoxLayout()
        vbox_layout.addLayout(form_layout)
        vbox_layout.addLayout(icon_layout)
        vbox_layout.addLayout(checkbox_layout)
        vbox_layout.addLayout(double_form_layout_1)
        vbox_layout.addLayout(double_form_layout_2)
        vbox_layout.addLayout(double_form_layout_3)
        vbox_layout.addLayout(double_form_layout_4)
        vbox_layout.addWidget(self.custom_toast_button)
        vbox_layout.addStretch(1)
        self.custom_toast_group.setLayout(vbox_layout)

        return self.custom_toast_group

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
        # Show toast with selected preset and random duration
        toast = Toast(self)
        toast.setDuration(random.randint(2000, 5000))

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

        # Map icon dropdown index to icon type
        icon_index = self.icon_dropdown.currentIndex()
        icon_map = [ToastIcon.SUCCESS, ToastIcon.WARNING, ToastIcon.ERROR, ToastIcon.INFORMATION, ToastIcon.CLOSE]
        if 0 <= icon_index < len(icon_map):
            toast.setIcon(icon_map[icon_index])

        # Map close button dropdown index to alignment
        close_button_index = self.close_button_settings_dropdown.currentIndex()
        if close_button_index == 0:  # Top
            toast.setCloseButtonAlignment(ToastButtonAlignment.TOP)
        elif close_button_index == 1:  # Middle
            toast.setCloseButtonAlignment(ToastButtonAlignment.MIDDLE)
        elif close_button_index == 2:  # Bottom
            toast.setCloseButtonAlignment(ToastButtonAlignment.BOTTOM)
        elif close_button_index == 3:  # Disabled
            toast.setShowCloseButton(False)

        toast.show()
