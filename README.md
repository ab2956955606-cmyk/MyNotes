<p align="center">
  <br>
  <strong>MyNotes</strong>
  <br>
  <span>一款安静、轻盈的 AI 日常规划助手</span>
  <br>
  <span>A quiet daily planner for notes, time, and completion.</span>
  <br><br>
  <a href="#中文">中文</a>
  <span>&nbsp;/&nbsp;</span>
  <a href="#english">English</a>
  <br><br>
  <img alt="Frontend" src="https://img.shields.io/badge/Frontend-HTML%20CSS%20JS-0a84ff">
  <img alt="Backend" src="https://img.shields.io/badge/Backend-FastAPI-30d158">
  <img alt="AI" src="https://img.shields.io/badge/AI-Agent%20RAG%20Memory-ff9f0a">
  <img alt="Storage" src="https://img.shields.io/badge/Storage-localStorage%20%2B%20SQLite-6e6e73">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-1d1d1f">
</p>

---

## 中文

**MyNotes** 是一款 AI 日常规划助手。它保留了轻量日历、每日规划、完成情况和月备注，也新增了 AI 目标拆解、日复盘、资料问答和一键写入计划能力。前端可以直接打开 `MyNotes.html` 运行；后端 FastAPI 服务是可选增强，用于真实 AI API、RAG 和 Agent 工具调用。

它的设计目标很简单：让日常计划变得轻一点。日历负责提供时间感，规划列表负责承载行动，完成记录负责留下回顾的痕迹。所有数据都保存在当前浏览器本地，适合个人、离线、轻量的日常使用。

### 界面预览

<p align="center">
  <img src="assets/mynotes-demo.png" alt="MyNotes 中文界面功能展示" width="860">
</p>

截图展示了 MyNotes 的主要功能：月历用于查看每天的计划状态，月备注用于保存阶段目标和提醒，规划列表可以记录时间、事项内容与完成情况，底部输入栏用于快速添加新的日程事项。

### ✨ 核心体验

| 模块 | 说明 |
| --- | --- |
| 📅 日历视图 | 按月查看日期，快速识别哪些天有规划、哪些天已经全部完成。 |
| ✅ 每日规划 | 为选中日期添加事项，支持时间、正文、完成勾选和删除。 |
| 🧾 完成情况 | 每条事项下方都可以记录执行结果，适合复盘和追踪。 |
| 📝 月备注 | 每个月拥有独立备注区，用来记录阶段目标、提醒或灵感。 |
| ✨ AI 规划 | 输入长期目标、截止日期和每天可用时间，生成阶段计划与今日任务。 |
| 🧠 RAG 问答 | 粘贴岗位 JD、学习资料或个人基础，返回相关片段和建议。 |
| 🧩 Agent 工具 | 后端暴露任务创建、资料检索、周总结等工具定义。 |
| 📊 评估体系 | 内置规划质量评估接口，按可执行性、时间感、上下文和复盘闭环打分。 |
| 🌐 双语界面 | 支持中文与 English 切换，语言偏好自动保存。 |
| 🔒 本地存储 | 数据写入 `localStorage`，关闭页面后仍会保留。 |

### 🚀 快速开始

```text
1. 下载或克隆项目
2. 用浏览器打开 MyNotes.html
3. 开始记录当天计划
```

项目没有安装步骤。你可以直接通过文件协议打开，也可以使用 VS Code Live Server 预览。

如果要启用后端 AI API：

```bash
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

默认接口地址为 `http://127.0.0.1:8000`。没有 API key 时，系统会使用 mock AI，仍然可以完整演示目标拆解、复盘和资料问答流程。

如果直接用文件方式打开 `MyNotes.html`，前端默认使用 Mock AI。需要让静态页面调用本地后端时，可在浏览器控制台执行：

```js
localStorage.setItem('my_notes_api_enabled', '1')
localStorage.setItem('my_notes_api_base', 'http://127.0.0.1:8000')
```

### 🧭 使用说明

**📅 日历**

- 点击顶部“日历”展开或折叠月历。
- 使用左右箭头切换月份。
- 点击任意日期，规划面板会切换到对应日期。
- 点击“今天”可以回到当前日期。
- 日期颜色代表状态：蓝色表示当天有未完成规划，绿色表示当天规划已全部完成，深色实心圆表示今天。

**✅ 规划**

- 在底部选择时间，输入事项内容。
- 点击加号按钮添加事项。
- 在输入框中按 `Enter` 也可以添加事项。
- 使用 `Shift + Enter`、`Ctrl + Enter` 或 `Command + Enter` 可以换行。
- 点击圆形勾选框标记完成。
- 鼠标悬停到事项上，可以显示删除按钮。

**🧾 完成情况**

每个事项下方都有独立的完成情况输入区。内容会自动保存，适合记录“做到了什么”“哪里没完成”“下一步怎么调整”。

**📝 月备注**

日历右侧的备注区按年月保存。切换月份时，应用会自动加载该月份的备注。

**🌐 语言切换**

- 点击右上角“中文 / EN”切换语言。
- 使用 `Ctrl + L` 或 `Command + L` 也可以快速切换。

**✨ AI 规划助手**

- 输入长期目标、截止日期、每天可用时间和资料约束。
- 点击“生成阶段计划”获得阶段拆解和今日建议任务。
- 点击“复盘今天”根据当天完成情况生成复盘建议。
- 点击“资料问答”对粘贴的 JD/资料做轻量 RAG 检索。
- 点击“保存偏好”记录用户节奏，例如上午深度学习、晚上复盘。
- 点击“运行评估”查看规划质量评分和测试案例。
- 点击“写入今天”把 AI 生成的任务加入当天计划。

### 🎨 设计语言

MyNotes 的视觉方向参考 Apple Human Interface Guidelines：克制、清晰、柔和。界面没有复杂装饰，重点放在信息层级、触控尺寸和阅读舒适度上。

| 设计项 | 实现 |
| --- | --- |
| 🔤 字体 | `-apple-system`、`SF Pro Display`、`PingFang SC` |
| 🌫️ 背景 | 浅灰系统底色，降低长时间使用的视觉负担 |
| 🧊 卡片 | 半透明毛玻璃质感，配合轻阴影分层 |
| 🔵 主色 | Apple Blue `#0a84ff` |
| 🟢 完成色 | System Green `#30d158` |
| 🔴 警示色 | System Red `#ff453a` |
| ◇ 图标 | 内嵌 SVG symbol，无外部图标库 |
| ⏱️ 动效 | 轻量过渡，优先保证操作反馈自然 |

### 💾 数据存储

所有数据都保存在当前浏览器的 `localStorage` 中。

| Key | 内容 |
| --- | --- |
| `my_notes_data` | 所有日期的规划数据 |
| `my_notes_lang` | 当前语言偏好 |
| `note_{year}_{month}` | 每个月的备注 |

请注意：数据不会自动同步到其他设备。清除浏览器数据、更换浏览器或更换设备后，原本的数据将不可见。

### 🗂️ 项目结构

```text
note/
├── MyNotes.html
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── Dockerfile
├── requirements.txt
├── .env.example
├── docs/
│   └── architecture.md
├── backend/
│   └── app/
│       ├── main.py
│       ├── schemas.py
│       ├── db.py
│       └── services/
│           ├── agent.py
│           ├── evaluator.py
│           ├── llm.py
│           ├── memory.py
│           ├── rag.py
│           └── tools.py
├── css/
│   ├── base.css
│   ├── nav.css
│   ├── calendar.css
│   ├── panel.css
│   └── time-picker.css
└── js/
    ├── app.js
    ├── state.js
    ├── helpers.js
    ├── storage.js
    ├── lang.js
    ├── notes.js
    ├── calendar.js
    ├── plans.js
    ├── ai.js
    └── timepicker.js
```

### 🛠️ 技术说明

MyNotes 的前端使用原生 HTML、CSS 和 JavaScript 编写。脚本通过 `<script>` 标签按顺序加载，不使用 ES Module、框架、包管理器或构建工具；后端作为可选增强，用 FastAPI 承载 Agent、RAG、Memory 和 Eval 能力。

```html
<script src="js/helpers.js"></script>
<script src="js/state.js"></script>
<script src="js/storage.js"></script>
<script src="js/lang.js"></script>
<script src="js/notes.js"></script>
<script src="js/timepicker.js"></script>
<script src="js/calendar.js"></script>
<script src="js/plans.js"></script>
<script src="js/ai.js"></script>
<script src="js/app.js"></script>
```

后端使用 FastAPI，核心接口：

| 接口 | 作用 |
| --- | --- |
| `POST /api/agent/plan` | 根据目标、时间和资料生成阶段计划 |
| `POST /api/agent/review` | 根据当天完成情况生成复盘建议 |
| `GET /api/agent/tools` | 查看 Agent 可调用工具定义 |
| `POST /api/memory/preferences` | 保存用户偏好记忆 |
| `POST /api/rag/ingest` | 将资料切片写入轻量 RAG 库 |
| `POST /api/rag/query` | 对资料/JD 做轻量检索问答 |
| `POST /api/eval/planner` | 运行规划质量评估 |
| `GET /api/health` | 健康检查 |

`.env.example` 中提供了模型配置项。默认 `AI_PROVIDER=mock`，可以接入 DeepSeek/OpenAI 兼容接口。

项目也提供 `Dockerfile` 和 [架构说明](docs/architecture.md)，方便把它作为 AI 应用作品集继续扩展和部署。

### 简历亮点

- 独立实现 AI 日常规划助手，覆盖目标拆解、日程生成、动态复盘、资料问答和质量评估。
- 前端保持轻量原生实现，后端使用 FastAPI 暴露 Agent/RAG/Memory/Eval API。
- 封装 `create_task`、`search_materials`、`summarize_week` 等 Agent 工具定义。
- 设计 mock fallback，保证无 API key 时也能完整演示产品闭环。
- 基于 localStorage 和 SQLite 分别承载前端任务数据与后端 AI 事件记录。

### 🌐 浏览器支持

推荐使用最新版 Chrome、Edge 或 Safari。界面使用了 `backdrop-filter`，较旧浏览器可能无法显示完整毛玻璃效果，但核心记录功能不受影响。

---

## English

**MyNotes** is an AI daily planner for personal notes, time-based tasks, and completion records. It keeps the lightweight calendar experience and adds AI goal decomposition, daily review, material QA, and one-click task insertion. The frontend can run directly from `MyNotes.html`; the optional FastAPI backend enables real LLM, RAG, and Agent workflows.

The product idea is intentionally small: make daily planning feel lighter. The calendar gives a sense of time, the plan list captures action, and completion notes preserve the details worth reviewing. Everything is stored locally in the current browser.

### Interface Preview

<p align="center">
  <img src="assets/mynotes-demo-en.png" alt="MyNotes English interface feature walkthrough" width="860">
</p>

The screenshot shows the English interface in use: the calendar summarizes monthly status, monthly notes keep goals and reminders, the plan list captures timed tasks, and completion notes preserve review details. The bottom input area is used to add new tasks quickly.

### ✨ Experience

| Area | Description |
| --- | --- |
| 📅 Calendar | Browse the month and understand daily progress at a glance. |
| ✅ Daily plans | Add tasks to a selected date with time, content, completion state, and deletion. |
| 🧾 Completion notes | Record the result of each task for reflection and follow-up. |
| 📝 Monthly notes | Keep month-level goals, reminders, or loose thoughts. |
| ✨ AI planning | Turn a long-term goal, deadline, and daily hours into phased tasks. |
| 🧠 RAG QA | Paste JDs or learning materials and retrieve relevant snippets. |
| 🧩 Agent tools | Backend exposes task creation, material search and weekly summary tools. |
| 📊 Evaluation | Built-in planner evaluation scores actionability, timing, context and review loop. |
| 🌐 Bilingual UI | Switch between Chinese and English with saved preference. |
| 🔒 Local first | Data is stored in `localStorage` and remains after closing the page. |

### 🚀 Quick Start

```text
1. Download or clone the project
2. Open MyNotes.html in your browser
3. Start planning your day
```

There is no installation step. You can open the file directly or preview it with VS Code Live Server.

To enable the backend AI API:

```bash
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

The default API base is `http://127.0.0.1:8000`. Without an API key, mock AI keeps the full planning, review, and retrieval demo available.

When opening `MyNotes.html` directly via file protocol, the frontend uses Mock AI by default. To call a local backend from the static page, run this in the browser console:

```js
localStorage.setItem('my_notes_api_enabled', '1')
localStorage.setItem('my_notes_api_base', 'http://127.0.0.1:8000')
```

### 🧭 How To Use

**📅 Calendar**

- Click “Calendar” in the top bar to expand or collapse the month view.
- Use the arrow buttons to switch months.
- Click any date to view and edit its plans.
- Click “Today” to return to the current date.
- Date colors show progress: blue means the day has unfinished plans, green means all plans are completed, and the dark filled circle marks today.

**✅ Plans**

- Pick a time and write a task at the bottom.
- Click the plus button to add it.
- Press `Enter` in the input field to add quickly.
- Use `Shift + Enter`, `Ctrl + Enter`, or `Command + Enter` for a new line.
- Click the circular checkbox to mark a task as completed.
- Hover over a task to reveal the delete button.

**🧾 Completion Notes**

Each task includes a dedicated completion note field. It autosaves while typing, making it useful for short reviews such as what was done, what changed, and what should happen next.

**📝 Monthly Notes**

The note area beside the calendar is stored per month. Switching months automatically loads the corresponding note.

**🌐 Language**

- Click “中文 / EN” in the top-right corner.
- Or use `Ctrl + L` / `Command + L` to switch quickly.

**✨ AI Planner**

- Enter a long-term goal, deadline, daily hours, and optional materials.
- Generate a phased plan and suggested tasks for today.
- Review today based on actual completion data.
- Ask pasted materials with a lightweight RAG flow.
- Save user preference memory such as morning deep work and evening review.
- Run planner quality evaluation with test cases.
- Apply generated tasks directly to today’s plan.

### 🎨 Visual Direction

MyNotes follows a quiet, Apple-inspired interface direction: soft surfaces, clear hierarchy, comfortable spacing, and minimal visual noise.

| Element | Implementation |
| --- | --- |
| 🔤 Font | `-apple-system`, `SF Pro Display`, `PingFang SC` |
| 🌫️ Background | Soft system gray for long-session comfort |
| 🧊 Cards | Translucent frosted surfaces with subtle shadows |
| 🔵 Accent | Apple Blue `#0a84ff` |
| 🟢 Completion | System Green `#30d158` |
| 🔴 Danger | System Red `#ff453a` |
| ◇ Icons | Inline SVG symbols, no external icon dependency |
| ⏱️ Motion | Gentle transitions for natural feedback |

### 💾 Storage

All data is saved in the current browser's `localStorage`.

| Key | Content |
| --- | --- |
| `my_notes_data` | All dated plan data |
| `my_notes_lang` | Current language preference |
| `note_{year}_{month}` | Monthly notes |

Data is not synced across devices. Clearing browser data, switching browsers, or moving to another device will make the local data unavailable.

### 🗂️ Project Structure

```text
note/
├── MyNotes.html
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── Dockerfile
├── requirements.txt
├── .env.example
├── docs/
│   └── architecture.md
├── backend/
│   └── app/
│       ├── main.py
│       ├── schemas.py
│       ├── db.py
│       └── services/
│           ├── agent.py
│           ├── evaluator.py
│           ├── llm.py
│           ├── memory.py
│           ├── rag.py
│           └── tools.py
├── css/
│   ├── base.css
│   ├── nav.css
│   ├── calendar.css
│   ├── panel.css
│   └── time-picker.css
└── js/
    ├── app.js
    ├── state.js
    ├── helpers.js
    ├── storage.js
    ├── lang.js
    ├── notes.js
    ├── calendar.js
    ├── plans.js
    ├── ai.js
    └── timepicker.js
```

### 🛠️ Technical Notes

The MyNotes frontend is built with plain HTML, CSS, and JavaScript. Scripts are loaded in order with regular `<script>` tags. There are no ES Modules, frontend frameworks, package managers, or build tools; the optional backend uses FastAPI for Agent, RAG, Memory, and Eval workflows.

```html
<script src="js/helpers.js"></script>
<script src="js/state.js"></script>
<script src="js/storage.js"></script>
<script src="js/lang.js"></script>
<script src="js/notes.js"></script>
<script src="js/timepicker.js"></script>
<script src="js/calendar.js"></script>
<script src="js/plans.js"></script>
<script src="js/ai.js"></script>
<script src="js/app.js"></script>
```

The backend exposes planning, review, memory, RAG ingestion/query, tool listing, and planner evaluation endpoints. `Dockerfile` and [architecture notes](docs/architecture.md) are included for deployment and portfolio review.

### 🌐 Browser Support

Latest Chrome, Edge, and Safari are recommended. Older browsers may not fully render the `backdrop-filter` glass effect, but the core planning features should remain usable.

---

## 📄 License

MIT License
