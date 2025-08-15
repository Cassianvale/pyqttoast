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
        self.current_language = Language.ENGLISH
        self.translations = {
            # Window and group titles
            "static_settings": {Language.CHINESE: "静态设置", Language.ENGLISH: "Static Settings"},
            "toast_presets": {Language.CHINESE: "Toast 预设", Language.ENGLISH: "Toast Presets"},
            "custom_toast": {Language.CHINESE: "自定义 Toast", Language.ENGLISH: "Custom Toast"},
            
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

            # Font customization labels
            "title_font_size": {Language.CHINESE: "标题字体大小:", Language.ENGLISH: "Title Font Size:"},
            "text_font_size": {Language.CHINESE: "文本字体大小:", Language.ENGLISH: "Text Font Size:"},
            "font_family": {Language.CHINESE: "字体族:", Language.ENGLISH: "Font Family:"},
            "font_presets": {Language.CHINESE: "字体预设:", Language.ENGLISH: "Font Presets:"},
            
            # Multiline text
            "multiline_text": {Language.CHINESE: "启用多行文本", Language.ENGLISH: "Enable multiline text"},

            # Font preset buttons
            "small_font": {Language.CHINESE: "小字体 (10pt)", Language.ENGLISH: "Small (10pt)"},
            "medium_font": {Language.CHINESE: "中等字体 (12pt)", Language.ENGLISH: "Medium (12pt)"},
            "large_font": {Language.CHINESE: "大字体 (18pt)", Language.ENGLISH: "Large (18pt)"},

            # Test features
            "test_clickable_links": {Language.CHINESE: "测试可点击链接", Language.ENGLISH: "Test Clickable Links"},
            "clickable_links_title": {Language.CHINESE: "可点击链接测试", Language.ENGLISH: "Clickable Links Test"},
            "clickable_links_text": {
                Language.CHINESE: "URLs Test! Try these:\n"
                    "HTML: <a href='https://www.example.com'>Click here</a>",
                Language.ENGLISH: "URLs Test! Try these:\n"
                    "HTML: <a href='https://www.example.com'>Click here</a>"
            },

            # Close button positions
            "top": {Language.CHINESE: "顶部", Language.ENGLISH: "Top"},
            "middle": {Language.CHINESE: "中间", Language.ENGLISH: "Middle"},
            "bottom": {Language.CHINESE: "底部", Language.ENGLISH: "Bottom"},
            "disabled": {Language.CHINESE: "禁用", Language.ENGLISH: "Disabled"},
            
            # Tab titles
            "basic_features": {Language.CHINESE: "基础功能", Language.ENGLISH: "Basic Features"},
            "advanced_features": {Language.CHINESE: "高级功能", Language.ENGLISH: "Advanced Features"},

            # Animation group
            "animation_settings": {Language.CHINESE: "动画设置", Language.ENGLISH: "Animation Settings"},
            "animation_direction": {Language.CHINESE: "动画方向:", Language.ENGLISH: "Animation Direction:"},
            "auto": {Language.CHINESE: "自动", Language.ENGLISH: "Auto"},
            "from_top": {Language.CHINESE: "从顶部", Language.ENGLISH: "From Top"},
            "from_bottom": {Language.CHINESE: "从底部", Language.ENGLISH: "From Bottom"},
            "from_left": {Language.CHINESE: "从左侧", Language.ENGLISH: "From Left"},
            "from_right": {Language.CHINESE: "从右侧", Language.ENGLISH: "From Right"},
            "fade_only": {Language.CHINESE: "仅淡化", Language.ENGLISH: "Fade Only"},
            "test_animation": {Language.CHINESE: "测试动画", Language.ENGLISH: "Test Animation"},

            # Margins group
            "margins_settings": {Language.CHINESE: "边距设置", Language.ENGLISH: "Margins Settings"},
            "content_margins": {Language.CHINESE: "内容边距:", Language.ENGLISH: "Content Margins:"},
            "icon_margins": {Language.CHINESE: "图标边距:", Language.ENGLISH: "Icon Margins:"},
            "text_section_margins": {Language.CHINESE: "文本区域边距:", Language.ENGLISH: "Text Section Margins:"},
            "left": {Language.CHINESE: "左:", Language.ENGLISH: "Left:"},
            "right": {Language.CHINESE: "右:", Language.ENGLISH: "Right:"},
            "apply_margins": {Language.CHINESE: "应用边距", Language.ENGLISH: "Apply Margins"},

            # Colors group
            "color_settings": {Language.CHINESE: "颜色设置", Language.ENGLISH: "Color Settings"},
            "background_color": {Language.CHINESE: "背景颜色:", Language.ENGLISH: "Background Color:"},
            "title_color": {Language.CHINESE: "标题颜色:", Language.ENGLISH: "Title Color:"},
            "text_color": {Language.CHINESE: "文本颜色:", Language.ENGLISH: "Text Color:"},
            "icon_color": {Language.CHINESE: "图标颜色:", Language.ENGLISH: "Icon Color:"},
            "duration_bar_color": {Language.CHINESE: "持续时间条颜色:", Language.ENGLISH: "Duration Bar Color:"},
            "choose_color": {Language.CHINESE: "选择颜色", Language.ENGLISH: "Choose Color"},
            "reset_colors": {Language.CHINESE: "重置颜色", Language.ENGLISH: "Reset Colors"},

            # Advanced features group
            "advanced_settings": {Language.CHINESE: "高级设置", Language.ENGLISH: "Advanced Settings"},
            "stay_on_top": {Language.CHINESE: "保持在顶层", Language.ENGLISH: "Stay on Top"},
            "icon_separator": {Language.CHINESE: "显示图标分隔符", Language.ENGLISH: "Show Icon Separator"},
            "separator_width": {Language.CHINESE: "分隔符宽度:", Language.ENGLISH: "Separator Width:"},
            "separator_color": {Language.CHINESE: "分隔符颜色:", Language.ENGLISH: "Separator Color:"},
            "close_button_color": {Language.CHINESE: "关闭按钮颜色:", Language.ENGLISH: "Close Button Color:"},
            "test_callbacks": {Language.CHINESE: "测试回调事件", Language.ENGLISH: "Test Callbacks"},
            "show_multiple": {Language.CHINESE: "显示多个通知", Language.ENGLISH: "Show Multiple Toasts"},
            "queue_demo": {Language.CHINESE: "队列演示", Language.ENGLISH: "Queue Demo"},

            # Additional labels for margins
            "top": {Language.CHINESE: "上:", Language.ENGLISH: "Top:"},
            "bottom": {Language.CHINESE: "下:", Language.ENGLISH: "Bottom:"},

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
