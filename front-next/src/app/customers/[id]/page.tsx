'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import DataGrid, { Column, Pager, Paging, Button as GridButton } from 'devextreme-react/data-grid';
import { Button } from 'devextreme-react/button';
import { getCustomer } from '../../../lib/api';
import { Customer, Order, STATUS_LABELS, OrderStatus } from '../../../types';


export default function CustomerDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [orders,   setOrders]   = useState<Order[]>([]);

  useEffect(() => {
    getCustomer(params.id).then((d: any) => {
      setCustomer(d);
      setOrders(d.orders ?? []);
    });
  }, [params.id]);

  if (!customer) return <div style={{ padding: 40 }}>Cargando...</div>;

  return (
    <div>
      <div className="breadcrumb">
        <Link href="/customers">Clientes</Link>
        <span className="breadcrumb-sep">/</span>
        <span>{customer.firstName} {customer.lastName}</span>
      </div>
      <div className="page-header">
        <h1 className="page-title">{customer.firstName} {customer.lastName}</h1>
        <Button text="Editar" icon="edit" type="default" onClick={() => router.push(`/customers/${params.id}/edit`)} />
      </div>
      <div className="two-col">
        <div className="card">
          <div className="card-title">Datos del cliente</div>
          <ul className="detail-list">
            <li><span className="label">ID</span><span className="value">{customer.id}</span></li>
            <li><span className="label">Ciudad</span><span className="value">{customer.city || '—'}</span></li>
            <li><span className="label">País</span><span className="value">{customer.country || '—'}</span></li>
            <li><span className="label">Teléfono</span><span className="value">{customer.phone || '—'}</span></li>
          </ul>
        </div>
        <div className="card" style={{ padding: 0 }}>
          <div className="card-title" style={{ padding: '16px 20px 12px', margin: 0 }}>Pedidos del cliente</div>
          <DataGrid dataSource={orders} showBorders={false} showRowLines>
            <Paging defaultPageSize={10} />
            <Pager showInfo />
            <Column dataField="orderNumber" caption="N° Pedido" width={130} />
            <Column dataField="orderDate"   caption="Fecha" dataType="date" format="dd/MM/yyyy" width={110} />
            <Column dataField="totalAmount" caption="Total" format={{ type: 'currency', precision: 2 }} width={110} />
            <Column
              dataField="status"
              caption="Estado"
              width={120}
              cellRender={({ data }: { data: Order }) => (
                <span className={`badge badge-${data.status}`}>{STATUS_LABELS[data.status as OrderStatus] ?? data.status}</span>
              )}
            />
            <Column type="buttons" width={60}>
              <GridButton icon="eyeopen" hint="Ver pedido" onClick={(e: any) => router.push(`/orders/${e.row.data.id}`)} />
            </Column>
          </DataGrid>
        </div>
      </div>
    </div>
  );
}
