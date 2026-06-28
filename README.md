<p align="center">
  <img src="https://img.shields.io/badge/status-active-brightgreen" />
  <img src="https://img.shields.io/badge/frontend-pure-007aff" />
  <img src="https://img.shields.io/badge/license-MIT-blue" />
</p>

<h1 align="center">📝 我的笔记 — MyNotes</h1>

<p align="center">
  一款纯前端、无需后端的个人日常规划工具，<br>
  以日期为中心管理每日待办，通过月历概览全局。
</p>

<p align="center">
  <strong>⌨️ <kbd>Ctrl</kbd>+<kbd>L</kbd> / <kbd>⌘</kbd>+<kbd>L</kbd> 一键中英文切换</strong>
</p>

---

## 🚀 快速开始

1. 下载或克隆本仓库
2. 用浏览器直接打开 `index.html`
3. 开始记录！

> 无需 `npm install`、无需构建工具、无需后端服务器。

---

## ✨ 功能

### 📅 日历
- 点击 **「日历 ▾」** 展开或折叠月视图
- 左右箭头 `‹` `›` 切换月份
- 日期颜色标记：
  - **蓝色** `#007aff` — 该天有规划但未全部完成
  - **绿色** `#34c759` — 该天所有规划已完成
- 当天带蓝色实心圆高亮
- 点击日期：日历保持展开，下方显示该天的规划

### 📋 规划与完成情况
- **添加规划**：在底部输入时间和事项，按 `+` 或 `Enter` 提交
- **序号**：每个规划项左侧自动编号 ① ② ③…
- **勾选**：点击圆形勾选框标记完成，序号和文字变绿+删除线
- **完成情况**：每项规划下方可填写完成详情，自动保存
- **删除**：鼠标悬停时出现 ✕ 按钮

### 🕐 时间选择器
- 选中值蓝色高亮放大，滚动无限循环
- 点击「完成」确认选择

### 📝 备注
- 日历右侧的备注区，每个月份独立存储
- 输入自动保存，切换月份自动加载

### 🌐 中英文切换
- 点击右上角 **「中文 / EN」** 切换
- 或使用键盘快捷键 <kbd>Ctrl</kbd>+<kbd>L</kbd> / <kbd>⌘</kbd>+<kbd>L</kbd>
- 语言偏好自动保存到 `localStorage`

### 🎛️ 其他
- **「今天」** 按钮一键跳回当前日期
- 所有数据存储在浏览器本地，关闭页面不丢失

---

## 🎨 设计

| 要素 | 实现 |
|------|------|
| 字体 | `-apple-system` / `SF Pro Display` / `PingFang SC` |
| 背景色 | `#f2f2f6` — iOS 系统灰 |
| 卡片 | `backdrop-filter: blur(16px)` — 毛玻璃效果 |
| 强调色 | `#007aff` — Apple Blue |
| 圆角 | `20px` / `14px` / `10px` 层次化圆角体系 |
| 阴影 | `0 4px 24px rgba(0,0,0,0.04)` 极轻阴影 |
| 动效 | 过渡动画 200–350ms `ease` / `cubic-bezier` |

---

## 💾 数据存储

所有数据存储在浏览器 `localStorage`：

| Key | 内容 |
|-----|------|
| `my_notes_data` | 所有日期的规划数据（JSON） |
| `my_notes_lang` | 语言偏好（`zh` / `en`） |
| `note_{year}_{month}` | 各月备注 |

> ⚠️ 数据不会跨设备同步。清除浏览器数据会导致笔记丢失。

---

## 🗂️ 项目结构

```
note/
├── index.html            ← 入口页面
├── README.md             ← 本文件
│
├── css/
│   ├── base.css          ← 全局重置、字体、容器布局
│   ├── nav.css           ← 顶部导航栏 + 语言切换
│   ├── calendar.css      ← 日历卡片、网格、颜色标记
│   ├── panel.css         ← 规划面板、列表项、添加区域
│   └── time-picker.css   ← 时间选择器组件样式
│
└── js/
    ├── app.js            ← 应用入口：模块初始化协调
    ├── state.js          ← 全局状态变量
    ├── helpers.js        ← 工具函数
    ├── storage.js        ← 数据持久化层
    ├── lang.js           ← 多语言包 + 中英文切换
    ├── notes.js          ← 月备注功能
    ├── calendar.js       ← 日历渲染与导航
    ├── plans.js          ← 规划增删改查 + 完成情况
    └── timepicker.js     ← 时间选择器组件
```

---

## 🌐 浏览器支持

| Safari 15+ | Chrome 90+ | Edge 90+ | 
|:----------:|:----------:|:--------:|
| ✅ 最佳 | ✅ | ✅ |

---

## 📄 许可

MIT License — 随意使用、修改、分享。


