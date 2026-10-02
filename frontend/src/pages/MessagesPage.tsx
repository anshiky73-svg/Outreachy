import { useQuery } from '@tanstack/react-query'
import { messagesService } from '../services/messages'
import { StatusBadge } from '../components/StatusBadge'

export function MessagesPage() {
  const { data = [] } = useQuery({
    queryKey: ['messages'],
    queryFn: messagesService.list,
  })

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <div className="eyebrow">Messages</div>
          <h1>Generated outreach</h1>
        </div>
      </header>

      <div className="panel table-wrap">
        <table>
          <thead>
            <tr>
              <th>Influencer</th>
              <th>Email</th>
              <th>Word count</th>
              <th>DM word count</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item) => (
              <tr key={item._id}>
                <td>{item.influencerId}</td>
                <td>{item.emailSubject}</td>
                <td>{item.emailWordCount ?? 0}</td>
                <td>{item.dmWordCount ?? 0}</td>
                <td><StatusBadge status={item.status || 'READY'} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
