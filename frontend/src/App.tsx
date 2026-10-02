import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

import './App.css'
import { AppLayout } from './layouts/AppLayout'
import { DashboardPage } from './pages/DashboardPage'
import { DiscoveryPage } from './pages/DiscoveryPage'
import { InfluencerDetailPage } from './pages/InfluencerDetailPage'
import { InfluencersPage } from './pages/InfluencersPage'
import { MessagesPage } from './pages/MessagesPage'
import { OutreachPage } from './pages/OutreachPage'
import { SettingsPage } from './pages/SettingsPage'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<AppLayout />}>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/discovery" element={<DiscoveryPage />} />
            <Route path="/influencers" element={<InfluencersPage />} />
            <Route path="/influencers/:id" element={<InfluencerDetailPage />} />
            <Route path="/messages" element={<MessagesPage />} />
            <Route path="/outreach" element={<OutreachPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
