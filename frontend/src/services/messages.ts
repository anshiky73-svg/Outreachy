import { apiRequest } from './api'
import type { MessageRecord } from '../types'

export const messagesService = {
  list: () => apiRequest<MessageRecord[]>('/api/messages'),
  get: (id: string) => apiRequest<MessageRecord>(`/api/messages/${id}`),
}
