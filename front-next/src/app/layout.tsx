import type { Metadata } from 'next';
import './globals.css';
import Sidebar from '../components/Sidebar';


export const metadata: Metadata = {
  title: 'Python Orders',
  description: 'Sistema de gestión de pedidos',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>
        <div className="app-shell">
          <Sidebar />
          <main className="main-content">
            <div className="page-content">{children}</div>
          </main>
        </div>
      </body>
    </html>
  );
}
