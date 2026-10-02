import { useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'
import { Button } from '../components/Button'
import { StatusBadge } from '../components/StatusBadge'
import { influencersService } from '../services/influencers'
import { personalizationService } from '../services/personalization'
import { outreachService } from '../services/outreach'

export function InfluencerDetailPage() {
  const { id } = useParams()
  const { data: influencer, isLoading } = useQuery({
    queryKey: ['influencer', id],
    queryFn: () => influencersService.get(id || ''),
    enabled: !!id,
  })

  const { data: qualification } = useQuery({
    queryKey: ['qualification', id],
    queryFn: () => influencersService.getQualification(id || ''),
    enabled: !!id,
  })

  const messageQuery = useQuery({
    queryKey: ['message', id],
    queryFn: () => personalizationService.generate(id || ''),
    enabled: false,
  })

  const reasons = useMemo(() => qualification?.qualificationReasons || [], [qualification])

  if (isLoading || !influencer) return <div className="panel">Loading creator…</div>

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <div className="eyebrow">Creator</div>
          <h1>{influencer.name}</h1>
        </div>
        <div className="action-row">
          <Button onClick={() => messageQuery.refetch()} variant="secondary">Generate Message</Button>
          <Button onClick={() => outreachService.simulate(id || '')} variant="secondary">Simulate Email</Button>
          <Button onClick={() => outreachService.send(id || '')} variant="secondary">Send Email</Button>
          <Button onClick={() => outreachService.markDmSent(id || '')} variant="secondary">Mark DM Sent</Button>
        </div>
      </header>

      <div className="detail-grid">
        <div className="panel">
          <div className="section-header"><h2>Profile</h2></div>
          <div className="meta-grid">
            <div><span className="label">Platform</span><strong>{influencer.platform}</strong></div>
            <div><span className="label">Profile URL</span><a href={influencer.profileUrl || '#'}>{influencer.profileUrl || 'Not Found'}</a></div>
            <div><span className="label">Followers</span><strong>{influencer.followerCount ?? 0}</strong></div>
            <div><span className="label">Estimated engagement</span><strong>{influencer.engagementRate ?? 0}%</strong></div>
            <div><span className="label">Niche</span><strong>{influencer.niche ?? 'Technology'}</strong></div>
            <div><span className="label">Email</span><strong>{influencer.contactEmail ?? 'Not Found'}</strong></div>
            <div><span className="label">Email source</span><strong>{influencer.emailSource ?? 'not_found'}</strong></div>
            <div><span className="label">Website</span><strong>{influencer.website || 'Not Found'}</strong></div>
          </div>
        </div>

        <div className="panel">
          <div className="section-header"><h2>Qualification</h2></div>
          <div className="meta-grid">
            <div><span className="label">Status</span><StatusBadge status={qualification?.qualificationStatus ?? influencer.qualificationStatus ?? 'PENDING'} /></div>
            <div><span className="label">Score</span><strong>{qualification?.qualificationScore ?? influencer.qualificationScore ?? 0}</strong></div>
          </div>
          <ul className="reason-list">
            {reasons.length === 0 ? <li>No qualification reasons available.</li> : reasons.map((reason) => <li key={reason}>{reason}</li>)}
          </ul>
        </div>
      </div>

      <div className="panel">
        <div className="section-header"><h2>Content themes</h2></div>
        <div className="chip-row">
          {(influencer.contentThemes || ['technology']).map((theme) => <span key={theme} className="chip">{theme}</span>)}
        </div>
        <p className="muted">Content style: {influencer.contentStyle || 'Creator content'}</p>
      </div>

      <div className="panel">
        <div className="section-header"><h2>Generated message</h2></div>
        {messageQuery.data ? (
          <div className="message-block">
            <strong>{messageQuery.data.emailSubject}</strong>
            <p>{messageQuery.data.emailBody}</p>
            <div className="muted">Signals: {messageQuery.data.personalizationSignals?.join(', ') || 'Not available'}</div>
            <div className="dm-box">DM: {messageQuery.data.instagramDm}</div>
          </div>
        ) : (
          <div className="muted">No generated message yet. Use Generate Message.</div>
        )}
      </div>
    </div>
  )
}
