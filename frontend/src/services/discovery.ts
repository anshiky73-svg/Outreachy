import { apiRequest } from './api'
import type { DiscoveryRun, Influencer } from '../types'

export const discoveryService = {
  run: (payload: { niche?: string; queries?: string[]; candidate_limit?: number }) =>
    apiRequest<{ runId: string; status: string; data: DiscoveryRun }>('/api/discovery/run', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  getRuns: () => apiRequest<DiscoveryRun[]>('/api/discovery/runs'),
  getRunResults: (runId: string) => apiRequest<{ runId: string; influencers: Influencer[] }>(`/api/discovery/runs/${runId}/results`),
}
