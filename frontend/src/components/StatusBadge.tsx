type StatusBadgeProps = {
  status: string
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const normalized = status.toUpperCase()
  const tone =
    normalized === 'QUALIFIED' || normalized === 'SENT' || normalized === 'SIMULATED' || normalized === 'MANUAL_SENT'
      ? 'status-ok'
      : normalized === 'FAILED' || normalized === 'DUPLICATE'
        ? 'status-fail'
        : 'status-neutral'

  return <span className={`status-badge ${tone}`}>{normalized}</span>
}
