'use client';
import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import DataGrid, { Column, Editing, Lookup } from 'devextreme-react/data-grid';
import { Button } from 'devextreme-react/button';
import { SelectBox } from 'devextreme-react/select-box';
import { DateBox } from 'devextreme-react/date-box';
import { TextBox } from 'devextreme-react/text-box';
import notify from 'devextreme/ui/notify';
import ArrayStore from 'devextreme/data/array_store';
import DataSource from 'devextreme/data/data_source';
import { listCustomers, listProducts, createOrder } from '../../../lib/api';
import { Customer, Product } from '../../../types';


interface LocalItem { _id: number; productId: number | null; quantity: number; unitPrice: number | null; }

export default function NewOrderPage() {
  const router = useRouter();
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [products,  setProducts]  = useState<Product[]>([]);
  const [customerId, setCustomerId] = useState<number | null>(null);
  const [orderNumber, setOrderNumber] = useState('');
  const [orderDate,   setOrderDate]   = useState<Date | null>(null);
  const [items, setItems] = useState<LocalItem[]>([]);
  const gridRef = useRef<any>(null);

  useEffect(() => {
    listCustomers({ limit: 1000 }).then((d: any) => setCustomers(d.items ?? d)).catch(() => {});
    listProducts({ limit: 1000  }).then((d: any) => setProducts(d.items ?? d)).catch(() => {});
  }, []);

  const itemsStore = new DataSource({
    store: new ArrayStore({ key: '_id', data: items }),
  });

  const handleSave = async () => {
    if (!customerId) { notify('Selecciona un cliente', 'warning', 2000); return; }
    const rows: LocalItem[] = gridRef.current?.instance?.getDataSource().items() ?? [];
    if (!rows.length) { notify('Agregá al menos un ítem', 'warning', 2000); return; }

    const payload: any = {
      customerId,
      items: rows.map(r => ({
        productId: r.productId,
        quantity:  r.quantity,
        ...(r.unitPrice ? { unitPrice: r.unitPrice } : {}),
      })),
    };
    if (orderNumber) payload.orderNumber = orderNumber;
    if (orderDate)   payload.orderDate   = orderDate.toISOString();

    try {
      const saved = await createOrder(payload);
      router.push(`/orders/${saved.id}`);
    } catch (e: any) {
      notify(e.message, 'error', 3000);
    }
  };

  return (
    <div style={{ maxWidth: 900 }}>
      <div className="breadcrumb">
        <Link href="/orders">Pedidos</Link>
        <span className="breadcrumb-sep">/</span>
        <span>Nuevo</span>
      </div>

      <div className="card">
        <div className="card-title">Nuevo Pedido</div>
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr', gap: 16 }}>
          <div>
            <div style={{ marginBottom: 4, fontSize: 12, color: 'var(--text-muted)' }}>Cliente *</div>
            <SelectBox
              dataSource={customers}
              valueExpr="id"
              displayExpr={(c: Customer) => c ? `${c.firstName} ${c.lastName}` : ''}
              searchEnabled
              placeholder="Seleccionar cliente..."
              onValueChanged={(e) => setCustomerId(e.value)}
            />
          </div>
          <div>
            <div style={{ marginBottom: 4, fontSize: 12, color: 'var(--text-muted)' }}>N° Pedido</div>
            <TextBox placeholder="Auto-generado" value={orderNumber} onValueChanged={(e) => setOrderNumber(e.value)} />
          </div>
          <div>
            <div style={{ marginBottom: 4, fontSize: 12, color: 'var(--text-muted)' }}>Fecha</div>
            <DateBox type="datetime" displayFormat="dd/MM/yyyy HH:mm" value={orderDate ?? undefined} onValueChanged={(e) => setOrderDate(e.value)} />
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-title">Ítems <span style={{ color: '#c62828' }}>*</span></div>
        <DataGrid
          ref={gridRef}
          dataSource={itemsStore}
          showBorders
          onRowInserted={(e) => { e.data._id = Date.now(); }}
        >
          <Editing mode="row" allowUpdating allowDeleting allowAdding={false} />
          <Column dataField="productId" caption="Producto">
            <Lookup dataSource={products} valueExpr="id" displayExpr="productName" />
          </Column>
          <Column dataField="quantity"  caption="Cantidad"  dataType="number" width={110} />
          <Column dataField="unitPrice" caption="Precio (opc.)" dataType="number" width={140} />
        </DataGrid>
        <div className="mt-16">
          <Button
            text="Agregar fila"
            icon="plus"
            type="normal"
            onClick={() => gridRef.current?.instance?.addRow()}
          />
        </div>
      </div>

      <div className="btn-row">
        <Button text="Crear Pedido" type="default" icon="check" onClick={handleSave} />
        <Button text="Cancelar"     type="normal"  onClick={() => router.back()} />
      </div>
    </div>
  );
}
