"""
Language management module for PySide6 Toast Demo.

This module provides internationalization support with Chinese and English translations
for all UI elements in the toast demonstration application.
"""

from enum import Enum
from typing import Dict


class Language(Enum):
    """Language enumeration for bilingual support."""
    CHINESE = "zh"
    ENGLISH = "en"


class LanguageManager:
    """Manages bilingual text content for the application."""
    
    def __init__(self):
        self.current_language = Language.CHINESE
        self.translations = {
            # Window and group titles
            "window_title": {
                Language.CHINESE: "Enhanced PySide6 Toast Demo - Manual & Automatic Progress",
                Language.ENGLISH: "Enhanced PySide6 Toast Demo - Manual & Automatic Progress"
            },
            "static_settings": {Language.CHINESE: "静态设置", Language.ENGLISH: "Static Settings"},
            "toast_presets": {Language.CHINESE: "Toast 预设", Language.ENGLISH: "Toast Presets"},
            "custom_toast": {Language.CHINESE: "自定义 Toast", Language.ENGLISH: "Custom Toast"},
            "progress_demo": {
                Language.CHINESE: "增强进度管理演示",
                Language.ENGLISH: "Enhanced Progress Management Demo",
            },
            
            # Static settings labels
            "max_on_screen": {Language.CHINESE: "屏幕最大数量:", Language.ENGLISH: "Max on Screen:"},
            "spacing": {Language.CHINESE: "间距:", Language.ENGLISH: "Spacing:"},
            "x_offset": {Language.CHINESE: "X偏移:", Language.ENGLISH: "X Offset:"},
            "y_offset": {Language.CHINESE: "Y偏移:", Language.ENGLISH: "Y Offset:"},
            "position": {Language.CHINESE: "位置:", Language.ENGLISH: "Position:"},
            "always_main_screen": {Language.CHINESE: "始终在主屏幕上", Language.ENGLISH: "Always on Main Screen"},
            "update_button": {Language.CHINESE: "更新", Language.ENGLISH: "Update"},
            
            # Position options
            "bottom_left": {Language.CHINESE: "左下", Language.ENGLISH: "Bottom Left"},
            "bottom_middle": {Language.CHINESE: "中下", Language.ENGLISH: "Bottom Middle"},
            "bottom_right": {Language.CHINESE: "右下", Language.ENGLISH: "Bottom Right"},
            "top_left": {Language.CHINESE: "左上", Language.ENGLISH: "Top Left"},
            "top_middle": {Language.CHINESE: "中上", Language.ENGLISH: "Top Middle"},
            "top_right": {Language.CHINESE: "右上", Language.ENGLISH: "Top Right"},
            "center": {Language.CHINESE: "居中", Language.ENGLISH: "Center"},
            
            # Preset options
            "success": {Language.CHINESE: "成功", Language.ENGLISH: "Success"},
            "warning": {Language.CHINESE: "警告", Language.ENGLISH: "Warning"},
            "error": {Language.CHINESE: "错误", Language.ENGLISH: "Error"},
            "information": {Language.CHINESE: "信息", Language.ENGLISH: "Information"},
            "success_dark": {Language.CHINESE: "成功(深色)", Language.ENGLISH: "Success (Dark)"},
            "warning_dark": {Language.CHINESE: "警告(深色)", Language.ENGLISH: "Warning (Dark)"},
            "error_dark": {Language.CHINESE: "错误(深色)", Language.ENGLISH: "Error (Dark)"},
            "information_dark": {Language.CHINESE: "信息(深色)", Language.ENGLISH: "Information (Dark)"},
            "close": {Language.CHINESE: "关闭", Language.ENGLISH: "Close"},
            
            # Buttons
            "show_preset_toast": {Language.CHINESE: "显示预设 Toast", Language.ENGLISH: "Show Preset Toast"},
            "show_custom_toast": {Language.CHINESE: "显示自定义 Toast", Language.ENGLISH: "Show Custom Toast"},
            "toggle_language": {Language.CHINESE: "切换语言", Language.ENGLISH: "Toggle Language"},
            
            # Custom toast labels
            "duration": {Language.CHINESE: "持续时间:", Language.ENGLISH: "Duration:"},
            "title": {Language.CHINESE: "标题:", Language.ENGLISH: "Title:"},
            "text": {Language.CHINESE: "文本:", Language.ENGLISH: "Text:"},
            "show_icon": {Language.CHINESE: "显示图标", Language.ENGLISH: "Show Icon"},
            "icon_size": {Language.CHINESE: "图标大小:", Language.ENGLISH: "Icon Size:"},
            "show_duration_bar": {Language.CHINESE: "显示持续时间条", Language.ENGLISH: "Show Duration Bar"},
            "reset_on_hover": {Language.CHINESE: "悬停时重置持续时间", Language.ENGLISH: "Reset Duration on Hover"},
            "border_radius": {Language.CHINESE: "边框圆角:", Language.ENGLISH: "Border Radius:"},
            "close_button": {Language.CHINESE: "关闭按钮:", Language.ENGLISH: "Close Button:"},
            "min_width": {Language.CHINESE: "最小宽度:", Language.ENGLISH: "Min Width:"},
            "max_width": {Language.CHINESE: "最大宽度:", Language.ENGLISH: "Max Width:"},
            "min_height": {Language.CHINESE: "最小高度:", Language.ENGLISH: "Min Height:"},
            "max_height": {Language.CHINESE: "最大高度:", Language.ENGLISH: "Max Height:"},
            "fade_in_duration": {Language.CHINESE: "淡入持续时间:", Language.ENGLISH: "Fade In Duration:"},
            "fade_out_duration": {Language.CHINESE: "淡出持续时间:", Language.ENGLISH: "Fade Out Duration:"},
            
            # Close button positions
            "top": {Language.CHINESE: "顶部", Language.ENGLISH: "Top"},
            "middle": {Language.CHINESE: "中间", Language.ENGLISH: "Middle"},
            "bottom": {Language.CHINESE: "底部", Language.ENGLISH: "Bottom"},
            "disabled": {Language.CHINESE: "禁用", Language.ENGLISH: "Disabled"},
            
            # Default values
            "default_title": {Language.CHINESE: "这是一个标题", Language.ENGLISH: "This is a title"},
            
            # Toast messages
            "success_title": {
                Language.CHINESE: "成功！确认邮件已发送。",
                Language.ENGLISH: "Success! Confirmation email sent.",
            },
            "success_text": {
                Language.CHINESE: "请检查您的邮箱以完成注册。",
                Language.ENGLISH: "Please check your email to complete registration.",
            },
            "warning_title": {
                Language.CHINESE: "警告！密码不匹配。",
                Language.ENGLISH: "Warning! Passwords do not match.",
            },
            "warning_text": {
                Language.CHINESE: "请再次确认您的密码。",
                Language.ENGLISH: "Please confirm your password again.",
            },
            "error_title": {
                Language.CHINESE: "错误！无法完成请求。",
                Language.ENGLISH: "Error! Unable to complete request.",
            },
            "error_text": {
                Language.CHINESE: "请几分钟后再试。",
                Language.ENGLISH: "Please try again in a few minutes.",
            },
            "info_title": {Language.CHINESE: "信息：需要重启。", Language.ENGLISH: "Information: Restart required."},
            "info_text": {Language.CHINESE: "请重启应用程序。", Language.ENGLISH: "Please restart the application."},
            
            # Additional UI text
            "manual_mode": {Language.CHINESE: "手动模式", Language.ENGLISH: "Manual Mode"},
            "automatic_mode": {Language.CHINESE: "自动模式", Language.ENGLISH: "Automatic Mode"},
            "progress_mode": {Language.CHINESE: "进度模式:", Language.ENGLISH: "Progress Mode:"},
            "select_task": {Language.CHINESE: "选择任务:", Language.ENGLISH: "Select Task:"},
            "manual_progress": {Language.CHINESE: "手动进度:", Language.ENGLISH: "Manual Progress:"},
            "animated_progress": {Language.CHINESE: "动画进度", Language.ENGLISH: "Animated Progress"},
            "create_manual_task": {Language.CHINESE: "创建手动任务", Language.ENGLISH: "Create Manual Task"},
            "create_auto_task": {Language.CHINESE: "创建自动任务", Language.ENGLISH: "Create Auto Task"},
            "create_bulk_tasks": {Language.CHINESE: "创建3个混合任务", Language.ENGLISH: "Create 3 Mixed Tasks"},
            "start_all_auto": {Language.CHINESE: "启动所有自动任务", Language.ENGLISH: "Start All Auto Tasks"},
            "stop_all_auto": {Language.CHINESE: "停止所有自动任务", Language.ENGLISH: "Stop All Auto Tasks"},
            "start_selected_auto": {Language.CHINESE: "启动选中的自动任务", Language.ENGLISH: "Start Selected Auto"},
            "stop_selected_auto": {Language.CHINESE: "停止选中的自动任务", Language.ENGLISH: "Stop Selected Auto"},
            "switch_mode": {Language.CHINESE: "切换选中模式", Language.ENGLISH: "Switch Selected Mode"},
            "clear_completed": {Language.CHINESE: "清除已完成", Language.ENGLISH: "Clear Completed"},
            "progress_text": {Language.CHINESE: "进度: {0}%", Language.ENGLISH: "Progress: {0}%"},
            "no_tasks": {Language.CHINESE: "无任务 - 创建新任务", Language.ENGLISH: "No tasks - Create a new task"},
            "multiline_text": {Language.CHINESE: "启用多行文本", Language.ENGLISH: "Enable multiline text"},
        }
    
    def get_text(self, key: str) -> str:
        """Get translated text for the current language."""
        if key in self.translations:
            return self.translations[key].get(self.current_language, key)
        return key
    
    def toggle_language(self) -> None:
        """Toggle between Chinese and English."""
        self.current_language = Language.ENGLISH if self.current_language == Language.CHINESE else Language.CHINESE
    
    def is_chinese(self) -> bool:
        """Check if current language is Chinese."""
        return self.current_language == Language.CHINESE
    
    def is_english(self) -> bool:
        """Check if current language is English."""
        return self.current_language == Language.ENGLISH
    
    def get_current_language(self) -> Language:
        """Get the current language."""
        return self.current_language
    
    def set_language(self, language: Language) -> None:
        """Set the current language."""
        if isinstance(language, Language):
            self.current_language = language
