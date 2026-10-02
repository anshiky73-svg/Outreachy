import { apiRequest } from './api'

export const enrichmentService = {
  run: () => apiRequest<{ status: string; results: Array<{ influencerId: string; status: string; emailFound: boolean; emailSource?: string; notes: string }> }>('/api/enrichment/run', { method: 'POST' }),
  enrich: (influencerId: string) => apiRequest<{ influencerId: string; status: string; emailFound: boolean; emailSource?: string; notes: string }>(`/api/enrichment/${influencerId}`, { method: 'POST' }),
}
