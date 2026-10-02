import { apiRequest } from './api'
import type { Influencer } from '../types'

export const influencersService = {
  list: (params?: { skip?: number; limit?: number; platform?: string; niche?: string; status?: string }) =>
    apiRequest<{ items: Influencer[]; count: number }>(`/api/influencers${params ? `?${new URLSearchParams(Object.entries(params).filter(([, value]) => value !== undefined && value !== null && value !== '').map(([key, value]) => [key, String(value)]) as [string, string][]).toString()}` : ''}`),
  get: (id: string) => apiRequest<Influencer>(`/api/influencers/${id}`),
  getQualification: (id: string) => apiRequest<{ influencerId: string; qualificationStatus: string; qualificationReasons: string[]; qualificationScore: number }>(`/api/influencers/${id}/qualification`),
}
