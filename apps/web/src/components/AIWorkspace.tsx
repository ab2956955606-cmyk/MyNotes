import { useEffect, useState } from 'react';
import { Bot, ClipboardCheck, DatabaseZap, FileSearch, KeyRound, PlugZap, Save, Settings, Sparkles } from 'lucide-react';
import type { AiSettings, AppData, PlannerResponse, PlannerTask } from '../types';
import {
  askMaterials,
  evaluatePlanner,
  fetchAiSettings,
  generatePlan,
  reviewToday,
  saveAiSettings,
  saveMemory,
  testAiSettings
} from '../lib/api';

interface AIWorkspaceProps {
  data: AppData;
  date: string;
  preferences: string;
  onPreferencesChange: (value: string) => void;
  onApplyTasks: (tasks: PlannerTask[]) => void;
  t: (key: string) => string;
}

const defaultSettings: AiSettings = {
  provider: 'deepseek',
  baseUrl: 'https://api.deepseek.com',
  model: 'deepseek-chat',
  hasApiKey: false,
  temperature: 0.3,
  timeoutSeconds: 40,
  updatedAt: ''
};

export function AIWorkspace(props: AIWorkspaceProps) {
  const { data, date, preferences, onPreferencesChange, onApplyTasks, t } = props;
  const [goal, setGoal] = useState('3 个月内拿到北京 AI 应用开发实习');
  const [deadline, setDeadline] = useState(() => {
    const d = new Date();
    d.setMonth(d.getMonth() + 3);
    return d.toISOString().slice(0, 10);
  });
  const [dailyHours, setDailyHours] = useState(3);
  const [materials, setMaterials] = useState('');
  const [result, setResult] = useState<PlannerResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [settings, setSettings] = useState<AiSettings>(defaultSettings);
  const [apiKey, setApiKey] = useState('');
  const [settingsStatus, setSettingsStatus] = useState('');

  const payload = { goal, deadline, dailyHours, materials, preferences, date, data };
  const aiTasks = result?.tasks ?? [];

  useEffect(() => {
    fetchAiSettings()
      .then(setSettings)
      .catch(() => undefined);
  }, []);

  async function run(action: 'plan' | 'review' | 'rag' | 'eval' | 'memory') {
    setLoading(true);
    try {
      if (action === 'plan') setResult(await generatePlan(payload));
      if (action === 'review') setResult(await reviewToday(payload));
      if (action === 'rag') setResult(await askMaterials(payload));
      if (action === 'eval') setResult(await evaluatePlanner(payload));
      if (action === 'memory') {
        await saveMemory(preferences);
        setResult({ summary: t('saved') });
      }
    } finally {
      setLoading(false);
    }
  }

  async function saveModelSettings() {
    try {
      const saved = await saveAiSettings({
        provider: settings.provider,
        baseUrl: settings.baseUrl,
        model: settings.model,
        apiKey: apiKey.trim() || undefined,
        temperature: settings.temperature,
        timeoutSeconds: settings.timeoutSeconds
      });
      setSettings(saved);
      setApiKey('');
      setSettingsStatus(t('settingsSaved'));
    } catch {
      setSettingsStatus(t('settingsError'));
    }
  }

  async function testModel() {
    try {
      const test = await testAiSettings();
      setSettingsStatus(test.ok ? test.message : t('settingsError'));
    } catch {
      setSettingsStatus(t('settingsError'));
    }
  }

  const modeLabel = result?.mode === 'mock' ? t('mockMode') : result?.mode === 'llm' ? t('llmMode') : t('apiMode');

  return (
    <section className="surface ai-panel">
      <div className="section-head">
        <div>
          <span className="eyebrow"><Bot size={14} /> {modeLabel}</span>
          <h2>{t('aiWorkspace')}</h2>
        </div>
      </div>

      <div className="model-settings">
        <div className="settings-title">
          <span><Settings size={15} />{t('aiSettings')}</span>
          <strong>{settings.hasApiKey ? t('hasKey') : t('noKey')}</strong>
        </div>
        <div className="settings-grid">
          <label>
            <span>{t('provider')}</span>
            <select
              value={settings.provider}
              onChange={(event) => setSettings((current) => ({ ...current, provider: event.target.value as AiSettings['provider'] }))}
            >
              <option value="deepseek">DeepSeek</option>
              <option value="openai">OpenAI</option>
              <option value="custom">Custom</option>
              <option value="mock">Mock</option>
            </select>
          </label>
          <label>
            <span>{t('baseUrl')}</span>
            <input value={settings.baseUrl} onChange={(event) => setSettings((current) => ({ ...current, baseUrl: event.target.value }))} />
          </label>
          <label>
            <span>{t('model')}</span>
            <input value={settings.model} onChange={(event) => setSettings((current) => ({ ...current, model: event.target.value }))} />
          </label>
          <label>
            <span><KeyRound size={13} />{t('apiKey')}</span>
            <input type="password" value={apiKey} onChange={(event) => setApiKey(event.target.value)} placeholder={t('apiKeyPlaceholder')} />
          </label>
          <label>
            <span>{t('temperature')}</span>
            <input
              type="number"
              min={0}
              max={2}
              step={0.1}
              value={settings.temperature}
              onChange={(event) => setSettings((current) => ({ ...current, temperature: Number(event.target.value) }))}
            />
          </label>
          <label>
            <span>{t('timeout')}</span>
            <input
              type="number"
              min={5}
              max={120}
              value={settings.timeoutSeconds}
              onChange={(event) => setSettings((current) => ({ ...current, timeoutSeconds: Number(event.target.value) }))}
            />
          </label>
        </div>
        <div className="settings-actions">
          <button onClick={saveModelSettings}><Save size={16} />{t('saveSettings')}</button>
          <button onClick={testModel}><PlugZap size={16} />{t('testModel')}</button>
          {settingsStatus && <span>{settingsStatus}</span>}
        </div>
      </div>

      <div className="ai-grid">
        <label>
          <span>{t('goal')}</span>
          <input value={goal} onChange={(event) => setGoal(event.target.value)} placeholder={t('goalPlaceholder')} />
        </label>
        <label>
          <span>{t('deadline')}</span>
          <input type="date" value={deadline} onChange={(event) => setDeadline(event.target.value)} />
        </label>
        <label>
          <span>{t('dailyHours')}</span>
          <input type="number" min={1} max={12} value={dailyHours} onChange={(event) => setDailyHours(Number(event.target.value))} />
        </label>
        <label className="wide">
          <span>{t('preference')}</span>
          <input value={preferences} onChange={(event) => onPreferencesChange(event.target.value)} placeholder={t('preferencePlaceholder')} />
        </label>
        <label className="wide">
          <span>{t('materials')}</span>
          <textarea value={materials} onChange={(event) => setMaterials(event.target.value)} placeholder={t('materialsPlaceholder')} />
        </label>
      </div>
      <div className="command-row">
        <button onClick={() => run('plan')}><Sparkles size={16} />{t('generate')}</button>
        <button onClick={() => run('review')}><ClipboardCheck size={16} />{t('review')}</button>
        <button onClick={() => run('rag')}><FileSearch size={16} />{t('rag')}</button>
        <button onClick={() => run('memory')}><Save size={16} />{t('saveMemory')}</button>
        <button onClick={() => run('eval')}><DatabaseZap size={16} />{t('evaluate')}</button>
      </div>
      <div className="ai-output">
        {loading && <div className="empty-state">{t('loading')}</div>}
        {!loading && !result && <div className="empty-state">{t('backendTip')}</div>}
        {!loading && result && <ResultView result={result} t={t} />}
      </div>
      <button className="apply-button" onClick={() => onApplyTasks(aiTasks)} disabled={!aiTasks.length}>
        {aiTasks.length ? t('applyTasks') : t('noAiTasks')}
      </button>
    </section>
  );
}

function ResultView({ result, t }: { result: PlannerResponse; t: (key: string) => string }) {
  const heading = result.score ? `${t('score')}: ${result.score}/5` : result.summary ?? result.answer ?? t('aiWorkspace');
  return (
    <div className="result-view">
      <h3>{heading}</h3>
      {result.provider && <p><strong>{result.provider}</strong> / {result.model}</p>}
      {result.phases?.map((phase) => <p key={phase.title}><strong>{phase.title}</strong>: {phase.detail}</p>)}
      {result.tasks?.map((task) => (
        <div className="ai-task" key={`${task.time}-${task.title}`}>
          <time>{task.time}</time>
          <div><strong>{task.title}</strong><p>{task.reason}</p></div>
        </div>
      ))}
      {result.suggestions && <ul>{result.suggestions.map((item) => <li key={item}>{item}</li>)}</ul>}
      {result.answer && result.answer !== heading && <p>{result.answer}</p>}
      {result.sources && <ul>{result.sources.map((item) => <li key={item.title}><strong>{item.title}</strong>: {item.quote}</li>)}</ul>}
      {result.keywords && <p>{result.keywords.join(' / ')}</p>}
      {result.results && <ul>{result.results.map((item) => <li key={item.case}><strong>{item.score}/5</strong> {item.case} - {item.reason}</li>)}</ul>}
    </div>
  );
}
