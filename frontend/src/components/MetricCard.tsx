type MetricCardProps = {
  label: string
  value: string | number
  tone?: 'default' | 'positive' | 'warning'
}

export function MetricCard({ label, value, tone = 'default' }: MetricCardProps) {
  return (
    <div className={`metric-card ${tone}`}>
      <div className="eyebrow">{label}</div>
      <div className="metric-value">{value}</div>
    </div>
  )
}
