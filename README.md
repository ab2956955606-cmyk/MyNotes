<p align="center">
  <a href="#readme-zh">🇨🇳 中文</a> &nbsp;·&nbsp; <a href="#readme-en">🇬🇧 English</a>
</p>

---

<h1 align="center" id="readme-zh">📝 我的笔记 — MyNotes</h1>

<p align="center">
  一款风格简洁的个人日常笔记工具。<br>
  以日期为中心，帮助你管理每日规划、追踪完成情况，并通过日历概览全局。
</p>

<p align="center">
  <strong>⌨️ <code>Ctrl+L</code> / <code>⌘L</code> 一键中英文切换</strong>
</p>

---

## ✨ 特色

- **每日规划** — 按时间列出待办事项，支持勾选完成
- **完成追踪** — 每项规划可填写完成情况，一目了然
- **日历总览** — 月视图一眼看清各天的状态（🔵 待完成 / 🟢 全部完成）
- **折叠日历** — 点击「日历」展开或收起，腾出更多编辑空间
- **月备注** — 每个月份可以写一段备注，切换月份自动切换
- **中英文切换** — 右上角「中文 / EN」切换，或按 <kbd>Ctrl</kbd>+<kbd>L</kbd> / <kbd>⌘</kbd>+<kbd>L</kbd>
- **纯前端** — 无需安装、无需后端，浏览器直接打开即用
- **本地持久化** — 所有数据存储在浏览器的 `localStorage` 中

## 🎨 设计理念

| 要素 | 实现方式 |
|------|----------|
| 字体 | `-apple-system` / `SF Pro Display` / `PingFang SC` |
| 背景色 | `#f2f2f6` — iOS 系统灰 |
| 卡片 | `backdrop-filter: blur(16px)` — 毛玻璃效果 |
| 强调色 | `#007aff` — Apple Blue |
| 圆角 | `20px` / `14px` / `10px` 层次化圆角体系 |
| 阴影 | 极轻阴影 `0 4px 24px rgba(0,0,0,0.04)` |
| 动效 | 过渡动画 200–350ms `ease` / `cubic-bezier` |

## 🚀 快速开始

1. 下载或克隆本仓库
2. 用浏览器直接打开 `index.html`
3. 开始记录！

> 无需 `npm install`、无需构建工具、无需后端服务器。

## 🧭 功能指南

### 导航栏
- 左侧：应用标题 + 笔记图标
- 右侧：语言切换 + 当前选中日期 + **「今天」** 按钮（一键跳回今天）

### 📅 日历
- 点击 **「日历 ▾」** 展开或折叠月视图
- 左右箭头 `‹` `›` 切换月份
- 日期颜色标记：
  - **蓝色** `#007aff` — 该天有规划但未全部完成
  - **绿色** `#34c759` — 该天所有规划已完成
- 点击某天 → 日历保持展开，下方显示该天的规划和完成情况
- 当天带蓝色实心圆高亮

### 📋 规划与完成情况
- **添加规划**：在底部输入时间和事项，点击 `+` 或按 `Enter`
- **序号**：每个规划项左侧自动编号 ① ② ③…
- **勾选**：点击圆形勾选框标记完成，序号和文字变绿
- **完成情况**：每项规划下方可填写详情
- **删除**：鼠标悬停时出现 ✕ 按钮

### 🕐 时间选择器
- 小时与分钟分列，中间 `:` 分隔
- 选中值蓝色高亮放大，滚动无限循环
- 点击「完成」确认选择

### 📝 备注
- 日历右侧的备注区，每个月份独立存储
- 输入自动保存，切换月份自动加载

### 🎯 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| <kbd>Ctrl</kbd>+<kbd>L</kbd> / <kbd>⌘</kbd>+<kbd>L</kbd> | 切换中英文 |

## 💾 数据存储

所有数据存储在浏览器本地：

```
localStorage
├── my_notes_data        → 所有日期的规划数据（JSON）
├── my_notes_lang        → 语言偏好（zh / en）
├── note_2026_6          → 2026 年 6 月的备注
├── note_2026_7          → 2026 年 7 月的备注
└── …
```

> ⚠️ 数据不会跨设备同步。清除浏览器数据会导致笔记丢失。

## 🌐 浏览器支持

| 浏览器 | 兼容性 |
|--------|--------|
| Safari 15+ | ✅ 最佳（原生支持毛玻璃） |
| Chrome 90+ | ✅ |
| Edge 90+ | ✅ |
| Firefox 100+ | ⚠️ 毛玻璃效果略不同 |

## 🗂️ 项目结构

```
note/
├── index.html          ← 入口页面（仅 HTML 骨架 + 模块引用）
├── README.md           ← 本文件
│
├── css/                ← 样式文件（按功能拆分）
│   ├── base.css        ←   全局重置、字体、容器
│   ├── nav.css         ←   顶部导航栏
│   ├── calendar.css    ←   日历卡片、网格、标记
│   ├── panel.css       ←   规划面板、列表项、添加区域
│   └── time-picker.css ←   自定义时间选择器
│
├── js/                 ← 脚本模块
│   ├── app.js          ←   应用入口：协调各模块初始化
│   ├── state.js        ←   全局状态变量
│   ├── helpers.js      ←   工具函数
│   ├── storage.js      ←   数据持久化层（localStorage）
│   ├── lang.js         ←   多语言包 + 中英文切换（含键盘快捷键）
│   ├── notes.js        ←   月备注功能
│   ├── calendar.js     ←   日历渲染与导航
│   ├── plans.js        ←   规划增删改查 + 完成情况
│   └── timepicker.js   ←   时间选择器组件
│
└── .git/
```

## 💡 设计说明

本应用遵循 Apple Human Interface Guidelines 的核心原则：

- **Deference** — 内容优先，界面后退。毛玻璃和极简配色让规划内容成为视觉焦点
- **Clarity** — 清晰的层级结构：日历 → 规划列表 → 完成情况，从上到下自然浏览
- **Depth** — 通过毛玻璃、阴影和层级切换营造空间感，让交互有层次

---

<h1 align="center" id="readme-en">📝 MyNotes</h1>

<p align="center">
  A clean, daily note-taking tool for personal use.<br>
  Date-centric — manage your daily plans, track completion status, and get a bird's-eye view through the calendar.
</p>

<p align="center">
  <strong>⌨️ Press <code>Ctrl+L</code> / <code>⌘L</code> to toggle Chinese / English</strong>
</p>

---

## ✨ Features

- **Daily Plans** — List tasks by time, check them off when done
- **Completion Tracking** — Write completion notes for each task
- **Calendar Overview** — Monthly view shows each day's status at a glance (🔵 pending / 🟢 all done)
- **Collapsible Calendar** — Click "Calendar" to expand or collapse
- **Monthly Notes** — Write notes per month, auto-switches when browsing months
- **Language Toggle** — Switch between Chinese & English via the top-right toggle or <kbd>Ctrl</kbd>+<kbd>L</kbd> / <kbd>⌘</kbd>+<kbd>L</kbd>
- **Pure Frontend** — No installation, no backend, just open in a browser
- **Local Persistence** — All data stored in browser `localStorage`

## 🎨 Design Philosophy

| Element | Implementation |
|---------|----------------|
| Font | `-apple-system` / `SF Pro Display` / `PingFang SC` |
| Background | `#f2f2f6` — iOS System Gray |
| Cards | `backdrop-filter: blur(16px)` — Frosted glass |
| Accent | `#007aff` — Apple Blue |
| Radius | `20px` / `14px` / `10px` layered radii |
| Shadow | Subtle `0 4px 24px rgba(0,0,0,0.04)` |
| Motion | 200–350ms `ease` / `cubic-bezier` transitions |

## 🚀 Quick Start

1. Download or clone this repo
2. Open `index.html` in your browser
3. Start taking notes!

> No `npm install`, no build tools, no backend server required.

## 🧭 Feature Guide

### Navigation Bar
- Left: App title + note icon
- Right: Language toggle + selected date + **"Today"** button (jump back to today)

### 📅 Calendar
- Click **"Calendar ▾"** to expand/collapse the month view
- Arrow buttons `‹` `›` to switch months
- Date color indicators:
  - **Blue** `#007aff` — tasks exist but not all completed
  - **Green** `#34c759` — all tasks completed for that day
- Click a date → calendar stays open, shows that day's plans below
- Today is highlighted with a blue dot

### 📋 Plans & Completion
- **Add Plan**: Enter a time and task at the bottom, click `+` or press `Enter`
- **Numbering**: Each plan is auto-numbered ① ② ③…
- **Check Off**: Click the circle to mark complete, number and text turn green
- **Completion**: Write detailed completion notes under each task
- **Delete**: Hover to reveal the ✕ button

### 🕐 Time Picker
- Hours and minutes in separate columns with `:` separator
- Selected value highlighted in blue with scale animation, infinite scroll
- Click "Done" to confirm

### 📝 Notes
- Notes area beside the calendar, stored independently per month
- Auto-saves on input, auto-loads when switching months

### 🎯 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| <kbd>Ctrl</kbd>+<kbd>L</kbd> / <kbd>⌘</kbd>+<kbd>L</kbd> | Toggle Chinese / English |

## 💾 Data Storage

All data is stored in browser local storage:

```
localStorage
├── my_notes_data        → All plan data (JSON)
├── my_notes_lang        → Language preference (zh / en)
├── note_2026_6          → Notes for June 2026
├── note_2026_7          → Notes for July 2026
└── …
```

> ⚠️ Data is not synced across devices. Clearing browser data will delete your notes.

## 🌐 Browser Support

| Browser | Compatibility |
|---------|---------------|
| Safari 15+ | ✅ Best (native frosted glass support) |
| Chrome 90+ | ✅ |
| Edge 90+ | ✅ |
| Firefox 100+ | ⚠️ Frosted glass may differ slightly |

## 🗂️ Project Structure

```
note/
├── index.html          ← Entry point (HTML skeleton + module references)
├── README.md           ← This file
│
├── css/                ← Stylesheets (split by feature)
│   ├── base.css        ←   Global reset, fonts, container
│   ├── nav.css         ←   Navigation bar
│   ├── calendar.css    ←   Calendar card, grid, markers
│   ├── panel.css       ←   Plans panel, list items, add area
│   └── time-picker.css ←   Custom time picker
│
├── js/                 ← Script modules
│   ├── app.js          ←   App entry: coordinate module initialization
│   ├── state.js        ←   Global state variables
│   ├── helpers.js      ←   Utility functions
│   ├── storage.js      ←   Data persistence layer (localStorage)
│   ├── lang.js         ←   Language pack + toggle (with keyboard shortcut)
│   ├── notes.js        ←   Monthly notes
│   ├── calendar.js     ←   Calendar rendering & navigation
│   ├── plans.js        ←   Plans CRUD + completion
│   └── timepicker.js   ←   Time picker component
│
└── .git/
```

## 💡 Design Notes

This app follows the core principles of the Apple Human Interface Guidelines:

- **Deference** — Content first, interface recedes. Frosted glass and minimal colors keep plans as the focal point
- **Clarity** — Clear hierarchy: Calendar → Plans → Completion, natural top-to-bottom browsing
- **Depth** — Spatial depth through frosted glass, shadows, and layered transitions

---

## 📄 License

MIT License — feel free to use, modify, and share.

---

<p align="center">
  <em>Made with ❤️ and a bit of Apple spirit.</em>
</p>
