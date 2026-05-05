'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from 'devextreme-react/button';
import { TextBox } from 'devextreme-react/text-box';
import { NumberBox } from 'devextreme-react/number-box';
import { SelectBox } from 'devextreme-react/select-box';
import { CheckBox } from 'devextreme-react/check-box';
import notify from 'devextreme/ui/notify';

import { getProduct, createProduct, patchProduct, listSuppliers } from '../../lib/api';
import { Product, Supplier } from '../../types';


export default function ProductForm({ id }: { id?: string }) {
  const router = useRouter();
  const isEdit = !!id && id !== 'new';
  const [form, setForm] = useState<Partial<Product>>({ isDiscontinued: false });
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [loading, setLoading] = useState(isEdit);

  useEffect(() => {
    listSuppliers({ limit: 1000 }).then((d: any) => setSuppliers(d.items ?? d));
    if (isEdit && id) {
      getProduct(id).then(setForm).finally(() => setLoading(false));
    }
  }, [id, isEdit]);

  const handleSave = async () => {
    if (!form.productName) { notify('El nombre del producto es requerido', 'warning', 2000); return; }
    try {
      const data = { ...form };
      if (typeof data.supplier === 'object' && data.supplier !== null) {
          // @ts-ignore
          data.supplierId = data.supplier.id;
          delete data.supplier;
      }
      
      const saved = isEdit && id ? await patchProduct(id, data) : await createProduct(data);
      router.push(`/products/${saved.id}`);
    } catch (e: any) {
      notify(e.message, 'error', 3000);
    }
  };

  if (loading) return <div style={{ padding: 40 }}>Cargando...</div>;

  return (
    <div style={{ maxWidth: 680 }}>
      <div className="breadcrumb">
        <Link href="/products">Productos</Link>
        <span className="breadcrumb-sep">/</span>
        {isEdit && <><Link href={`/products/${id}`}>{form.productName}</Link><span className="breadcrumb-sep">/</span></>}
        <span>{isEdit ? 'Editar' : 'Nuevo'}</span>
      </div>
      <div className="card">
        <div className="card-title">{isEdit ? 'Editar Producto' : 'Nuevo Producto'}</div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          <div style={{ gridColumn: 'span 2' }}>
            <div style={{ marginBottom: 4, fontSize: 12, color: 'var(--text-muted)' }}>Nombre del Producto *</div>
            <TextBox value={form.productName} onValueChanged={(e) => setForm(f => ({ ...f, productName: e.value }))} />
          </div>
          
          <div style={{ gridColumn: 'span 2' }}>
            <div style={{ marginBottom: 4, fontSize: 12, color: 'var(--text-muted)' }}>Proveedor</div>
            <SelectBox
              dataSource={suppliers}
              valueExpr="id"
              displayExpr="companyName"
              value={typeof form.supplier === 'object' ? form.supplier?.id : form.supplier}
              searchEnabled
              onValueChanged={(e) => setForm(f => ({ ...f, supplier: e.value }))}
            />
          </div>

          <div>
            <div style={{ marginBottom: 4, fontSize: 12, color: 'var(--text-muted)' }}>Precio</div>
            <NumberBox format="$ #,##0.00" value={form.unitPrice} onValueChanged={(e) => setForm(f => ({ ...f, unitPrice: e.value }))} />
          </div>

          <div>
            <div style={{ marginBottom: 4, fontSize: 12, color: 'var(--text-muted)' }}>Envase</div>
            <TextBox value={form.package} onValueChanged={(e) => setForm(f => ({ ...f, package: e.value }))} />
          </div>

          <div style={{ gridColumn: 'span 2', display: 'flex', alignItems: 'center', gap: 8 }}>
            <CheckBox value={form.isDiscontinued} onValueChanged={(e) => setForm(f => ({ ...f, isDiscontinued: e.value }))} />
            <span style={{ fontSize: 13 }}>Descontinuado</span>
          </div>
        </div>
        <div className="btn-row mt-24">
          <Button text="Guardar"   type="default" icon="check" onClick={handleSave} />
          <Button text="Cancelar" type="normal"  onClick={() => router.back()} />
        </div>
      </div>
    </div>
  );
}
