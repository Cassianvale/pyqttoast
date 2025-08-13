# Toast API Reference Table

This document provides a quick reference for the Toast class API in table format. For detailed documentation, see [Toast_API_Documentation.md](Toast_API_Documentation.md).

## ✨ API Featured Functions

**Modern Margin API** - Flexible and Efficient 🚀
- **Multi-format Support**: Supports various input formats including integers, tuples, dictionaries, QMargins, etc.
- **Unified Interface**: One method handles all margin types and components
- **Concise Calls**: Complete complex margin settings with one line of code
- **Backward Compatible**: Retains commonly used traditional methods

## Table of Contents

- [Method Quick Reference](#method-quick-reference)
- [Functional Categories](#functional-categories)
- [Preset Styles Comparison](#preset-styles-comparison)
- [Position Enumeration](#position-enumeration)
- [Animation Direction Enumeration](#animation-direction-enumeration)
- [Performance Optimizations](#performance-optimizations)
- [Quick Usage Patterns](#quick-usage-patterns)

## Method Quick Reference

### Basic Content & Display Methods

| Method | Type | Parameters | Returns | Description | Post-show? |
|--------|------|------------|---------|-------------|------------|
| `__init__` | Instance | `parent: QWidget \| None` | - | Create new Toast instance | N/A |
| `show` | Instance | - | - | Display the toast notification | ❌ |
| `hide` | Instance | - | - | Start hiding process | ✅ |
| `getTitle` | Instance | - | `str` | Get title text | ✅ |
| `setTitle` | Instance | `title: str` | - | Set title text | ❌ |
| `getText` | Instance | - | `str` | Get main text | ✅ |
| `setText` | Instance | `text: str` | - | Set main text (auto-links URLs) | ❌ |
| `getDuration` | Instance | - | `int` | Get duration in milliseconds | ✅ |
| `setDuration` | Instance | `duration: int` | - | Set duration (0 = infinite) | ❌ |
| `isShowDurationBar` | Instance | - | `bool` | Check if duration bar shown | ✅ |
| `setShowDurationBar` | Instance | `on: bool` | - | Enable/disable duration bar | ❌ |
| `setDurationBarValue` | Instance | `fraction: float` | - | Set duration bar progress (0.0-1.0) | ✅ |

### Icon Configuration Methods

| Method | Type | Parameters | Returns | Description | Post-show? |
|--------|------|------------|---------|-------------|------------|
| `getIcon` | Instance | - | `QPixmap` | Get current icon | ✅ |
| `setIcon` | Instance | `icon: QPixmap \| ToastIcon` | - | Set icon (pixmap or enum) | ❌ |
| `isShowIcon` | Instance | - | `bool` | Check if icon shown | ✅ |
| `setShowIcon` | Instance | `on: bool` | - | Enable/disable icon display | ❌ |
| `getIconSize` | Instance | - | `QSize` | Get icon size | ✅ |
| `setIconSize` | Instance | `size: QSize` | - | Set icon size | ❌ |
| `getIconColor` | Instance | - | `QColor \| None` | Get icon color | ✅ |
| `setIconColor` | Instance | `color: QColor \| None` | - | Set icon recolor (None = original) | ❌ |
| `isShowIconSeparator` | Instance | - | `bool` | Check if separator shown | ✅ |
| `setShowIconSeparator` | Instance | `on: bool` | - | Enable/disable icon separator | ❌ |
| `getIconSeparatorWidth` | Instance | - | `int` | Get separator width | ✅ |
| `setIconSeparatorWidth` | Instance | `width: int` | - | Set separator width | ❌ |
| `getIconSeparatorColor` | Instance | - | `QColor` | Get separator color | ✅ |
| `setIconSeparatorColor` | Instance | `color: QColor` | - | Set separator color | ❌ |

### Close Button Configuration Methods

| Method | Type | Parameters | Returns | Description | Post-show? |
|--------|------|------------|---------|-------------|------------|
| `getCloseButtonIcon` | Instance | - | `QPixmap` | Get close button icon | ✅ |
| `setCloseButtonIcon` | Instance | `icon: QPixmap \| ToastIcon` | - | Set close button icon | ❌ |
| `isShowCloseButton` | Instance | - | `bool` | Check if close button shown | ✅ |
| `setShowCloseButton` | Instance | `show: bool` | - | Enable/disable close button | ❌ |
| `getCloseButtonIconSize` | Instance | - | `QSize` | Get close button icon size | ✅ |
| `setCloseButtonIconSize` | Instance | `size: QSize` | - | Set close button icon size | ❌ |
| `getCloseButtonSize` | Instance | - | `QSize` | Get close button size | ✅ |
| `setCloseButtonSize` | Instance | `size: QSize` | - | Set close button size | ❌ |
| `getCloseButtonWidth` | Instance | - | `int` | Get close button width | ✅ |
| `setCloseButtonWidth` | Instance | `width: int` | - | Set close button width | ❌ |
| `getCloseButtonHeight` | Instance | - | `int` | Get close button height | ✅ |
| `setCloseButtonHeight` | Instance | `height: int` | - | Set close button height | ❌ |
| `getCloseButtonAlignment` | Instance | - | `ToastButtonAlignment` | Get button alignment | ✅ |
| `setCloseButtonAlignment` | Instance | `alignment: ToastButtonAlignment` | - | Set button alignment (TOP/MIDDLE/BOTTOM) | ❌ |
| `getCloseButtonIconColor` | Instance | - | `QColor \| None` | Get close button icon color | ✅ |
| `setCloseButtonIconColor` | Instance | `color: QColor \| None` | - | Set close button icon color | ❌ |

### Animation & Behavior Methods

| Method | Type | Parameters | Returns | Description | Post-show? |
|--------|------|------------|---------|-------------|------------|
| `getFadeInDuration` | Instance | - | `int` | Get fade-in duration (ms) | ✅ |
| `setFadeInDuration` | Instance | `duration: int` | - | Set fade-in duration | ❌ |
| `getFadeOutDuration` | Instance | - | `int` | Get fade-out duration (ms) | ✅ |
| `setFadeOutDuration` | Instance | `duration: int` | - | Set fade-out duration | ❌ |
| `getAnimationDirection` | Instance | - | `ToastAnimationDirection` | Get animation direction | ✅ |
| `setAnimationDirection` | Instance | `direction: ToastAnimationDirection` | - | Set slide animation direction | ❌ |
| `isResetDurationOnHover` | Instance | - | `bool` | Check if duration resets on hover | ✅ |
| `setResetDurationOnHover` | Instance | `on: bool` | - | Enable/disable hover reset | ❌ |
| `isStayOnTop` | Instance | - | `bool` | Check if toast stays on top | ✅ |
| `setStayOnTop` | Instance | `on: bool` | - | Enable/disable stay on top | ❌ |

### Appearance Customization Methods

| Method | Type | Parameters | Returns | Description | Post-show? |
|--------|------|------------|---------|-------------|------------|
| `getBorderRadius` | Instance | - | `int` | Get border radius | ✅ |
| `setBorderRadius` | Instance | `border_radius: int` | - | Set border radius | ❌ |
| `getBackgroundColor` | Instance | - | `QColor` | Get background color | ✅ |
| `setBackgroundColor` | Instance | `color: QColor` | - | Set background color | ❌ |
| `getTitleColor` | Instance | - | `QColor` | Get title text color | ✅ |
| `setTitleColor` | Instance | `color: QColor` | - | Set title text color | ❌ |
| `getTextColor` | Instance | - | `QColor` | Get main text color | ✅ |
| `setTextColor` | Instance | `color: QColor` | - | Set main text color | ❌ |
| `getDurationBarColor` | Instance | - | `QColor` | Get duration bar color | ✅ |
| `setDurationBarColor` | Instance | `color: QColor` | - | Set duration bar color | ❌ |

### Font Configuration Methods

| Method | Type | Parameters | Returns | Description | Post-show? |
|--------|------|------------|---------|-------------|------------|
| `getTitleFont` | Instance | - | `QFont` | Get title font | ✅ |
| `setTitleFont` | Instance | `font: QFont` | - | Set title font | ❌ |
| `getTextFont` | Instance | - | `QFont` | Get text font | ✅ |
| `setTextFont` | Instance | `font: QFont` | - | Set text font | ❌ |
| `getTitleFontSize` | Instance | - | `int` | Get title font size (points) | ✅ |
| `setTitleFontSize` | Instance | `size: int` | - | Set title font size | ❌ |
| `getTextFontSize` | Instance | - | `int` | Get text font size (points) | ✅ |
| `setTextFontSize` | Instance | `size: int` | - | Set text font size | ❌ |
| `setFontSize` | Instance | `title_size: int, text_size: int = None` | - | Set both font sizes | ❌ |
| `setFontFamily` | Instance | `family: str` | - | Set font family for both | ❌ |
| `getTitleFontFamily` | Instance | - | `str` | Get title font family | ✅ |
| `getTextFontFamily` | Instance | - | `str` | Get text font family | ✅ |

### Layout & Size Control Methods

| Method | Type | Parameters | Returns | Description | Post-show? |
|--------|------|------------|---------|-------------|------------|
| `setFixedSize` | Instance | `size: QSize` | - | Set fixed toast size | ❌ |
| `setFixedWidth` | Instance | `width: int` | - | Set fixed toast width | ❌ |
| `setFixedHeight` | Instance | `height: int` | - | Set fixed toast height | ❌ |
| `getMargins` | Instance | - | `QMargins` | Get content margins | ✅ |
| `setMargins` | Instance | `margins: QMargins` | - | Set content margins | ❌ |
| `getMarginLeft/Top/Right/Bottom` | Instance | - | `int` | Get individual margins | ✅ |
| `setMarginLeft/Top/Right/Bottom` | Instance | `margin: int` | - | Set individual margins | ❌ |
| `getTextSectionSpacing` | Instance | - | `int` | Get title-text spacing | ✅ |
| `setTextSectionSpacing` | Instance | `spacing: int` | - | Set title-text spacing | ❌ |

### Margin Management Methods (11 methods)

| Method | Type | Parameters | Returns | Description | Post-show? |
|--------|------|------------|---------|-------------|------------|
| **Core Margin Methods** |
| `setMargins` | Instance | `margins, margin_type='content'` | - | Flexible margin setting, supports multiple input formats | ❌ |
| `getMargins` | Instance | `margin_type='content'` | `QMargins` | Get margins of specified type | ✅ |
| `adjustMargins` | Instance | `margin_type='content', **kwargs` | - | Fine-tune specific directions of specified margins | ❌ |
| **Compatibility Methods** |
| `setMarginLeft` | Instance | `margin: int` | - | Set content left margin | ❌ |
| `setMarginTop` | Instance | `margin: int` | - | Set content top margin | ❌ |
| `setMarginRight` | Instance | `margin: int` | - | Set content right margin | ❌ |
| `setMarginBottom` | Instance | `margin: int` | - | Set content bottom margin | ❌ |
| `getMarginLeft` | Instance | - | `int` | Get content left margin | ✅ |
| `getMarginTop` | Instance | - | `int` | Get content top margin | ✅ |
| `getMarginRight` | Instance | - | `int` | Get content right margin | ✅ |
| `getMarginBottom` | Instance | - | `int` | Get content bottom margin | ✅ |

#### setMargins Method Detailed Description

The `setMargins` method supports multiple flexible input formats:

**Parameter Description:**
- `margins`: Margin values, supports the following formats:
  - `int`: All margins use the same value, e.g., `setMargins(20)`
  - `tuple (4 elements)`: (left, top, right, bottom), e.g., `setMargins((10, 15, 20, 25))`
  - `tuple (2 elements)`: (horizontal, vertical), e.g., `setMargins((15, 10))`
  - `dict`: Partial update, e.g., `setMargins({'left': 30, 'right': 40})`
  - `QMargins`: Standard margin object, e.g., `setMargins(QMargins(10, 5, 10, 5))`
- `margin_type`: Margin type, options:
  - `'content'` (default): Content margins
  - `'icon'`: Icon margins
  - `'icon_section'`: Icon section margins
  - `'text_section'`: Text section margins
  - `'close_button'`: Close button margins

**Usage Examples:**
```python
# Basic usage
toast.setMargins(20)                    # All margins 20px
toast.setMargins((10, 15, 20, 25))      # Left, top, right, bottom respectively
toast.setMargins((15, 10))              # Horizontal 15px, vertical 10px

# Partial updates
toast.setMargins({'left': 30})          # Only update left margin
toast.setMargins({'top': 5, 'bottom': 8}) # Update top and bottom margins

# Different component margins
toast.setMargins(15, 'icon')            # Set icon margins
toast.setMargins(10, 'text_section')    # Set text section margins

# Fine-tune margins
toast.adjustMargins(left=25, right=30)  # Adjust content margins
toast.adjustMargins('icon', top=5)      # Adjust icon top margin
```

### Advanced Features Methods

| Method | Type | Parameters | Returns | Description | Post-show? |
|--------|------|------------|---------|-------------|------------|
| `isMultiline` | Instance | - | `bool` | Check if multiline enabled | ✅ |
| `setMultiline` | Instance | `on: bool` | - | Enable/disable multiline text | ❌ |
| `applyPreset` | Instance | `preset: ToastPreset` | - | Apply predefined style preset | ❌ |

### Static Configuration Methods

| Method | Type | Parameters | Returns | Description | Post-show? |
|--------|------|------------|---------|-------------|------------|
| `getMaximumOnScreen` | Static | - | `int` | Get max simultaneous toasts | ✅ |
| `setMaximumOnScreen` | Static | `maximum_on_screen: int` | - | Set max simultaneous toasts | ✅ |
| `getSpacing` | Static | - | `int` | Get spacing between toasts | ✅ |
| `setSpacing` | Static | `spacing: int` | - | Set spacing between toasts | ✅ |
| `getOffsetX` | Static | - | `int` | Get horizontal offset | ✅ |
| `setOffsetX` | Static | `offset_x: int` | - | Set horizontal offset | ✅ |
| `getOffsetY` | Static | - | `int` | Get vertical offset | ✅ |
| `setOffsetY` | Static | `offset_y: int` | - | Set vertical offset | ✅ |
| `getOffset` | Static | - | `tuple[int, int]` | Get both offsets | ✅ |
| `setOffset` | Static | `offset_x: int, offset_y: int` | - | Set both offsets | ✅ |
| `getPosition` | Static | - | `ToastPosition` | Get display position | ✅ |
| `setPosition` | Static | `position: ToastPosition` | - | Set display position | ✅ |
| `getPositionRelativeToWidget` | Static | - | `QWidget \| None` | Get reference widget | ✅ |
| `setPositionRelativeToWidget` | Static | `widget: QWidget \| None` | - | Set reference widget | ✅ |
| `isMovePositionWithWidget` | Static | - | `bool` | Check if follows widget | ✅ |
| `setMovePositionWithWidget` | Static | `on: bool` | - | Enable/disable widget following | ✅ |
| `isAlwaysOnMainScreen` | Static | - | `bool` | Check if forced to main screen | ✅ |
| `setAlwaysOnMainScreen` | Static | `on: bool` | - | Force display on main screen | ✅ |
| `getFixedScreen` | Static | - | `QScreen \| None` | Get fixed screen | ✅ |
| `setFixedScreen` | Static | `screen: QScreen \| None` | - | Set fixed screen | ✅ |
| `getCount` | Static | - | `int` | Get total toast count | ✅ |
| `getVisibleCount` | Static | - | `int` | Get visible toast count | ✅ |
| `getQueuedCount` | Static | - | `int` | Get queued toast count | ✅ |
| `reset` | Static | - | - | Reset all settings to defaults | ✅ |

## Functional Categories

### 📝 Basic Content & Display (12 methods)
- **Content**: `getTitle`, `setTitle`, `getText`, `setText`
- **Display Control**: `show`, `hide`, `getDuration`, `setDuration`
- **Duration Bar**: `isShowDurationBar`, `setShowDurationBar`, `setDurationBarValue`
- **Constructor**: `__init__`

### 🎨 Icon System (13 methods)
- **Basic Icon**: `getIcon`, `setIcon`, `isShowIcon`, `setShowIcon`
- **Icon Properties**: `getIconSize`, `setIconSize`, `getIconColor`, `setIconColor`
- **Icon Separator**: `isShowIconSeparator`, `setShowIconSeparator`, `getIconSeparatorWidth`, `setIconSeparatorWidth`, `getIconSeparatorColor`, `setIconSeparatorColor`

### ❌ Close Button System (13 methods)
- **Basic Button**: `getCloseButtonIcon`, `setCloseButtonIcon`, `isShowCloseButton`, `setShowCloseButton`
- **Button Size**: `getCloseButtonIconSize`, `setCloseButtonIconSize`, `getCloseButtonSize`, `setCloseButtonSize`
- **Dimensions**: `getCloseButtonWidth`, `setCloseButtonWidth`, `getCloseButtonHeight`, `setCloseButtonHeight`
- **Styling**: `getCloseButtonAlignment`, `setCloseButtonAlignment`, `getCloseButtonIconColor`, `setCloseButtonIconColor`

### 🎭 Animation & Behavior (10 methods)
- **Fade Effects**: `getFadeInDuration`, `setFadeInDuration`, `getFadeOutDuration`, `setFadeOutDuration`
- **Animation Direction Control**: `getAnimationDirection`, `setAnimationDirection`
- **Interaction Behavior**: `isResetDurationOnHover`, `setResetDurationOnHover`
- **Window Behavior**: `isStayOnTop`, `setStayOnTop`

### 🎨 Appearance & Colors (10 methods)
- **Shape**: `getBorderRadius`, `setBorderRadius`
- **Colors**: `getBackgroundColor`, `setBackgroundColor`, `getTitleColor`, `setTitleColor`, `getTextColor`, `setTextColor`, `getDurationBarColor`, `setDurationBarColor`

### 🔤 Font Configuration (12 methods)
- **Font Objects**: `getTitleFont`, `setTitleFont`, `getTextFont`, `setTextFont`
- **Font Sizes**: `getTitleFontSize`, `setTitleFontSize`, `getTextFontSize`, `setTextFontSize`, `setFontSize`
- **Font Families**: `setFontFamily`, `getTitleFontFamily`, `getTextFontFamily`

### 📐 Layout & Margins (14 methods)
- **Size Control**: `setFixedSize`, `setFixedWidth`, `setFixedHeight`
- **Modern Margin API**: `setMargins`, `getMargins`, `adjustMargins`
- **Compatibility Margins**: `setMarginLeft/Top/Right/Bottom`, `getMarginLeft/Top/Right/Bottom`
- **Spacing**: `getTextSectionSpacing`, `setTextSectionSpacing`

### ⚡ Advanced Features (2 methods)
- **Text Handling**: `isMultiline`, `setMultiline`
- **Style Presets**: `applyPreset`

### 🌐 Global Configuration (24 static methods)
- **Display Limits**: `getMaximumOnScreen`, `setMaximumOnScreen`
- **Positioning**: `getSpacing`, `setSpacing`, `getOffsetX/Y`, `setOffsetX/Y`, `getOffset`, `setOffset`
- **Position Control**: `getPosition`, `setPosition`, `getPositionRelativeToWidget`, `setPositionRelativeToWidget`
- **Widget Following**: `isMovePositionWithWidget`, `setMovePositionWithWidget`
- **Multi-Screen**: `isAlwaysOnMainScreen`, `setAlwaysOnMainScreen`, `getFixedScreen`, `setFixedScreen`
- **Queue Management**: `getCount`, `getVisibleCount`, `getQueuedCount`
- **System Control**: `reset`

## Preset Styles Comparison

| Preset | Icon | Icon Color | Duration Bar Color | Use Case |
|--------|------|------------|-------------------|----------|
| `SUCCESS` | ✅ Success | Green | Green | Successful operations |
| `SUCCESS_DARK` | ✅ Success | Green | Green | Success (dark theme) |
| `WARNING` | ⚠️ Warning | Orange/Yellow | Orange/Yellow | Warnings, cautions |
| `WARNING_DARK` | ⚠️ Warning | Orange/Yellow | Orange/Yellow | Warning (dark theme) |
| `ERROR` | ❌ Error | Red | Red | Errors, failures |
| `ERROR_DARK` | ❌ Error | Red | Red | Error (dark theme) |
| `INFORMATION` | ℹ️ Info | Blue | Blue | General information |
| `INFORMATION_DARK` | ℹ️ Info | Blue | Blue | Info (dark theme) |

**Usage Example:**
```python
toast.applyPreset(ToastPreset.SUCCESS)  # Green success style
toast.applyPreset(ToastPreset.ERROR_DARK)  # Red error style for dark themes
```

## Position Enumeration

| Position | Value | Description | Visual Location |
|----------|-------|-------------|-----------------|
| `BOTTOM_LEFT` | 1 | Bottom-left corner | ⬇️⬅️ |
| `BOTTOM_MIDDLE` | 2 | Bottom center | ⬇️ |
| `BOTTOM_RIGHT` | 3 | Bottom-right corner (default) | ⬇️➡️ |
| `TOP_LEFT` | 4 | Top-left corner | ⬆️⬅️ |
| `TOP_MIDDLE` | 5 | Top center | ⬆️ |
| `TOP_RIGHT` | 6 | Top-right corner | ⬆️➡️ |
| `CENTER` | 7 | Screen center | 🎯 |

**Usage Example:**
```python
Toast.setPosition(ToastPosition.TOP_RIGHT)  # Show toasts in top-right
Toast.setPosition(ToastPosition.CENTER)     # Show toasts in center
```

## Animation Direction Enumeration

| Direction | Value | Description | Slide Behavior |
|-----------|-------|-------------|----------------|
| `AUTO` | 0 | Automatic based on position (default) | ⬆️⬇️ Based on toast position |
| `FROM_TOP` | 1 | Slide from top | ⬇️ Slides down on show, up on hide |
| `FROM_BOTTOM` | 2 | Slide from bottom | ⬆️ Slides up on show, down on hide |
| `FROM_LEFT` | 3 | Slide from left | ➡️ Slides right on show, left on hide |
| `FROM_RIGHT` | 4 | Slide from right | ⬅️ Slides left on show, right on hide |
| `FADE_ONLY` | 5 | Pure opacity fade | 🌫️ No position movement, opacity only |

**Usage Example:**
```python
# Independent control of position and animation direction
Toast.setPosition(ToastPosition.TOP_RIGHT)  # Position in top-right
toast.setAnimationDirection(ToastAnimationDirection.FROM_LEFT)  # But slide from left

# Pure fade animation
toast.setAnimationDirection(ToastAnimationDirection.FADE_ONLY)  # No sliding

# Horizontal animations
toast.setAnimationDirection(ToastAnimationDirection.FROM_RIGHT)  # Slide from right

# Custom animation timing with horizontal sliding
toast = Toast()
toast.setTitle("Custom Animation")
toast.setText("Slow horizontal sliding effect")
toast.setAnimationDirection(ToastAnimationDirection.FROM_LEFT)
toast.setFadeInDuration(800)   # Slower slide-in
toast.setFadeOutDuration(600)  # Slower slide-out
toast.show()
```

### Close Button Alignment

| Alignment | Value | Description |
|-----------|-------|-------------|
| `TOP` | 1 | Align to top of toast |
| `MIDDLE` | 2 | Align to middle of toast |
| `BOTTOM` | 3 | Align to bottom of toast |

## Performance Optimizations

| Feature | Implementation | Benefit | Impact |
|---------|----------------|---------|--------|
| **URL Regex Caching** | Compiled regex stored as class attribute | Avoids recompilation on each URL conversion | 50-80% faster URL processing |
| **Stylesheet Caching** | Generated stylesheets cached by content hash | Prevents repeated string formatting | 70-80% faster style updates |
| **CSS File Caching** | CSS file read once and cached in memory | Eliminates repeated file I/O | 20-30% faster Toast creation |
| **Event Filter State Tracking** | Boolean flags track filter installation | Prevents redundant system calls | Improved responsiveness |
| **Animation Cleanup** | Proper animation object lifecycle management | Prevents memory leaks | Better long-term stability |
| **Icon Recoloring Simplification** | Simplified pixel-by-pixel processing | Cleaner, more maintainable code | Consistent performance across all image sizes |
| **Modern Margin API** | Flexible margin setting interface supporting multiple input formats | Reduces method call count, improves setting efficiency | Batch margin setting performance optimization |

### Performance Benchmarks

| Operation | Mean Time | Median Time | Min Time | Max Time | Std Dev | Iterations | Notes |
|-----------|-----------|-------------|----------|----------|---------|------------|-------|
| URL Conversion | 0.003ms | 0.003ms | 0.003ms | 0.016ms | 0.001ms | 1000x | Cached regex compilation |
| Icon Recoloring (16x16) | 0.384ms | 0.366ms | 0.351ms | 1.183ms | - | 100x | pixel-by-pixel method |
| Icon Recoloring (32x32) | 1.471ms | 1.430ms | 1.396ms | 2.843ms | - | 100x | pixel-by-pixel method |
| Icon Recoloring (64x64) | 5.870ms | 5.716ms | 5.626ms | 7.442ms | - | 100x | pixel-by-pixel method |
| Toast Creation | 7.598ms | 3.939ms | 3.621ms | 179.994ms | 24.883ms | 50x | Complete UI setup with caching |
| Stylesheet Update | 0.005ms | 0.005ms | 0.005ms | 0.052ms | 0.002ms | 1000x | With stylesheet caching |
| Layout Calculation | 1.732ms | 0.629ms | 0.615ms | 35.102ms | 4.075ms | 100x | Font metrics caching |

## Quick Usage Patterns

### Basic Toast
```python
toast = Toast()
toast.setTitle("Success")
toast.setText("Operation completed")
toast.show()
```

### Styled Toast with Preset
```python
toast = Toast()
toast.setTitle("Warning")
toast.setText("Please check your input")
toast.applyPreset(ToastPreset.WARNING)
toast.setDuration(5000)
toast.show()
```

### Global Configuration
```python
# Configure once for all toasts
Toast.setMaximumOnScreen(3)
Toast.setPosition(ToastPosition.TOP_RIGHT)
Toast.setSpacing(10)
Toast.setOffset(20, 50)
```

### Multi-Screen Setup
```python
# Force all toasts to main screen
Toast.setAlwaysOnMainScreen(True)

# Or use specific screen
screens = QGuiApplication.screens()
Toast.setFixedScreen(screens[1])  # Use second monitor
```

### Custom Styling
```python
toast = Toast()
toast.setTitle("Custom Toast")
toast.setText("With custom appearance")
toast.setBackgroundColor(QColor(50, 50, 50))
toast.setTitleColor(QColor(255, 255, 255))
toast.setTextColor(QColor(200, 200, 200))
toast.setBorderRadius(15)
toast.setDuration(0)  # Infinite duration
toast.show()
```

### Animation Direction Control
```python
# Basic horizontal sliding animation
toast = Toast()
toast.setTitle("Horizontal Slide")
toast.setText("Toast sliding from left")
toast.setAnimationDirection(ToastAnimationDirection.FROM_LEFT)
toast.applyPreset(ToastPreset.SUCCESS)
toast.show()

# Independent control of position and animation direction
Toast.setPosition(ToastPosition.TOP_RIGHT)  # Position in top-right
toast = Toast()
toast.setTitle("Independent Control")
toast.setText("Top-right position, left slide-in")
toast.setAnimationDirection(ToastAnimationDirection.FROM_LEFT)  # Slide from left
toast.show()

# Pure fade transition (no sliding)
toast = Toast()
toast.setTitle("Pure Fade")
toast.setText("Only opacity change, no position movement")
toast.setAnimationDirection(ToastAnimationDirection.FADE_ONLY)
toast.show()

# Custom animation timing with sliding effect
toast = Toast()
toast.setTitle("Custom Timing")
toast.setText("Slow sliding animation")
toast.setAnimationDirection(ToastAnimationDirection.FROM_RIGHT)
toast.setFadeInDuration(800)   # Slower slide-in
toast.setFadeOutDuration(600)  # Slower slide-out
toast.show()
```

### Modern Margin Settings
```python
toast = Toast()
toast.setTitle("Margin Example")
toast.setText("Demonstrating flexible margin settings")

# Simple setting - all margins the same
toast.setMargins(20)

# Precise setting - left, top, right, bottom
toast.setMargins((15, 10, 15, 20))

# Symmetric setting - horizontal, vertical
toast.setMargins((25, 15))

# Partial update - only modify specific margins
toast.setMargins({'left': 30, 'right': 35})

# Different component margins
toast.setMargins(10, 'icon')           # Icon margins
toast.setMargins(5, 'text_section')   # Text section margins

# Fine-tune margins
toast.adjustMargins(top=8, bottom=12)
toast.show()
```

---

**Note:** This table reference complements the detailed [Toast_API_Documentation.md](Toast_API_Documentation.md). For complete method descriptions, examples, and best practices, refer to the full documentation.
