import { useMemo, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { StatusBadge } from '../components/StatusBadge'
import { influencersService } from '../services/influencers'

export function InfluencersPage() {
  const [query, setQuery] = useState('')
  const [status, setStatus] = useState('')
  const [platform, setPlatform] = useState('')

  const { data } = useQuery({
    queryKey: ['influencers', { status, platform }],
    queryFn: () => influencersService.list({ limit: 200, status: status || undefined, platform: platform || undefined }),
  })

  const items = data?.items || []

  const filtered = useMemo(() => {
    return items.filter((item) => {
      const text = `${item.name} ${item.niche || ''} ${item.contactEmail || ''}`.toLowerCase()
      return text.includes(query.toLowerCase())
    })
  }, [items, query])

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <div className="eyebrow">Influencers</div>
          <h1>Qualified candidates</h1>
        </div>
      </header>

      <div className="panel controls-panel">
        <input aria-label="Search influencers" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search by name, email, niche" />
        <select value={status} onChange={(event) => setStatus(event.target.value)}>
          <option value="">All status</option>
          <option value="QUALIFIED">Qualified</option>
          <option value="FAILED">Failed</option>
        </select>
        <select value={platform} onChange={(event) => setPlatform(event.target.value)}>
          <option value="">All platforms</option>
          <option value="youtube">YouTube</option>
          <option value="instagram">Instagram</option>
          <option value="tiktok">TikTok</option>
        </select>
      </div>

      <div className="panel table-wrap">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Platform</th>
              <th>Followers</th>
              <th>Engagement</th>
              <th>Niche</th>
              <th>Email</th>
              <th>Score</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((item) => (
              <tr key={item._id}>
                <td><Link to={`/influencers/${item._id}`}>{item.name}</Link></td>
                <td>{item.platform}</td>
                <td>{item.followerCount ?? 0}</td>
                <td>{item.engagementRate ?? 0}%</td>
                <td>{item.niche ?? 'Technology'}</td>
                <td>{item.contactEmail ?? 'Not Found'}</td>
                <td>{item.qualificationScore ?? 0}</td>
                <td><StatusBadge status={item.qualificationStatus ?? 'PENDING'} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
