import { useQuery } from '@tanstack/react-query'
import { settingsService } from '../services/settings'

export function SettingsPage() {
  const { data } = useQuery({ queryKey: ['settings'], queryFn: settingsService.get })

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <div className="eyebrow">Settings</div>
          <h1>Configuration status</h1>
        </div>
      </header>

      <div className="panel">
        <div className="meta-grid">
          <div><span className="label">MongoDB</span><strong>{data?.database ?? 'Not configured'}</strong></div>
          <div><span className="label">YouTube API</span><strong>{data?.youtubeApi ?? 'Not configured'}</strong></div>
          <div><span className="label">LLM</span><strong>{data?.llm ?? 'Not configured'}</strong></div>
          <div><span className="label">SMTP</span><strong>{data?.smtp ?? 'Not configured'}</strong></div>
          <div><span className="label">Email mode</span><strong>{data?.emailMode ?? 'simulation'}</strong></div>
        </div>
      </div>
    </div>
  )
}
