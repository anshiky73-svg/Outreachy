import { NavLink, Outlet } from 'react-router-dom'

const links = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/discovery', label: 'Discovery' },
  { to: '/influencers', label: 'Influencers' },
  { to: '/messages', label: 'Messages' },
  { to: '/outreach', label: 'Outreach' },
  { to: '/settings', label: 'Settings' },
]

export function AppLayout() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">I</div>
          <div>
            <div className="eyebrow">Influencer</div>
            <div className="brand-name">Outreach AI</div>
          </div>
        </div>

        <nav className="nav">
          {links.map((link) => (
            <NavLink key={link.to} to={link.to} className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
              {link.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      <main className="content-shell">
        <Outlet />
      </main>
    </div>
  )
}
