import { apiRequest } from './api'
import type { DashboardStats } from '../types'

export const dashboardService = {
  getStats: () => apiRequest<DashboardStats>('/api/dashboard/stats'),
}
