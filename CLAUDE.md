# CLAUDE.md - MyNotes

## 项目简介

MyNotes 是一个 AI 日常规划助手。前端可直接打开 `MyNotes.html` 运行；后端为可选 FastAPI 服务，用于 AI 计划生成、复盘、RAG 资料问答、偏好记忆、Agent 工具定义和规划质量评估。没有 API key 时，前端和后端都提供 mock 结果，方便演示。

## 技术栈

- 前端：原生 HTML、CSS、JavaScript，非 ES Module
- 后端：Python FastAPI
- 数据：前端 `localStorage`，后端 SQLite
- AI：LLM API adapter + mock fallback
- RAG：轻量文本切片与关键词检索
- Agent：工具调用风格输出、偏好记忆、评估接口

## 入口与结构

```text
MyNotes.html
README.md
AGENTS.md
CLAUDE.md
assets/
docs/
  architecture.md
Dockerfile
backend/
  app/
    main.py
    schemas.py
    db.py
    services/
      agent.py
      evaluator.py
      llm.py
      memory.py
      rag.py
      tools.py
requirements.txt
.env.example
css/
  base.css
  nav.css
  calendar.css
  panel.css
  time-picker.css
js/
  helpers.js
  state.js
  storage.js
  lang.js
  notes.js
  timepicker.js
  calendar.js
  plans.js
  ai.js
  app.js
```

## 开发约定

- 保持原生前端实现，不引入框架或构建流程。
- JS 文件依赖加载顺序见 `MyNotes.html`，新增脚本时必须注意顺序。
- 全局状态集中在 `js/state.js`。
- 数据读写统一走 `js/storage.js`。
- 多语言文案维护在 `js/lang.js`，静态文本使用 `data-i18n` 和 `data-i18n-placeholder`。
- CSS 按模块维护，避免无关样式混入。
- README 中引用的截图放在 `assets/`。
- 后端接口保持在 `/api/agent/*`、`/api/rag/*`、`/api/memory/*`、`/api/eval/*`。
- 不提交 `.env`、数据库文件或虚拟环境。

## 数据键

- `my_notes_data`：每日规划数据
- `my_notes_lang`：语言偏好
- `note_{year}_{month}`：月备注

## AI 能力

- 目标拆解：长期目标生成阶段计划和今日任务。
- 动态复盘：根据当天完成情况生成建议。
- RAG 问答：对粘贴或入库的 JD/资料做轻量检索并返回片段。
- 偏好记忆：保存用户节奏，例如上午深度学习、晚上复盘。
- Agent 工具：暴露 `create_task`、`search_materials`、`summarize_week` 等工具定义。
- 质量评估：用测试案例对规划的可执行性、时间感、上下文和复盘闭环打分。

## 设计方向

整体风格参考 Apple Human Interface Guidelines：浅灰背景、毛玻璃卡片、清晰层级、克制动效。主色为 Apple Blue，完成状态使用绿色，删除/危险状态使用红色。

## 运行方式

直接打开：

```text
MyNotes.html
```

也可以用 VS Code Live Server 预览。

后端可选运行：

```bash
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

## Git

- 默认分支：`main`
- 远程仓库：`https://github.com/ab2956955606-cmyk/MyNotes`
- 提交前检查 `git status --short --branch`
