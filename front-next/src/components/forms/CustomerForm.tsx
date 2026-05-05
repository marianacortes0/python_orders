'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from 'devextreme-react/button';
import { TextBox } from 'devextreme-react/text-box';
import notify from 'devextreme/ui/notify';

import { getCustomer, createCustomer, patchCustomer } from '../../lib/api';
import { Customer } from '../../types';


export default function CustomerForm({ id }: { id?: string }) {
  const router = useRouter();
  const isEdit = !!id && id !== 'new';
  const [form, setForm] = useState<Partial<Customer>>({});
  const [loading, setLoading] = useState(isEdit);

  useEffect(() => {
    if (isEdit && id) {
      getCustomer(id).then(setForm).finally(() => setLoading(false));
    }
  }, [id, isEdit]);

  const field = (key: keyof Customer, label: string, required = false, colSpan?: number) => (
    <div style={{ gridColumn: colSpan === 2 ? 'span 2' : undefined }}>
      <div style={{ marginBottom: 4, fontSize: 12, color: 'var(--text-muted)' }}>{label}{required && <span style={{ color: '#c62828' }}> *</span>}</div>
      <TextBox
        value={String(form[key] ?? '')}
        onValueChanged={(e) => setForm(f => ({ ...f, [key]: e.value }))}
      />
    </div>
  );

  const handleSave = async () => {
    if (!form.firstName || !form.lastName) { notify('Nombre y Apellido son requeridos', 'warning', 2000); return; }
    try {
      const saved = isEdit && id ? await patchCustomer(id, form) : await createCustomer(form);
      router.push(`/customers/${saved.id}`);
    } catch (e: any) {
      notify(e.message, 'error', 3000);
    }
  };

  if (loading) return <div style={{ padding: 40 }}>Cargando...</div>;

  return (
    <div style={{ maxWidth: 680 }}>
      <div className="breadcrumb">
        <Link href="/customers">Clientes</Link>
        <span className="breadcrumb-sep">/</span>
        {isEdit && <><Link href={`/customers/${id}`}>{form.firstName} {form.lastName}</Link><span className="breadcrumb-sep">/</span></>}
        <span>{isEdit ? 'Editar' : 'Nuevo'}</span>
      </div>
      <div className="card">
        <div className="card-title">{isEdit ? 'Editar Cliente' : 'Nuevo Cliente'}</div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          {field('firstName', 'Nombre',   true)}
          {field('lastName',  'Apellido', true)}
          {field('city',      'Ciudad')}
          {field('country',   'País')}
          {field('phone',     'Teléfono', false, 2)}
        </div>
        <div className="btn-row mt-24">
          <Button text="Guardar"   type="default" icon="check" onClick={handleSave} />
          <Button text="Cancelar" type="normal"  onClick={() => router.back()} />
        </div>
      </div>
    </div>
  );
}
