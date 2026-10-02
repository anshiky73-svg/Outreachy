import { apiRequest } from './api'
import type { MessageRecord } from '../types'

export const personalizationService = {
  generate: (id: string) => apiRequest<MessageRecord>(`/api/personalization/generate/${id}`, { method: 'POST' }),
  generateBulk: () => apiRequest<{ count: number; results: MessageRecord[] }>('/api/personalization/generate-bulk', { method: 'POST' }),
  get: (id: string) => apiRequest<MessageRecord>(`/api/personalization/${id}`),
}
