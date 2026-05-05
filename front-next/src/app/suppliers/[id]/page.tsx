'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from 'devextreme-react/button';
import { getSupplier } from '../../../lib/api';
import { Supplier } from '../../../types';


export default function SupplierDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [supplier, setSupplier] = useState<Supplier | null>(null);

  useEffect(() => {
    getSupplier(params.id).then(setSupplier).catch(() => {});
  }, [params.id]);

  if (!supplier) return <div style={{ padding: 40 }}>Cargando...</div>;

  return (
    <div>
      <div className="breadcrumb">
        <Link href="/suppliers">Proveedores</Link>
        <span className="breadcrumb-sep">/</span>
        <span>{supplier.companyName}</span>
      </div>
      <div className="page-header">
        <h1 className="page-title">{supplier.companyName}</h1>
        <Button text="Editar" icon="edit" type="default" onClick={() => router.push(`/suppliers/${params.id}/edit`)} />
      </div>
      <div className="card" style={{ maxWidth: 600 }}>
        <div className="card-title">Datos del proveedor</div>
        <ul className="detail-list">
          <li><span className="label">ID</span><span className="value">{supplier.id}</span></li>
          <li><span className="label">Empresa</span><span className="value">{supplier.companyName}</span></li>
          <li><span className="label">Contacto</span><span className="value">{supplier.contactName || '—'}</span></li>
          <li><span className="label">Ciudad</span><span className="value">{supplier.city || '—'}</span></li>
          <li><span className="label">País</span><span className="value">{supplier.country || '—'}</span></li>
          <li><span className="label">Teléfono</span><span className="value">{supplier.phone || '—'}</span></li>
        </ul>
      </div>
    </div>
  );
}
