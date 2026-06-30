/* ============ AI 规划助手 ============ */

const AI_API_BASE = localStorage.getItem('my_notes_api_base') || 'http://127.0.0.1:8000';
const AI_API_ENABLED = location.protocol !== 'file:' || localStorage.getItem('my_notes_api_enabled') === '1';
let lastAiTasks = [];

function getAllPlansSnapshot() {
  return loadAll();
}

async function aiPost(path, payload) {
  if (!AI_API_ENABLED) throw new Error('AI API disabled for file preview');
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 1200);
  try {
    const res = await fetch(`${AI_API_BASE}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: controller.signal
    });
    if (!res.ok) throw new Error(`AI API ${res.status}`);
    return res.json();
  } finally {
    clearTimeout(timer);
  }
}

function aiSetMode(mode) {
  const el = $('aiMode');
  if (el) el.textContent = mode;
}

function getAiPayload() {
  return {
    goal: $('aiGoalInput').value.trim(),
    deadline: $('aiDeadlineInput').value,
    daily_hours: Number($('aiHoursInput').value || 2),
    context: $('aiContextInput').value.trim(),
    preferences: $('aiPreferenceInput').value.trim(),
    date: selectedDate || todayStr(),
    plans: getAllPlansSnapshot()
  };
}

function fallbackPlan(payload) {
  const goal = payload.goal || t('aiFallbackGoal');
  const hours = payload.daily_hours || 2;
  const focus = payload.context ? t('aiFallbackWithContext') : t('aiFallbackNoContext');
  return {
    mode: 'mock',
    summary: tf('aiPlanSummary', { goal, hours }),
    phases: [
      { title: t('aiPhase1'), detail: t('aiPhase1Detail') },
      { title: t('aiPhase2'), detail: t('aiPhase2Detail') },
      { title: t('aiPhase3'), detail: t('aiPhase3Detail') }
    ],
    tasks: [
      { time: '09:00', text: t('aiTaskResearch'), reason: focus },
      { time: '14:30', text: t('aiTaskBuild'), reason: t('aiTaskBuildReason') },
      { time: '20:00', text: t('aiTaskReview'), reason: t('aiTaskReviewReason') }
    ],
    rationale: t('aiFallbackRationale')
  };
}

function fallbackReview(payload) {
  const data = getDayData(payload.date);
  const plans = data.plans || [];
  const done = plans.filter(p => p.done).length;
  return {
    mode: 'mock',
    summary: tf('aiReviewSummary', { done, total: plans.length }),
    suggestions: [
      t('aiReviewSuggestion1'),
      t('aiReviewSuggestion2'),
      plans.length ? t('aiReviewSuggestion3') : t('aiReviewSuggestionEmpty')
    ]
  };
}

function fallbackSearch(payload) {
  const context = payload.context || t('aiSearchNoContext');
  const terms = context.split(/\s+|，|。|,|\./).filter(Boolean).slice(0, 6);
  return {
    mode: 'mock',
    answer: t('aiSearchAnswer'),
    sources: terms.map((term, idx) => ({ title: `${t('aiSource')} ${idx + 1}`, quote: term }))
  };
}

function fallbackEval() {
  return {
    average_score: 4.4,
    criteria: ['actionable', 'time-aware', 'adaptive', 'context-grounded', 'reviewable'],
    results: [
      { case: t('aiEvalCase1'), score: 5, reason: t('aiEvalReasonStrong') },
      { case: t('aiEvalCase2'), score: 4, reason: t('aiEvalReasonGood') },
      { case: t('aiEvalCase3'), score: 4, reason: t('aiEvalReasonGood') }
    ]
  };
}

function renderAiPlan(data) {
  lastAiTasks = data.tasks || [];
  $('aiOutput').innerHTML = `
    <h4>${escapeHtml(data.summary || t('aiGenerated'))}</h4>
    ${(data.phases || []).map(p => `<p><strong>${escapeHtml(p.title)}</strong>：${escapeHtml(p.detail)}</p>`).join('')}
    <h4>${t('aiTodayTasks')}</h4>
    ${(data.tasks || []).map(task => `
      <div class="ai-task">
        <time>${escapeHtml(task.time || '09:00')}</time>
        <div>
          <strong>${escapeHtml(task.text || '')}</strong>
          <p>${escapeHtml(task.reason || '')}</p>
        </div>
      </div>
    `).join('')}
    <p>${escapeHtml(data.rationale || '')}</p>
  `;
}

function renderAiReview(data) {
  lastAiTasks = [];
  $('aiOutput').innerHTML = `
    <h4>${escapeHtml(data.summary || t('aiReview'))}</h4>
    <ul>${(data.suggestions || []).map(s => `<li>${escapeHtml(s)}</li>`).join('')}</ul>
  `;
}

function renderAiSearch(data) {
  lastAiTasks = [];
  $('aiOutput').innerHTML = `
    <h4>${escapeHtml(data.answer || t('aiSearch'))}</h4>
    <ul>${(data.sources || []).map(s => `<li><strong>${escapeHtml(s.title)}</strong>：${escapeHtml(s.quote)}</li>`).join('')}</ul>
  `;
}

function renderAiEval(data) {
  lastAiTasks = [];
  $('aiOutput').innerHTML = `
    <h4>${t('aiEvalScore')}: ${escapeHtml(String(data.average_score || 0))}/5</h4>
    <p>${(data.criteria || []).map(escapeHtml).join(' · ')}</p>
    <ul>${(data.results || []).map(item => `<li><strong>${escapeHtml(String(item.score))}/5</strong> ${escapeHtml(item.case)} - ${escapeHtml(item.reason)}</li>`).join('')}</ul>
  `;
}

async function runAi(kind) {
  const payload = getAiPayload();
  $('aiOutput').innerHTML = `<div class="ai-empty">${t('aiLoading')}</div>`;
  try {
    const path = kind === 'plan' ? '/api/agent/plan' : kind === 'review' ? '/api/agent/review' : kind === 'eval' ? '/api/eval/planner' : '/api/rag/query';
    const data = await aiPost(path, payload);
    aiSetMode('API AI');
    if (kind === 'plan') renderAiPlan(data);
    else if (kind === 'review') renderAiReview(data);
    else if (kind === 'eval') renderAiEval(data);
    else renderAiSearch(data);
  } catch {
    aiSetMode('Mock AI');
    if (kind === 'plan') renderAiPlan(fallbackPlan(payload));
    else if (kind === 'review') renderAiReview(fallbackReview(payload));
    else if (kind === 'eval') renderAiEval(fallbackEval());
    else renderAiSearch(fallbackSearch(payload));
  }
}

async function saveAiMemory() {
  const preferences = $('aiPreferenceInput').value.trim();
  localStorage.setItem('my_notes_preferences', preferences);
  try {
    await aiPost('/api/memory/preferences', { user_id: 'local-user', preferences });
    aiSetMode('API AI');
  } catch {
    aiSetMode('Mock AI');
  }
  $('aiOutput').innerHTML = `<h4>${t('aiMemorySaved')}</h4><p>${escapeHtml(preferences || t('aiMemoryEmpty'))}</p>`;
}

function applyAiTasksToToday() {
  if (!lastAiTasks.length) return;
  const data = getDayData(selectedDate);
  lastAiTasks.forEach(task => {
    data.plans.push({
      id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
      time: task.time || '09:00',
      text: task.text || '',
      done: false,
      completion: ''
    });
  });
  putDayData(selectedDate, data);
  renderDay(selectedDate);
  renderCalendar(viewYear, viewMonth);
  $('aiOutput').insertAdjacentHTML('beforeend', `<p><strong>${t('aiApplied')}</strong></p>`);
}

function initAiPlanner() {
  const deadline = $('aiDeadlineInput');
  if (deadline && !deadline.value) {
    const d = new Date();
    d.setMonth(d.getMonth() + 3);
    deadline.value = fmtDate(d.getFullYear(), d.getMonth(), d.getDate());
  }
  $('aiPreferenceInput').value = localStorage.getItem('my_notes_preferences') || '';
  $('aiGenerateBtn').addEventListener('click', () => runAi('plan'));
  $('aiReviewBtn').addEventListener('click', () => runAi('review'));
  $('aiSearchBtn').addEventListener('click', () => runAi('search'));
  $('aiMemoryBtn').addEventListener('click', saveAiMemory);
  $('aiEvalBtn').addEventListener('click', () => runAi('eval'));
  $('aiApplyBtn').addEventListener('click', applyAiTasksToToday);
}
