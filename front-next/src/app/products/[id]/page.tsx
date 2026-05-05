'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from 'devextreme-react/button';
import { getProduct } from '../../../lib/api';
import { Product } from '../../../types';


export default function ProductDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [product, setProduct] = useState<Product | null>(null);

  useEffect(() => { getProduct(params.id).then(setProduct); }, [params.id]);
  if (!product) return <div style={{ padding: 40 }}>Cargando...</div>;

  return (
    <div style={{ maxWidth: 600 }}>
      <div className="breadcrumb">
        <Link href="/products">Productos</Link>
        <span className="breadcrumb-sep">/</span>
        <span>{product.productName}</span>
      </div>
      <div className="page-header">
        <h1 className="page-title">{product.productName}</h1>
        <Button text="Editar" icon="edit" type="default" onClick={() => router.push(`/products/${params.id}/edit`)} />
      </div>
      <div className="card">
        <div className="card-title">Información del producto</div>
        <ul className="detail-list">
          <li><span className="label">ID</span><span className="value">{product.id}</span></li>
          <li><span className="label">Proveedor</span><span className="value">{product.supplier?.companyName ?? '—'}</span></li>
          <li><span className="label">Precio</span><span className="value fw-bold">${product.unitPrice?.toFixed(2)}</span></li>
          <li><span className="label">Envase</span><span className="value">{product.package ?? '—'}</span></li>
          <li>
            <span className="label">Estado</span>
            <span className={`badge ${product.isDiscontinued ? 'badge-disc' : 'badge-active'}`}>
              {product.isDiscontinued ? 'Discontinuado' : 'Activo'}
            </span>
          </li>
        </ul>
      </div>
    </div>
  );
}
