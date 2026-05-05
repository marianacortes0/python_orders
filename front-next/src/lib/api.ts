// ── Orders ──────────────────────────────────────────────────────────────────
export async function listOrders(params: Record<string, string | number> = {}) {
  const qs = new URLSearchParams(params as Record<string, string>).toString();
  const res = await fetch(`/api/orders${qs ? '?' + qs : ''}`);
  if (!res.ok) throw new Error('Error al cargar pedidos');
  return res.json();
}

export async function getOrder(id: number | string) {
  const res = await fetch(`/api/orders/${id}`);
  if (!res.ok) throw new Error('Error al cargar pedido');
  return res.json();
}

export async function createOrder(data: object) {
  const res = await fetch('/api/orders', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(json.detail || 'Error al crear pedido');
  return json;
}

export async function patchOrder(id: number | string, data: object) {
  const res = await fetch(`/api/orders/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(json.detail || 'Error al actualizar pedido');
  return json;
}

export async function deleteOrder(id: number | string) {
  const res = await fetch(`/api/orders/${id}`, { method: 'DELETE' });
  if (!res.ok && res.status !== 204) throw new Error('Error al eliminar pedido');
}

// ── Order Items ─────────────────────────────────────────────────────────────
export async function listItems(orderId: number | string) {
  const res = await fetch(`/api/orders/${orderId}/items`);
  if (!res.ok) throw new Error('Error al cargar ítems');
  return res.json();
}

export async function addItem(orderId: number | string, data: object) {
  const res = await fetch(`/api/orders/${orderId}/items`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(json.detail || 'Error al agregar ítem');
  return json;
}

export async function patchItem(orderId: number | string, itemId: number | string, data: object) {
  const res = await fetch(`/api/orders/${orderId}/items/${itemId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(json.detail || 'Error al actualizar ítem');
  return json;
}

export async function deleteItem(orderId: number | string, itemId: number | string) {
  const res = await fetch(`/api/orders/${orderId}/items/${itemId}`, { method: 'DELETE' });
  if (!res.ok && res.status !== 204) throw new Error('Error al eliminar ítem');
}

// ── Customers ───────────────────────────────────────────────────────────────
export async function listCustomers(params: Record<string, string | number> = {}) {
  const qs = new URLSearchParams(params as Record<string, string>).toString();
  const res = await fetch(`/api/customers${qs ? '?' + qs : ''}`);
  if (!res.ok) throw new Error('Error al cargar clientes');
  return res.json();
}

export async function getCustomer(id: number | string) {
  const res = await fetch(`/api/customers/${id}`);
  if (!res.ok) throw new Error('Error al cargar cliente');
  return res.json();
}

export async function createCustomer(data: object) {
  const res = await fetch('/api/customers', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(json.detail || 'Error al crear cliente');
  return json;
}

export async function patchCustomer(id: number | string, data: object) {
  const res = await fetch(`/api/customers/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(json.detail || 'Error al actualizar cliente');
  return json;
}

// ── Products ─────────────────────────────────────────────────────────────────
export async function listProducts(params: Record<string, string | number> = {}) {
  const qs = new URLSearchParams(params as Record<string, string>).toString();
  const res = await fetch(`/api/products${qs ? '?' + qs : ''}`);
  if (!res.ok) throw new Error('Error al cargar productos');
  return res.json();
}

export async function getProduct(id: number | string) {
  const res = await fetch(`/api/products/${id}`);
  if (!res.ok) throw new Error('Error al cargar producto');
  return res.json();
}

export async function createProduct(data: object) {
  const res = await fetch('/api/products', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(json.detail || 'Error al crear producto');
  return json;
}

export async function patchProduct(id: number | string, data: object) {
  const res = await fetch(`/api/products/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(json.detail || 'Error al actualizar producto');
  return json;
}

// ── Suppliers ────────────────────────────────────────────────────────────────
export async function listSuppliers(params: Record<string, string | number> = {}) {
  const qs = new URLSearchParams(params as Record<string, string>).toString();
  const res = await fetch(`/api/suppliers${qs ? '?' + qs : ''}`);
  if (!res.ok) throw new Error('Error al cargar proveedores');
  return res.json();
}

export async function getSupplier(id: number | string) {
  const res = await fetch(`/api/suppliers/${id}`);
  if (!res.ok) throw new Error('Error al cargar proveedor');
  return res.json();
}

export async function createSupplier(data: object) {
  const res = await fetch('/api/suppliers', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(json.detail || 'Error al crear proveedor');
  return json;
}

export async function patchSupplier(id: number | string, data: object) {
  const res = await fetch(`/api/suppliers/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(json.detail || 'Error al actualizar proveedor');
  return json;
}
