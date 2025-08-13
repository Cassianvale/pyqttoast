# Toast API 参考表格

本文档以表格形式提供 Toast 类 API 的快速参考。详细文档请参阅 [Toast_API_Documentation.md](Toast_API_Documentation.md)。

## ✨ API 特色功能

**现代化边距API** - 灵活高效 🚀
- **多格式支持**: 支持整数、元组、字典、QMargins等多种输入格式
- **统一接口**: 一个方法处理所有边距类型和组件
- **简洁调用**: 一行代码完成复杂边距设置
- **向后兼容**: 保留常用的传统方法

## 目录

- [方法快速参考](#方法快速参考)
- [功能分类](#功能分类)
- [预设样式对比](#预设样式对比)
- [位置枚举说明](#位置枚举说明)
- [动画方向枚举说明](#动画方向枚举说明)
- [性能优化特性](#性能优化特性)

## 方法快速参考

### 基本内容与显示方法

| 方法 | 类型 | 参数 | 返回值 | 描述 | show()后可调用? |
|------|------|------|--------|------|----------------|
| `__init__` | 实例 | `parent: QWidget \| None` | - | 创建新的 Toast 实例 | N/A |
| `show` | 实例 | - | - | 显示通知 | ❌ |
| `hide` | 实例 | - | - | 开始隐藏过程 | ✅ |
| `getTitle` | 实例 | - | `str` | 获取标题文本 | ✅ |
| `setTitle` | 实例 | `title: str` | - | 设置标题文本 | ❌ |
| `getText` | 实例 | - | `str` | 获取主要文本 | ✅ |
| `setText` | 实例 | `text: str` | - | 设置主要文本（自动链接URL） | ❌ |
| `getDuration` | 实例 | - | `int` | 获取持续时间（毫秒） | ✅ |
| `setDuration` | 实例 | `duration: int` | - | 设置持续时间（0 = 无限） | ❌ |
| `isShowDurationBar` | 实例 | - | `bool` | 检查是否显示持续时间条 | ✅ |
| `setShowDurationBar` | 实例 | `on: bool` | - | 启用/禁用持续时间条 | ❌ |
| `setDurationBarValue` | 实例 | `fraction: float` | - | 设置持续时间条进度（0.0-1.0） | ✅ |

### 图标配置方法

| 方法 | 类型 | 参数 | 返回值 | 描述 | show()后可调用? |
|------|------|------|--------|------|----------------|
| `getIcon` | 实例 | - | `QPixmap` | 获取当前图标 | ✅ |
| `setIcon` | 实例 | `icon: QPixmap \| ToastIcon` | - | 设置图标（像素图或枚举） | ❌ |
| `isShowIcon` | 实例 | - | `bool` | 检查是否显示图标 | ✅ |
| `setShowIcon` | 实例 | `on: bool` | - | 启用/禁用图标显示 | ❌ |
| `getIconSize` | 实例 | - | `QSize` | 获取图标尺寸 | ✅ |
| `setIconSize` | 实例 | `size: QSize` | - | 设置图标尺寸 | ❌ |
| `getIconColor` | 实例 | - | `QColor \| None` | 获取图标颜色 | ✅ |
| `setIconColor` | 实例 | `color: QColor \| None` | - | 设置图标重着色（None = 原色） | ❌ |
| `isShowIconSeparator` | 实例 | - | `bool` | 检查是否显示分隔符 | ✅ |
| `setShowIconSeparator` | 实例 | `on: bool` | - | 启用/禁用图标分隔符 | ❌ |
| `getIconSeparatorWidth` | 实例 | - | `int` | 获取分隔符宽度 | ✅ |
| `setIconSeparatorWidth` | 实例 | `width: int` | - | 设置分隔符宽度 | ❌ |
| `getIconSeparatorColor` | 实例 | - | `QColor` | 获取分隔符颜色 | ✅ |
| `setIconSeparatorColor` | 实例 | `color: QColor` | - | 设置分隔符颜色 | ❌ |

### 关闭按钮配置方法

| 方法 | 类型 | 参数 | 返回值 | 描述 | show()后可调用? |
|------|------|------|--------|------|----------------|
| `getCloseButtonIcon` | 实例 | - | `QPixmap` | 获取关闭按钮图标 | ✅ |
| `setCloseButtonIcon` | 实例 | `icon: QPixmap \| ToastIcon` | - | 设置关闭按钮图标 | ❌ |
| `isShowCloseButton` | 实例 | - | `bool` | 检查是否显示关闭按钮 | ✅ |
| `setShowCloseButton` | 实例 | `show: bool` | - | 启用/禁用关闭按钮 | ❌ |
| `getCloseButtonIconSize` | 实例 | - | `QSize` | 获取关闭按钮图标尺寸 | ✅ |
| `setCloseButtonIconSize` | 实例 | `size: QSize` | - | 设置关闭按钮图标尺寸 | ❌ |
| `getCloseButtonSize` | 实例 | - | `QSize` | 获取关闭按钮尺寸 | ✅ |
| `setCloseButtonSize` | 实例 | `size: QSize` | - | 设置关闭按钮尺寸 | ❌ |
| `getCloseButtonWidth` | 实例 | - | `int` | 获取关闭按钮宽度 | ✅ |
| `setCloseButtonWidth` | 实例 | `width: int` | - | 设置关闭按钮宽度 | ❌ |
| `getCloseButtonHeight` | 实例 | - | `int` | 获取关闭按钮高度 | ✅ |
| `setCloseButtonHeight` | 实例 | `height: int` | - | 设置关闭按钮高度 | ❌ |
| `getCloseButtonAlignment` | 实例 | - | `ToastButtonAlignment` | 获取按钮对齐方式 | ✅ |
| `setCloseButtonAlignment` | 实例 | `alignment: ToastButtonAlignment` | - | 设置按钮对齐（顶部/中间/底部） | ❌ |
| `getCloseButtonIconColor` | 实例 | - | `QColor \| None` | 获取关闭按钮图标颜色 | ✅ |
| `setCloseButtonIconColor` | 实例 | `color: QColor \| None` | - | 设置关闭按钮图标颜色 | ❌ |

### 动画与行为方法

| 方法 | 类型 | 参数 | 返回值 | 描述 | show()后可调用? |
|------|------|------|--------|------|----------------|
| `getFadeInDuration` | 实例 | - | `int` | 获取淡入持续时间（毫秒） | ✅ |
| `setFadeInDuration` | 实例 | `duration: int` | - | 设置淡入持续时间 | ❌ |
| `getFadeOutDuration` | 实例 | - | `int` | 获取淡出持续时间（毫秒） | ✅ |
| `setFadeOutDuration` | 实例 | `duration: int` | - | 设置淡出持续时间 | ❌ |
| `getAnimationDirection` | 实例 | - | `ToastAnimationDirection` | 获取动画方向 | ✅ |
| `setAnimationDirection` | 实例 | `direction: ToastAnimationDirection` | - | 设置滑动动画方向 | ❌ |
| `isResetDurationOnHover` | 实例 | - | `bool` | 检查悬停时是否重置持续时间 | ✅ |
| `setResetDurationOnHover` | 实例 | `on: bool` | - | 启用/禁用悬停重置 | ❌ |
| `isStayOnTop` | 实例 | - | `bool` | 检查是否保持在顶层 | ✅ |
| `setStayOnTop` | 实例 | `on: bool` | - | 启用/禁用保持在顶层 | ❌ |

### 外观定制方法

| 方法 | 类型 | 参数 | 返回值 | 描述 | show()后可调用? |
|------|------|------|--------|------|----------------|
| `getBorderRadius` | 实例 | - | `int` | 获取边框圆角 | ✅ |
| `setBorderRadius` | 实例 | `border_radius: int` | - | 设置边框圆角 | ❌ |
| `getBackgroundColor` | 实例 | - | `QColor` | 获取背景颜色 | ✅ |
| `setBackgroundColor` | 实例 | `color: QColor` | - | 设置背景颜色 | ❌ |
| `getTitleColor` | 实例 | - | `QColor` | 获取标题文本颜色 | ✅ |
| `setTitleColor` | 实例 | `color: QColor` | - | 设置标题文本颜色 | ❌ |
| `getTextColor` | 实例 | - | `QColor` | 获取主要文本颜色 | ✅ |
| `setTextColor` | 实例 | `color: QColor` | - | 设置主要文本颜色 | ❌ |
| `getDurationBarColor` | 实例 | - | `QColor` | 获取持续时间条颜色 | ✅ |
| `setDurationBarColor` | 实例 | `color: QColor` | - | 设置持续时间条颜色 | ❌ |

### 字体配置方法

| 方法 | 类型 | 参数 | 返回值 | 描述 | show()后可调用? |
|------|------|------|--------|------|----------------|
| `getTitleFont` | 实例 | - | `QFont` | 获取标题字体 | ✅ |
| `setTitleFont` | 实例 | `font: QFont` | - | 设置标题字体 | ❌ |
| `getTextFont` | 实例 | - | `QFont` | 获取文本字体 | ✅ |
| `setTextFont` | 实例 | `font: QFont` | - | 设置文本字体 | ❌ |
| `getTitleFontSize` | 实例 | - | `int` | 获取标题字体大小（点） | ✅ |
| `setTitleFontSize` | 实例 | `size: int` | - | 设置标题字体大小 | ❌ |
| `getTextFontSize` | 实例 | - | `int` | 获取文本字体大小（点） | ✅ |
| `setTextFontSize` | 实例 | `size: int` | - | 设置文本字体大小 | ❌ |
| `setFontSize` | 实例 | `title_size: int, text_size: int = None` | - | 设置两个字体大小 | ❌ |
| `setFontFamily` | 实例 | `family: str` | - | 设置两个字体族 | ❌ |
| `getTitleFontFamily` | 实例 | - | `str` | 获取标题字体族 | ✅ |
| `getTextFontFamily` | 实例 | - | `str` | 获取文本字体族 | ✅ |

### 布局与尺寸控制方法

| 方法 | 类型 | 参数 | 返回值 | 描述 | show()后可调用? |
|------|------|------|--------|------|----------------|
| `setFixedSize` | 实例 | `size: QSize` | - | 设置固定通知尺寸 | ❌ |
| `setFixedWidth` | 实例 | `width: int` | - | 设置固定通知宽度 | ❌ |
| `setFixedHeight` | 实例 | `height: int` | - | 设置固定通知高度 | ❌ |
| `getMargins` | 实例 | - | `QMargins` | 获取内容边距 | ✅ |
| `setMargins` | 实例 | `margins: QMargins` | - | 设置内容边距 | ❌ |
| `getMarginLeft/Top/Right/Bottom` | 实例 | - | `int` | 获取单个边距 | ✅ |
| `setMarginLeft/Top/Right/Bottom` | 实例 | `margin: int` | - | 设置单个边距 | ❌ |
| `getTextSectionSpacing` | 实例 | - | `int` | 获取标题-文本间距 | ✅ |
| `setTextSectionSpacing` | 实例 | `spacing: int` | - | 设置标题-文本间距 | ❌ |

### 边距管理方法 (11个方法)

| 方法 | 类型 | 参数 | 返回值 | 描述 | show()后可调用? |
|------|------|------|--------|------|----------------|
| **核心边距方法** |
| `setMargins` | 实例 | `margins, margin_type='content'` | - | 灵活设置边距，支持多种输入格式 | ❌ |
| `getMargins` | 实例 | `margin_type='content'` | `QMargins` | 获取指定类型的边距 | ✅ |
| `adjustMargins` | 实例 | `margin_type='content', **kwargs` | - | 微调指定边距的特定方向 | ❌ |
| **兼容性方法** |
| `setMarginLeft` | 实例 | `margin: int` | - | 设置内容左边距 | ❌ |
| `setMarginTop` | 实例 | `margin: int` | - | 设置内容上边距 | ❌ |
| `setMarginRight` | 实例 | `margin: int` | - | 设置内容右边距 | ❌ |
| `setMarginBottom` | 实例 | `margin: int` | - | 设置内容下边距 | ❌ |
| `getMarginLeft` | 实例 | - | `int` | 获取内容左边距 | ✅ |
| `getMarginTop` | 实例 | - | `int` | 获取内容上边距 | ✅ |
| `getMarginRight` | 实例 | - | `int` | 获取内容右边距 | ✅ |
| `getMarginBottom` | 实例 | - | `int` | 获取内容下边距 | ✅ |

#### setMargins 方法详细说明

`setMargins` 方法支持多种灵活的输入格式：

**参数说明：**
- `margins`: 边距值，支持以下格式：
  - `int`: 所有边距使用相同值，如 `setMargins(20)`
  - `tuple (4个元素)`: (左, 上, 右, 下)，如 `setMargins((10, 15, 20, 25))`
  - `tuple (2个元素)`: (水平, 垂直)，如 `setMargins((15, 10))`
  - `dict`: 部分更新，如 `setMargins({'left': 30, 'right': 40})`
  - `QMargins`: 标准边距对象，如 `setMargins(QMargins(10, 5, 10, 5))`
- `margin_type`: 边距类型，可选值：
  - `'content'` (默认): 内容边距
  - `'icon'`: 图标边距
  - `'icon_section'`: 图标区域边距
  - `'text_section'`: 文本区域边距
  - `'close_button'`: 关闭按钮边距

**使用示例：**
```python
# 基本用法
toast.setMargins(20)                    # 所有边距 20px
toast.setMargins((10, 15, 20, 25))      # 左上右下分别设置
toast.setMargins((15, 10))              # 水平15px，垂直10px

# 部分更新
toast.setMargins({'left': 30})          # 只更新左边距
toast.setMargins({'top': 5, 'bottom': 8}) # 更新上下边距

# 不同组件边距
toast.setMargins(15, 'icon')            # 设置图标边距
toast.setMargins(10, 'text_section')    # 设置文本区域边距

# 微调边距
toast.adjustMargins(left=25, right=30)  # 微调内容边距
toast.adjustMargins('icon', top=5)      # 微调图标上边距
```

### 高级功能方法

| 方法 | 类型 | 参数 | 返回值 | 描述 | show()后可调用? |
|------|------|------|--------|------|----------------|
| `isMultiline` | 实例 | - | `bool` | 检查是否启用多行 | ✅ |
| `setMultiline` | 实例 | `on: bool` | - | 启用/禁用多行文本 | ❌ |
| `applyPreset` | 实例 | `preset: ToastPreset` | - | 应用预定义样式预设 | ❌ |

### 静态配置方法

| 方法 | 类型 | 参数 | 返回值 | 描述 | show()后可调用? |
|------|------|------|--------|------|----------------|
| `getMaximumOnScreen` | 静态 | - | `int` | 获取最大同时显示数量 | ✅ |
| `setMaximumOnScreen` | 静态 | `maximum_on_screen: int` | - | 设置最大同时显示数量 | ✅ |
| `getSpacing` | 静态 | - | `int` | 获取通知间距 | ✅ |
| `setSpacing` | 静态 | `spacing: int` | - | 设置通知间距 | ✅ |
| `getOffsetX` | 静态 | - | `int` | 获取水平偏移 | ✅ |
| `setOffsetX` | 静态 | `offset_x: int` | - | 设置水平偏移 | ✅ |
| `getOffsetY` | 静态 | - | `int` | 获取垂直偏移 | ✅ |
| `setOffsetY` | 静态 | `offset_y: int` | - | 设置垂直偏移 | ✅ |
| `getOffset` | 静态 | - | `tuple[int, int]` | 获取两个偏移 | ✅ |
| `setOffset` | 静态 | `offset_x: int, offset_y: int` | - | 设置两个偏移 | ✅ |
| `getPosition` | 静态 | - | `ToastPosition` | 获取显示位置 | ✅ |
| `setPosition` | 静态 | `position: ToastPosition` | - | 设置显示位置 | ✅ |
| `getPositionRelativeToWidget` | 静态 | - | `QWidget \| None` | 获取参考组件 | ✅ |
| `setPositionRelativeToWidget` | 静态 | `widget: QWidget \| None` | - | 设置参考组件 | ✅ |
| `isMovePositionWithWidget` | 静态 | - | `bool` | 检查是否跟随组件 | ✅ |
| `setMovePositionWithWidget` | 静态 | `on: bool` | - | 启用/禁用组件跟随 | ✅ |
| `isAlwaysOnMainScreen` | 静态 | - | `bool` | 检查是否强制主屏幕 | ✅ |
| `setAlwaysOnMainScreen` | 静态 | `on: bool` | - | 强制在主屏幕显示 | ✅ |
| `getFixedScreen` | 静态 | - | `QScreen \| None` | 获取固定屏幕 | ✅ |
| `setFixedScreen` | 静态 | `screen: QScreen \| None` | - | 设置固定屏幕 | ✅ |
| `getCount` | 静态 | - | `int` | 获取通知总数 | ✅ |
| `getVisibleCount` | 静态 | - | `int` | 获取可见通知数 | ✅ |
| `getQueuedCount` | 静态 | - | `int` | 获取队列中通知数 | ✅ |
| `reset` | 静态 | - | - | 重置所有设置为默认值 | ✅ |

## 功能分类

### 📝 基本内容与显示 (12个方法)
- **内容**: `getTitle`, `setTitle`, `getText`, `setText`
- **显示控制**: `show`, `hide`, `getDuration`, `setDuration`
- **持续时间条**: `isShowDurationBar`, `setShowDurationBar`, `setDurationBarValue`
- **构造函数**: `__init__`

### 🎨 图标系统 (13个方法)
- **基本图标**: `getIcon`, `setIcon`, `isShowIcon`, `setShowIcon`
- **图标属性**: `getIconSize`, `setIconSize`, `getIconColor`, `setIconColor`
- **图标分隔符**: `isShowIconSeparator`, `setShowIconSeparator`, `getIconSeparatorWidth`, `setIconSeparatorWidth`, `getIconSeparatorColor`, `setIconSeparatorColor`

### ❌ 关闭按钮系统 (13个方法)
- **基本按钮**: `getCloseButtonIcon`, `setCloseButtonIcon`, `isShowCloseButton`, `setShowCloseButton`
- **按钮尺寸**: `getCloseButtonIconSize`, `setCloseButtonIconSize`, `getCloseButtonSize`, `setCloseButtonSize`
- **尺寸设置**: `getCloseButtonWidth`, `setCloseButtonWidth`, `getCloseButtonHeight`, `setCloseButtonHeight`
- **样式设置**: `getCloseButtonAlignment`, `setCloseButtonAlignment`, `getCloseButtonIconColor`, `setCloseButtonIconColor`

### 🎭 动画与行为 (10个方法)
- **淡入淡出效果**: `getFadeInDuration`, `setFadeInDuration`, `getFadeOutDuration`, `setFadeOutDuration`
- **动画方向控制**: `getAnimationDirection`, `setAnimationDirection`
- **交互行为**: `isResetDurationOnHover`, `setResetDurationOnHover`
- **窗口行为**: `isStayOnTop`, `setStayOnTop`

### 🎨 外观与颜色 (10个方法)
- **形状**: `getBorderRadius`, `setBorderRadius`
- **颜色**: `getBackgroundColor`, `setBackgroundColor`, `getTitleColor`, `setTitleColor`, `getTextColor`, `setTextColor`, `getDurationBarColor`, `setDurationBarColor`

### 🔤 字体配置 (12个方法)
- **字体对象**: `getTitleFont`, `setTitleFont`, `getTextFont`, `setTextFont`
- **字体大小**: `getTitleFontSize`, `setTitleFontSize`, `getTextFontSize`, `setTextFontSize`, `setFontSize`
- **字体族**: `setFontFamily`, `getTitleFontFamily`, `getTextFontFamily`

### 📐 布局与边距 (14个方法)
- **尺寸控制**: `setFixedSize`, `setFixedWidth`, `setFixedHeight`
- **现代边距API**: `setMargins`, `getMargins`, `adjustMargins`
- **兼容性边距**: `setMarginLeft/Top/Right/Bottom`, `getMarginLeft/Top/Right/Bottom`
- **间距**: `getTextSectionSpacing`, `setTextSectionSpacing`

### ⚡ 高级功能 (2个方法)
- **文本处理**: `isMultiline`, `setMultiline`
- **样式预设**: `applyPreset`

### 🌐 全局配置 (24个静态方法)
- **显示限制**: `getMaximumOnScreen`, `setMaximumOnScreen`
- **定位**: `getSpacing`, `setSpacing`, `getOffsetX/Y`, `setOffsetX/Y`, `getOffset`, `setOffset`
- **位置控制**: `getPosition`, `setPosition`, `getPositionRelativeToWidget`, `setPositionRelativeToWidget`
- **组件跟随**: `isMovePositionWithWidget`, `setMovePositionWithWidget`
- **多屏幕**: `isAlwaysOnMainScreen`, `setAlwaysOnMainScreen`, `getFixedScreen`, `setFixedScreen`
- **队列管理**: `getCount`, `getVisibleCount`, `getQueuedCount`
- **系统控制**: `reset`

## 预设样式对比

| 预设 | 图标 | 图标颜色 | 持续时间条颜色 | 使用场景 |
|------|------|----------|----------------|----------|
| `SUCCESS` | ✅ 成功 | 绿色 | 绿色 | 成功操作 |
| `SUCCESS_DARK` | ✅ 成功 | 绿色 | 绿色 | 成功（深色主题） |
| `WARNING` | ⚠️ 警告 | 橙色/黄色 | 橙色/黄色 | 警告、注意事项 |
| `WARNING_DARK` | ⚠️ 警告 | 橙色/黄色 | 橙色/黄色 | 警告（深色主题） |
| `ERROR` | ❌ 错误 | 红色 | 红色 | 错误、失败 |
| `ERROR_DARK` | ❌ 错误 | 红色 | 红色 | 错误（深色主题） |
| `INFORMATION` | ℹ️ 信息 | 蓝色 | 蓝色 | 一般信息 |
| `INFORMATION_DARK` | ℹ️ 信息 | 蓝色 | 蓝色 | 信息（深色主题） |

**使用示例:**
```python
toast.applyPreset(ToastPreset.SUCCESS)  # 绿色成功样式
toast.applyPreset(ToastPreset.ERROR_DARK)  # 深色主题红色错误样式
```

## 位置枚举说明

| 位置 | 值 | 描述 | 可视位置 |
|------|----|----- |----------|
| `BOTTOM_LEFT` | 1 | 左下角 | ⬇️⬅️ |
| `BOTTOM_MIDDLE` | 2 | 底部中央 | ⬇️ |
| `BOTTOM_RIGHT` | 3 | 右下角（默认） | ⬇️➡️ |
| `TOP_LEFT` | 4 | 左上角 | ⬆️⬅️ |
| `TOP_MIDDLE` | 5 | 顶部中央 | ⬆️ |
| `TOP_RIGHT` | 6 | 右上角 | ⬆️➡️ |
| `CENTER` | 7 | 屏幕中央 | 🎯 |

**使用示例:**
```python
Toast.setPosition(ToastPosition.TOP_RIGHT)  # 在右上角显示通知
Toast.setPosition(ToastPosition.CENTER)     # 在中央显示通知
```

## 动画方向枚举说明

| 方向 | 值 | 描述 | 滑动行为 |
|------|----|----- |----------|
| `AUTO` | 0 | 基于位置自动决定（默认） | ⬆️⬇️ 根据通知位置决定 |
| `FROM_TOP` | 1 | 从顶部滑入 | ⬇️ 显示时向下滑，隐藏时向上滑 |
| `FROM_BOTTOM` | 2 | 从底部滑入 | ⬆️ 显示时向上滑，隐藏时向下滑 |
| `FROM_LEFT` | 3 | 从左侧滑入 | ➡️ 显示时向右滑，隐藏时向左滑 |
| `FROM_RIGHT` | 4 | 从右侧滑入 | ⬅️ 显示时向左滑，隐藏时向右滑 |
| `FADE_ONLY` | 5 | 纯透明度渐变 | 🌫️ 无位置移动，仅透明度变化 |

**使用示例:**
```python
# 独立控制位置和动画方向
Toast.setPosition(ToastPosition.TOP_RIGHT)  # 位置在右上角
toast.setAnimationDirection(ToastAnimationDirection.FROM_LEFT)  # 但从左侧滑入

# 纯透明度渐变动画
toast.setAnimationDirection(ToastAnimationDirection.FADE_ONLY)  # 无滑动效果

# 水平动画效果
toast.setAnimationDirection(ToastAnimationDirection.FROM_RIGHT)  # 从右侧滑入

# 自定义动画时长的水平滑动
toast = Toast()
toast.setTitle("自定义动画")
toast.setText("慢速水平滑动效果")
toast.setAnimationDirection(ToastAnimationDirection.FROM_LEFT)
toast.setFadeInDuration(800)   # 较慢的滑入
toast.setFadeOutDuration(600)  # 较慢的滑出
toast.show()
```

### 关闭按钮对齐方式

| 对齐方式 | 值 | 描述 |
|----------|----|----- |
| `TOP` | 1 | 对齐到通知顶部 |
| `MIDDLE` | 2 | 对齐到通知中间 |
| `BOTTOM` | 3 | 对齐到通知底部 |

## 性能优化特性

| 功能 | 实现方式 | 优势 | 影响 |
|------|----------|------|------|
| **URL 正则表达式缓存** | 编译后的正则表达式存储为类属性 | 避免每次URL转换时重新编译 | URL处理速度提升50-80% |
| **样式表缓存** | 根据内容哈希缓存生成的样式表 | 防止重复字符串格式化 | 样式更新速度提升70-80% |
| **CSS文件缓存** | CSS文件一次读取并缓存在内存中 | 消除重复文件I/O | Toast创建速度提升20-30% |
| **事件过滤器状态跟踪** | 布尔标志跟踪过滤器安装状态 | 防止冗余系统调用 | 改善响应性 |
| **动画清理** | 适当的动画对象生命周期管理 | 防止内存泄漏 | 更好的长期稳定性 |
| **图标重着色简化** | 简化的像素级处理 | 更清洁、更易维护的代码 | 所有图像大小的一致性能 |
| **现代边距API** | 灵活的边距设置接口支持多种输入格式 | 减少方法调用次数，提升设置效率 | 批量边距设置性能优化 |

### 性能基准测试

| 操作 | 平均时间 | 中位数时间 | 最小时间 | 最大时间 | 标准差 | 迭代次数 | 备注 |
|------|----------|------------|----------|----------|--------|----------|------|
| URL转换 | 0.003ms | 0.003ms | 0.003ms | 0.016ms | 0.001ms | 1000次 | 缓存正则表达式编译 |
| 图标重着色 (16x16) | 0.384ms | 0.366ms | 0.351ms | 1.183ms | - | 100次 | 像素级处理方法 |
| 图标重着色 (32x32) | 1.471ms | 1.430ms | 1.396ms | 2.843ms | - | 100次 | 像素级处理方法 |
| 图标重着色 (64x64) | 5.870ms | 5.716ms | 5.626ms | 7.442ms | - | 100次 | 像素级处理方法 |
| Toast创建 | 7.598ms | 3.939ms | 3.621ms | 179.994ms | 24.883ms | 50次 | UI设置与缓存 |
| 样式表更新 | 0.005ms | 0.005ms | 0.005ms | 0.052ms | 0.002ms | 1000次 | 使用样式表缓存 |
| 布局计算 | 1.732ms | 0.629ms | 0.615ms | 35.102ms | 4.075ms | 100次 | 字体度量缓存 |

## 快速使用模式

### 基本通知
```python
toast = Toast()
toast.setTitle("成功")
toast.setText("操作已完成")
toast.show()
```

### 带预设样式的通知
```python
toast = Toast()
toast.setTitle("警告")
toast.setText("请检查您的输入")
toast.applyPreset(ToastPreset.WARNING)
toast.setDuration(5000)
toast.show()
```

### 全局配置
```python
# 为所有通知配置一次
Toast.setMaximumOnScreen(3)
Toast.setPosition(ToastPosition.TOP_RIGHT)
Toast.setSpacing(10)
Toast.setOffset(20, 50)
```

### 多屏幕设置
```python
# 强制所有通知显示在主屏幕
Toast.setAlwaysOnMainScreen(True)

# 或使用特定屏幕
screens = QGuiApplication.screens()
Toast.setFixedScreen(screens[1])  # 使用第二个显示器
```

### 自定义样式
```python
toast = Toast()
toast.setTitle("自定义通知")
toast.setText("具有自定义外观")
toast.setBackgroundColor(QColor(50, 50, 50))
toast.setTitleColor(QColor(255, 255, 255))
toast.setTextColor(QColor(200, 200, 200))
toast.setBorderRadius(15)
toast.setDuration(0)  # 无限持续时间
toast.show()
```

### 动画方向控制
```python
# 基本水平滑动动画
toast = Toast()
toast.setTitle("水平滑动")
toast.setText("从左侧滑入的通知")
toast.setAnimationDirection(ToastAnimationDirection.FROM_LEFT)
toast.applyPreset(ToastPreset.SUCCESS)
toast.show()

# 独立控制位置和动画方向
Toast.setPosition(ToastPosition.TOP_RIGHT)  # 位置在右上角
toast = Toast()
toast.setTitle("独立控制")
toast.setText("右上角位置，左侧滑入")
toast.setAnimationDirection(ToastAnimationDirection.FROM_LEFT)  # 从左侧滑入
toast.show()

# 纯透明度渐变（无滑动）
toast = Toast()
toast.setTitle("纯渐变")
toast.setText("仅透明度变化，无位置移动")
toast.setAnimationDirection(ToastAnimationDirection.FADE_ONLY)
toast.show()

# 自定义动画时长的滑动效果
toast = Toast()
toast.setTitle("自定义时长")
toast.setText("慢速滑动动画")
toast.setAnimationDirection(ToastAnimationDirection.FROM_RIGHT)
toast.setFadeInDuration(800)   # 较慢的滑入
toast.setFadeOutDuration(600)  # 较慢的滑出
toast.show()
```

### 现代边距设置
```python
toast = Toast()
toast.setTitle("边距示例")
toast.setText("展示灵活的边距设置")

# 简单设置 - 所有边距相同
toast.setMargins(20)

# 精确设置 - 左上右下
toast.setMargins((15, 10, 15, 20))

# 对称设置 - 水平垂直
toast.setMargins((25, 15))

# 部分更新 - 只修改特定边距
toast.setMargins({'left': 30, 'right': 35})

# 不同组件边距
toast.setMargins(10, 'icon')           # 图标边距
toast.setMargins(5, 'text_section')   # 文本区域边距

# 微调边距
toast.adjustMargins(top=8, bottom=12)
toast.show()
```

---

**注意:** 此表格参考补充了详细的 [Toast_API_Documentation.md](Toast_API_Documentation.md)。有关完整的方法描述、示例和最佳实践，请参阅完整文档。
