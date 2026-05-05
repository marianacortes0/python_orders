'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const links = [
  { href: '/orders',    label: 'Pedidos',      icon: '📋' },
  { href: '/customers', label: 'Clientes',     icon: '👤' },
  { href: '/products',  label: 'Productos',    icon: '📦' },
  { href: '/suppliers', label: 'Proveedores',  icon: '🏭' },
];

export default function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="sidebar">
      <Link href="/" className="sidebar-logo">
        <span className="sidebar-logo-icon">⚡</span>
        Python Orders
      </Link>
      <nav className="sidebar-nav">
        <div className="sidebar-section">Menú</div>
        {links.map(l => (
          <Link
            key={l.href}
            href={l.href}
            className={`sidebar-link ${pathname.startsWith(l.href) ? 'active' : ''}`}
          >
            <span className="sidebar-icon">{l.icon}</span>
            {l.label}
          </Link>
        ))}
      </nav>
      <div className="sidebar-footer">Python Orders v2.0</div>
    </aside>
  );
}
