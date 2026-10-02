import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Button } from '../components/Button'
import { discoveryService } from '../services/discovery'

const defaultQueries = [
  'AI tools',
  'artificial intelligence',
  'programming',
  'software development',
  'coding',
  'web development',
  'machine learning',
  'developer tools',
  'tech reviews',
  'software engineering',
]

export function DiscoveryPage() {
  const [niche, setNiche] = useState('Technology')
  const [queries, setQueries] = useState(defaultQueries.join('\n'))
  const [result, setResult] = useState<any>(null)
  const { data: runs = [] } = useQuery({ queryKey: ['discovery-runs'], queryFn: discoveryService.getRuns })

  const handleRun = async () => {
    const payload = {
      niche,
      queries: queries.split('\n').map((line) => line.trim()).filter(Boolean),
      candidate_limit: 150,
    }
    const response = await discoveryService.run(payload)
    setResult(response)
  }

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <div className="eyebrow">Discovery</div>
          <h1>Technology creator discovery</h1>
        </div>
      </header>

      <div className="panel">
        <div className="field-grid">
          <label>
            <span>Niche</span>
            <input value={niche} onChange={(event) => setNiche(event.target.value)} />
          </label>
          <label>
            <span>Search queries</span>
            <textarea rows={8} value={queries} onChange={(event) => setQueries(event.target.value)} />
          </label>
        </div>
        <div className="action-row top-gap">
          <Button onClick={handleRun}>Run Discovery</Button>
        </div>
      </div>

      {result && (
        <div className="panel">
          <div className="section-header">
            <h2>Run status</h2>
          </div>
          <div className="stats-line">
            <span>Run status: {result.status}</span>
            <span>Candidates: {result.data?.candidatesFound ?? 0}</span>
            <span>Stored: {result.data?.storedCount ?? 0}</span>
          </div>
        </div>
      )}

      <div className="panel">
        <div className="section-header">
          <h2>Recent runs</h2>
        </div>
        <div className="stack-list">
          {(runs || []).map((run) => (
            <div key={run._id} className="row-item">
              <div>
                <strong>{run.niche}</strong>
                <div className="muted">{run.status}</div>
              </div>
              <div className="muted">{run.candidatesFound} found • {run.storedCount} stored</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
