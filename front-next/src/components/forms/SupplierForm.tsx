'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from 'devextreme-react/button';
import { TextBox } from 'devextreme-react/text-box';
import notify from 'devextreme/ui/notify';

import { getSupplier, createSupplier, patchSupplier } from '../../lib/api';
import { Supplier } from '../../types';


export default function SupplierForm({ id }: { id?: string }) {
  const router = useRouter();
  const isEdit = !!id && id !== 'new';
  const [form, setForm] = useState<Partial<Supplier>>({});
  const [loading, setLoading] = useState(isEdit);

  useEffect(() => {
    if (isEdit && id) {
      getSupplier(id).then(setForm).finally(() => setLoading(false));
    }
  }, [id, isEdit]);

  const field = (key: keyof Supplier, label: string, required = false, colSpan?: number) => (
    <div style={{ gridColumn: colSpan === 2 ? 'span 2' : undefined }}>
      <div style={{ marginBottom: 4, fontSize: 12, color: 'var(--text-muted)' }}>{label}{required && <span style={{ color: '#c62828' }}> *</span>}</div>
      <TextBox
        value={String(form[key] ?? '')}
        onValueChanged={(e) => setForm(f => ({ ...f, [key]: e.value }))}
      />
    </div>
  );

  const handleSave = async () => {
    if (!form.companyName) { notify('El nombre de la empresa es requerido', 'warning', 2000); return; }
    try {
      const saved = isEdit && id ? await patchSupplier(id, form) : await createSupplier(form);
      router.push(`/suppliers/${saved.id}`);
    } catch (e: any) {
      notify(e.message, 'error', 3000);
    }
  };

  if (loading) return <div style={{ padding: 40 }}>Cargando...</div>;

  return (
    <div style={{ maxWidth: 680 }}>
      <div className="breadcrumb">
        <Link href="/suppliers">Proveedores</Link>
        <span className="breadcrumb-sep">/</span>
        {isEdit && <><Link href={`/suppliers/${id}`}>{form.companyName}</Link><span className="breadcrumb-sep">/</span></>}
        <span>{isEdit ? 'Editar' : 'Nuevo'}</span>
      </div>
      <div className="card">
        <div className="card-title">{isEdit ? 'Editar Proveedor' : 'Nuevo Proveedor'}</div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          {field('companyName', 'Empresa', true, 2)}
          {field('contactName', 'Contacto')}
          {field('phone',       'Teléfono')}
          {field('city',        'Ciudad')}
          {field('country',     'País')}
        </div>
        <div className="btn-row mt-24">
          <Button text="Guardar"   type="default" icon="check" onClick={handleSave} />
          <Button text="Cancelar" type="normal"  onClick={() => router.back()} />
        </div>
      </div>
    </div>
  );
}
