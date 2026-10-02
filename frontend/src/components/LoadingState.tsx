export function LoadingState({ label = 'Loading' }: { label?: string }) {
  return <div className="panel"><div className="section-label">{label}</div></div>
}
