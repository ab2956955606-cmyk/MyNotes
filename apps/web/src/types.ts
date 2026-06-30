export type Lang = 'zh' | 'en';

export interface Plan {
  id: string;
  time: string;
  title: string;
  done: boolean;
  completion: string;
  source?: 'manual' | 'ai';
}

export interface DayRecord {
  plans: Plan[];
}

export type AppData = Record<string, DayRecord>;

export interface PlannerTask {
  time: string;
  title: string;
  reason: string;
}

export interface PlannerResponse {
  mode?: 'api' | 'mock' | 'llm';
  summary?: string;
  phases?: Array<{ title: string; detail: string }>;
  tasks?: PlannerTask[];
  suggestions?: string[];
  answer?: string;
  sources?: Array<{ title: string; quote: string }>;
  keywords?: string[];
  score?: number;
  provider?: string;
  model?: string;
  results?: Array<{ case: string; score: number; reason: string }>;
}

export interface AiSettings {
  provider: 'mock' | 'deepseek' | 'openai' | 'custom';
  baseUrl: string;
  model: string;
  hasApiKey: boolean;
  temperature: number;
  timeoutSeconds: number;
  updatedAt: string;
}

export interface AiSettingsInput {
  provider: AiSettings['provider'];
  baseUrl: string;
  model: string;
  apiKey?: string;
  temperature: number;
  timeoutSeconds: number;
}

export interface AiSettingsTestResult {
  ok: boolean;
  mode: 'mock' | 'llm' | 'error';
  message: string;
  provider: string;
  model: string;
}
