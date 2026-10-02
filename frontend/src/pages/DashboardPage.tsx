import { useQuery } from '@tanstack/react-query'
import { Button } from '../components/Button'
import { MetricCard } from '../components/MetricCard'
import { StatusBadge } from '../components/StatusBadge'
import { dashboardService } from '../services/dashboard'
import { discoveryService } from '../services/discovery'
import { enrichmentService } from '../services/enrichment'
import { filteringService } from '../services/filtering'
import { personalizationService } from '../services/personalization'

export function DashboardPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: dashboardService.getStats,
  })

  const stats = data || {
    totalInfluencers: 0,
    qualifiedInfluencers: 0,
    failedInfluencers: 0,
    emailsFound: 0,
    messagesGenerated: 0,
    emailsSent: 0,
    emailsSimulated: 0,
    failedOutreach: 0,
    recentDiscoveryRuns: [],
    recentOutreach: [],
  }

  const runDiscovery = async () => {
    await discoveryService.run({ niche: 'Technology', queries: ['AI tools', 'artificial intelligence', 'programming'] })
    window.location.reload()
  }

  const runFiltering = async () => {
    await filteringService.run()
    window.location.reload()
  }

  const runEnrichment = async () => {
    await enrichmentService.run()
    window.location.reload()
  }

  const runMessages = async () => {
    await personalizationService.generateBulk()
    window.location.reload()
  }

  if (isLoading) return <div className="panel">Loading dashboard…</div>
  if (error) return <div className="panel">Unable to load dashboard.</div>

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <div className="eyebrow">Overview</div>
          <h1>Influencer outreach dashboard</h1>
        </div>
        <div className="action-row">
          <Button onClick={runDiscovery}>Run Discovery</Button>
          <Button variant="secondary" onClick={runFiltering}>Run Filtering</Button>
          <Button variant="secondary" onClick={runEnrichment}>Run Enrichment</Button>
          <Button variant="secondary" onClick={runMessages}>Generate Messages</Button>
        </div>
      </header>

      <section className="metrics-grid">
        <MetricCard label="Total candidates" value={stats.totalInfluencers} />
        <MetricCard label="Qualified" value={stats.qualifiedInfluencers} tone="positive" />
        <MetricCard label="Failed" value={stats.failedInfluencers} tone="warning" />
        <MetricCard label="Emails found" value={stats.emailsFound} />
        <MetricCard label="Messages generated" value={stats.messagesGenerated} />
        <MetricCard label="Emails sent" value={stats.emailsSent} />
        <MetricCard label="Simulated emails" value={stats.emailsSimulated} />
        <MetricCard label="Failed outreach" value={stats.failedOutreach} tone="warning" />
      </section>

      <section className="dashboard-grid">
        <div className="panel">
          <div className="section-header">
            <h2>Recent discovery runs</h2>
          </div>
          <div className="stack-list">
            {(stats.recentDiscoveryRuns || []).map((run) => (
              <div key={run._id} className="row-item">
                <div>
                  <strong>{run.niche}</strong>
                  <div className="muted">{run.status}</div>
                </div>
                <div className="muted">{run.candidatesFound} candidates</div>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="section-header">
            <h2>Recent outreach</h2>
          </div>
          <div className="stack-list">
            {(stats.recentOutreach || []).map((log) => (
              <div key={log._id} className="row-item">
                <div>
                  <strong>{log.influencerId}</strong>
                  <div className="muted">{log.channel}</div>
                </div>
                <StatusBadge status={log.status} />
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
