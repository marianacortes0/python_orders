'use client';
import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import DataGrid, {
  Column, Editing, Button as GridButton,
} from 'devextreme-react/data-grid';
import { Button } from 'devextreme-react/button';
import { SelectBox } from 'devextreme-react/select-box';
import { Form, Item, RequiredRule } from 'devextreme-react/form';
import { NumberBox } from 'devextreme-react/number-box';
import { confirm } from 'devextreme/ui/dialog';
import notify from 'devextreme/ui/notify';
import CustomStore from 'devextreme/data/custom_store';
import { getOrder, patchOrder, deleteOrder, listItems, addItem, patchItem, deleteItem, listProducts } from '../../../lib/api';
import { Order, OrderItem, Product, STATUS_OPTIONS, STATUS_LABELS, OrderStatus } from '../../../types';


export default function OrderDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [order,    setOrder]    = useState<Order | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [newStatus, setNewStatus] = useState<OrderStatus | null>(null);
  const [addForm,  setAddForm]  = useState({ productId: null as number | null, quantity: 1, unitPrice: null as number | null });
  const gridRef = useRef<any>(null);

  useEffect(() => {
    getOrder(params.id).then(setOrder).catch(() => notify('Error al cargar pedido', 'error', 3000));
    listProducts({ limit: 1000 }).then((d: any) => setProducts(d.items ?? d)).catch(() => {});
  }, [params.id]);

  const itemsStore = new CustomStore({
    key: 'id',
    load: () => listItems(params.id),
    update: (key: number, values: object) => patchItem(params.id, key, values),
    remove: (key: number) => deleteItem(params.id, key),
  });

  const handleChangeStatus = async () => {
    if (!newStatus || !order) return;
    try {
      const updated = await patchOrder(params.id, { status: newStatus });
      setOrder(updated);
      notify('Estado actualizado', 'success', 2000);
    } catch (e: any) {
      notify(e.message, 'error', 3000);
    }
  };

  const handleDelete = async () => {
    const ok = await confirm('¿Eliminar este pedido?', 'Confirmar');
    if (!ok) return;
    try {
      await deleteOrder(params.id);
      router.push('/orders');
    } catch (e: any) {
      notify(e.message, 'error', 3000);
    }
  };

  const handleAddItem = async () => {
    if (!addForm.productId) { notify('Selecciona un producto', 'warning', 2000); return; }
    if (!addForm.quantity || addForm.quantity < 1) { notify('Cantidad inválida', 'warning', 2000); return; }
    try {
      const body: any = { productId: addForm.productId, quantity: addForm.quantity };
      if (addForm.unitPrice) body.unitPrice = addForm.unitPrice;
      await addItem(params.id, body);
      gridRef.current?.instance?.refresh();
      setAddForm({ productId: null, quantity: 1, unitPrice: null });
      getOrder(params.id).then(setOrder);
      notify('Ítem agregado', 'success', 2000);
    } catch (e: any) {
      notify(e.message, 'error', 3000);
    }
  };

  if (!order) return <div style={{ padding: 40 }}>Cargando...</div>;

  return (
    <div>
      <div className="breadcrumb">
        <Link href="/orders">Pedidos</Link>
        <span className="breadcrumb-sep">/</span>
        <span>Pedido #{order.orderNumber}</span>
      </div>

      <div className="page-header">
        <h1 className="page-title">Pedido #{order.orderNumber}</h1>
        <div className="btn-row">
          <Button text="Eliminar" icon="trash" type="danger" onClick={handleDelete} />
        </div>
      </div>

      <div className="two-col">
        {/* ── Left column ── */}
        <div>
          <div className="card">
            <div className="card-title">Información</div>
            <ul className="detail-list">
              <li>
                <span className="label">Estado</span>
                <span className={`badge badge-${order.status}`}>{STATUS_LABELS[order.status]}</span>
              </li>
              <li>
                <span className="label">Cliente</span>
                <span className="value">
                  <Link href={`/customers/${order.customer.id}`}>
                    {order.customer.firstName} {order.customer.lastName}
                  </Link>
                </span>
              </li>
              <li>
                <span className="label">Fecha</span>
                <span className="value">{new Date(order.orderDate).toLocaleDateString('es-AR')}</span>
              </li>
              <li>
                <span className="label">Total</span>
                <span className="value fw-bold">${order.totalAmount.toFixed(2)}</span>
              </li>
            </ul>
          </div>

          <div className="card">
            <div className="card-title">Cambiar estado</div>
            <SelectBox
              items={STATUS_OPTIONS}
              valueExpr="value"
              displayExpr="label"
              defaultValue={order.status}
              onValueChanged={(e) => setNewStatus(e.value)}
            />
            <div className="mt-16">
              <Button text="Aplicar" type="default" onClick={handleChangeStatus} />
            </div>
          </div>
        </div>

        {/* ── Right column ── */}
        <div>
          <div className="card" style={{ padding: 0 }}>
            <div className="card-title" style={{ padding: '16px 20px 12px', margin: 0 }}>Ítems del pedido</div>
            <DataGrid
              ref={gridRef}
              dataSource={itemsStore}
              showBorders={false}
              showRowLines
            >
              <Editing mode="row" allowUpdating allowDeleting />
              <Column dataField="product.productName" caption="Producto"  allowEditing={false} />
              <Column dataField="unitPrice"           caption="Precio"    format={{ type: 'currency', precision: 2 }} allowEditing={false} width={110} />
              <Column dataField="quantity"            caption="Cantidad"  dataType="number" width={100} />
              <Column
                caption="Subtotal"
                allowEditing={false}
                width={110}
                calculateCellValue={(row: OrderItem) =>
                  row.unitPrice && row.quantity ? `$${(row.unitPrice * row.quantity).toFixed(2)}` : ''
                }
              />
            </DataGrid>
          </div>

          <div className="card">
            <div className="card-title">Agregar ítem</div>
            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr', gap: 12 }}>
              <div>
                <div style={{ marginBottom: 4, fontSize: 12, color: 'var(--text-muted)' }}>Producto</div>
                <SelectBox
                  dataSource={products}
                  valueExpr="id"
                  displayExpr="productName"
                  value={addForm.productId}
                  searchEnabled
                  placeholder="Seleccionar..."
                  onValueChanged={(e) => setAddForm(f => ({ ...f, productId: e.value }))}
                />
              </div>
              <div>
                <div style={{ marginBottom: 4, fontSize: 12, color: 'var(--text-muted)' }}>Cantidad</div>
                <NumberBox
                  min={1}
                  value={addForm.quantity}
                  onValueChanged={(e) => setAddForm(f => ({ ...f, quantity: e.value }))}
                />
              </div>
              <div>
                <div style={{ marginBottom: 4, fontSize: 12, color: 'var(--text-muted)' }}>Precio (opcional)</div>
                <NumberBox
                  min={0}
                  value={addForm.unitPrice ?? undefined}
                  placeholder="Auto"
                  onValueChanged={(e) => setAddForm(f => ({ ...f, unitPrice: e.value }))}
                />
              </div>
            </div>
            <div className="mt-16">
              <Button text="Agregar ítem" type="default" icon="plus" onClick={handleAddItem} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
