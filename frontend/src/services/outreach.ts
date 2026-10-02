import { apiRequest } from './api'
import type { OutreachLog } from '../types'

export const outreachService = {
  list: () => apiRequest<OutreachLog[]>('/api/outreach/logs'),
  get: (id: string) => apiRequest<OutreachLog>(`/api/outreach/${id}`),
  simulate: (id: string) => apiRequest<OutreachLog>(`/api/outreach/simulate/${id}`, { method: 'POST' }),
  send: (id: string) => apiRequest<OutreachLog>(`/api/outreach/send/${id}`, { method: 'POST' }),
  markDmSent: (id: string) => apiRequest<OutreachLog>(`/api/outreach/mark-dm-sent/${id}`, { method: 'POST' }),
}
