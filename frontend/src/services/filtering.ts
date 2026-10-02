import { apiRequest } from './api'

export const filteringService = {
  run: () => apiRequest<{ summary: { total: number; qualified: number; failed: number }; results: Array<{ influencerId: string; qualificationStatus: string; qualificationReasons: string[]; qualificationScore: number }> }>('/api/filtering/run', { method: 'POST' }),
  getResults: () => apiRequest<Array<{ influencerId: string; qualificationStatus: string; qualificationReasons: string[]; qualificationScore: number }>>('/api/filtering/results'),
}
