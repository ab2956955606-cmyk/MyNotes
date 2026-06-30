/* ============ 语言包 ============ */

const langStrings = {
  zh: {
    navTitle: '我的笔记',
    navToggle: '日历',
    btnToday: '今天',
    panelTitle: '规划与完成情况',
    notesLabel: '备注',
    notesPlaceholder: '这个月的备注…',
    completionLabel: '完成情况',
    completionPlaceholder: '写下完成情况…',
    addPlaceholder: '添加事项…',
    deletePlan: '删除事项',
    tpConfirm: '完成',
    aiTitle: 'AI 规划助手',
    aiSubtitle: '把长期目标拆成日程，按完成情况复盘和调整。',
    aiGoalLabel: '长期目标',
    aiGoalPlaceholder: '例如：3 个月内拿到北京 AI 应用开发实习',
    aiDeadlineLabel: '截止日期',
    aiHoursLabel: '每天可用时间',
    aiContextLabel: '资料 / JD / 约束',
    aiContextPlaceholder: '粘贴岗位 JD、课程资料、个人基础或时间限制，AI 会基于这些内容制定计划。',
    aiPreferenceLabel: '偏好记忆',
    aiPreferencePlaceholder: '例如：上午适合深度学习，晚上适合复盘，周末可以安排长任务。',
    aiGenerate: '生成阶段计划',
    aiReview: '复盘今天',
    aiSearch: '资料问答',
    aiMemory: '保存偏好',
    aiEval: '运行评估',
    aiApply: '写入今天',
    aiEmpty: '输入目标后生成计划；没有后端或 API key 时会使用本地模拟结果。',
    aiLoading: 'AI 正在思考…',
    aiGenerated: '生成结果',
    aiTodayTasks: '今日建议任务',
    aiApplied: '已写入今天的规划',
    aiFallbackGoal: '提升 AI 应用开发能力',
    aiFallbackWithContext: '已结合资料/JD 约束。',
    aiFallbackNoContext: '建议补充 JD 或学习资料，计划会更个性化。',
    aiPlanSummary: '围绕“{goal}”生成计划，每天约 {hours} 小时。',
    aiPhase1: '阶段一：定位差距',
    aiPhase1Detail: '梳理目标岗位要求、已有基础和最短补齐路径。',
    aiPhase2: '阶段二：项目冲刺',
    aiPhase2Detail: '围绕 AI 应用、Agent、RAG 和部署形成可展示成果。',
    aiPhase3: '阶段三：复盘投递',
    aiPhase3Detail: '用日报/周报追踪完成度，并迭代简历表达。',
    aiTaskResearch: '分析目标岗位 JD 与能力差距',
    aiTaskBuild: '实现一个可展示的 AI 应用功能',
    aiTaskBuildReason: '项目能力比单纯学习记录更适合简历展示。',
    aiTaskReview: '复盘今日完成情况并调整明日计划',
    aiTaskReviewReason: '动态调整能体现 Agent/规划助手的产品闭环。',
    aiFallbackRationale: '计划按“理解目标、输出成果、持续复盘”的路径安排。',
    aiReviewSummary: '今天完成 {done}/{total} 项。',
    aiReviewSuggestion1: '保留已完成事项作为复盘证据。',
    aiReviewSuggestion2: '未完成事项优先判断是任务过大还是时间估计偏差。',
    aiReviewSuggestion3: '建议把未完成事项拆成更小的下一步。',
    aiReviewSuggestionEmpty: '今天还没有规划，可以先生成一组 AI 建议任务。',
    aiSearchNoContext: '暂无资料，可粘贴 JD、课程或笔记。',
    aiSearchAnswer: '基于当前资料，优先关注这些信息片段。',
    aiSource: '来源',
    aiMemorySaved: '偏好记忆已保存',
    aiMemoryEmpty: '暂无偏好，后续计划会按默认节奏生成。',
    aiEvalScore: '规划质量评估',
    aiEvalCase1: '目标明确且时间有限',
    aiEvalCase2: '用户有岗位 JD 资料',
    aiEvalCase3: '用户需要根据未完成事项动态调整',
    aiEvalReasonStrong: '覆盖时间、上下文和复盘闭环。',
    aiEvalReasonGood: '可用，但还可以加入更多量化指标。',
    emptyPlans: '暂无规划',
    emptyAddHint: '在下方添加今日事项',
    todayLabel: '今天',
    items: '{n} 项',
    monthFormat: '{y}年{m}月',
    dateFormat: '{y}年{m}月{d}日',
    weekdayShort: ['一','二','三','四','五','六','日'],
    weekdayNames: ['日','一','二','三','四','五','六'],
    dateLabel: '{m}月{d}日 星期{w}',
  },
  en: {
    navTitle: 'My Notes',
    navToggle: 'Calendar',
    btnToday: 'Today',
    panelTitle: 'Plans & Completion',
    notesLabel: 'Notes',
    notesPlaceholder: 'Notes for this month…',
    completionLabel: 'Completion',
    completionPlaceholder: 'Write completion notes…',
    addPlaceholder: 'Add a task…',
    deletePlan: 'Delete task',
    tpConfirm: 'Done',
    aiTitle: 'AI Planner',
    aiSubtitle: 'Turn long-term goals into schedules, reviews, and adjustments.',
    aiGoalLabel: 'Long-term goal',
    aiGoalPlaceholder: 'Example: land a Beijing AI application internship in 3 months',
    aiDeadlineLabel: 'Deadline',
    aiHoursLabel: 'Daily hours',
    aiContextLabel: 'Materials / JD / Constraints',
    aiContextPlaceholder: 'Paste job descriptions, learning materials, current skills, or time limits.',
    aiPreferenceLabel: 'Preference memory',
    aiPreferencePlaceholder: 'Example: deep work in the morning, review at night, longer tasks on weekends.',
    aiGenerate: 'Generate plan',
    aiReview: 'Review today',
    aiSearch: 'Ask materials',
    aiMemory: 'Save memory',
    aiEval: 'Run eval',
    aiApply: 'Apply to today',
    aiEmpty: 'Enter a goal to generate a plan. Without backend or API key, local mock AI is used.',
    aiLoading: 'AI is thinking…',
    aiGenerated: 'Generated result',
    aiTodayTasks: 'Suggested tasks for today',
    aiApplied: 'Added to today’s plan',
    aiFallbackGoal: 'improve AI application development skills',
    aiFallbackWithContext: 'Context and JD constraints are included.',
    aiFallbackNoContext: 'Add a JD or learning material for a more personalized plan.',
    aiPlanSummary: 'Plan generated for “{goal}”, about {hours} hours per day.',
    aiPhase1: 'Phase 1: map the gap',
    aiPhase1Detail: 'Compare target role requirements with current skills.',
    aiPhase2: 'Phase 2: build portfolio',
    aiPhase2Detail: 'Ship visible AI app, Agent, RAG, and deployment features.',
    aiPhase3: 'Phase 3: review and apply',
    aiPhase3Detail: 'Track daily/weekly progress and refine resume wording.',
    aiTaskResearch: 'Analyze target JD and skill gaps',
    aiTaskBuild: 'Implement one demonstrable AI feature',
    aiTaskBuildReason: 'Project evidence is stronger than a learning checklist.',
    aiTaskReview: 'Review today and adjust the next plan',
    aiTaskReviewReason: 'Dynamic adjustment shows the planner loop clearly.',
    aiFallbackRationale: 'The plan follows a goal, output, and review loop.',
    aiReviewSummary: 'Today completed {done}/{total} tasks.',
    aiReviewSuggestion1: 'Keep completed tasks as review evidence.',
    aiReviewSuggestion2: 'For unfinished tasks, check scope and time estimates.',
    aiReviewSuggestion3: 'Break unfinished work into smaller next actions.',
    aiReviewSuggestionEmpty: 'No plan yet. Generate suggested AI tasks first.',
    aiSearchNoContext: 'No material yet. Paste a JD, course, or note.',
    aiSearchAnswer: 'Based on current material, focus on these snippets.',
    aiSource: 'Source',
    aiMemorySaved: 'Preference memory saved',
    aiMemoryEmpty: 'No preference yet. Plans will use default pacing.',
    aiEvalScore: 'Planner quality score',
    aiEvalCase1: 'Clear goal with limited time',
    aiEvalCase2: 'User provides JD materials',
    aiEvalCase3: 'User needs dynamic adjustment after unfinished work',
    aiEvalReasonStrong: 'Covers time, context and review loop.',
    aiEvalReasonGood: 'Useful, but could include more measurable outputs.',
    emptyPlans: 'No plans yet',
    emptyAddHint: 'Add a task below',
    todayLabel: 'Today',
    items: '{n} items',
    monthFormat: '{m}/{y}',
    dateFormat: '{y}-{m}-{d}',
    weekdayShort: ['Mo','Tu','We','Th','Fr','Sa','Su'],
    weekdayNames: ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],
    dateLabel: '{w}, {m}/{d}',
  }
};

let currentLang = 'zh';
let onLangChange = null;

function t(key) {
  return langStrings[currentLang][key] || key;
}

function tf(key, vars) {
  let s = t(key);
  for (const k in vars) {
    s = s.replace(`{${k}}`, vars[k]);
  }
  return s;
}

function padMonth(m) {
  return String(m).padStart(2, '0');
}
function padDay(d) {
  return String(d).padStart(2, '0');
}

/** 对各语言不同的日期格式做统一输出 */
function formatDateStr(y, m, d) {
  return tf('dateFormat', { y, m: padMonth(m), d: padDay(d) });
}

function setLang(l) {
  if (l === currentLang) return;
  currentLang = l;
  localStorage.setItem('my_notes_lang', l);
  // 更新 Language 切换按钮高亮
  document.querySelectorAll('.lang-opt').forEach(el => {
    el.classList.toggle('active', el.dataset.lang === l);
  });
  if (onLangChange) onLangChange(l);
}

function applyStaticI18n() {
  // 更新 data-i18n 静态元素
  document.querySelectorAll('[data-i18n]').forEach(el => {
    el.textContent = t(el.dataset.i18n);
  });
  // 更新 placeholder
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    el.placeholder = t(el.dataset.i18nPlaceholder);
  });
}

function initLang(onChange) {
  onLangChange = onChange;
  const saved = localStorage.getItem('my_notes_lang');
  if (saved === 'zh' || saved === 'en') currentLang = saved;
  // 初始化高亮
  document.querySelectorAll('.lang-opt').forEach(el => {
    el.classList.toggle('active', el.dataset.lang === currentLang);
  });
  // 首次应用静态文本
  applyStaticI18n();

  // ── 键盘快捷键：Ctrl+L / ⌘L 切换中英文 ──
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
      e.preventDefault();
      const next = currentLang === 'zh' ? 'en' : 'zh';
      setLang(next);
    }
  });
}
