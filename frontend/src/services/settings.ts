import { apiRequest } from './api'

export const settingsService = {
  get: () => apiRequest<{ database: string; youtubeApi: string; llm: string; smtp: string; emailMode: string }>('/api/settings'),
}
