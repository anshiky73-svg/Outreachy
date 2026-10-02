import { useQuery } from '@tanstack/react-query'
import { StatusBadge } from '../components/StatusBadge'
import { outreachService } from '../services/outreach'

export function OutreachPage() {
  const { data = [] } = useQuery({
    queryKey: ['outreach'],
    queryFn: outreachService.list,
  })

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <div className="eyebrow">Outreach</div>
          <h1>Sending tracker</h1>
        </div>
      </header>

      <div className="panel table-wrap">
        <table>
          <thead>
            <tr>
              <th>Influencer</th>
              <th>Recipient</th>
              <th>Channel</th>
              <th>Status</th>
              <th>Sent date</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item) => (
              <tr key={item._id}>
                <td>{item.influencerId}</td>
                <td>{item.recipient}</td>
                <td>{item.channel}</td>
                <td><StatusBadge status={item.status} /></td>
                <td>{item.sentAt || '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
