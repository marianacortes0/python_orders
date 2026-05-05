export type OrderStatus = 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled';

export interface Customer {
  id: number;
  firstName: string;
  lastName: string;
  city?: string;
  country?: string;
  phone?: string;
}

export interface Supplier {
  id: number;
  companyName: string;
  contactName?: string;
  city?: string;
  country?: string;
  phone?: string;
}

export interface Product {
  id: number;
  productName: string;
  unitPrice: number;
  package?: string;
  isDiscontinued: boolean;
  supplier?: Supplier;
}

export interface OrderItem {
  id: number;
  quantity: number;
  unitPrice: number;
  product: Product;
}

export interface Order {
  id: number;
  orderNumber: string;
  orderDate: string;
  totalAmount: number;
  status: OrderStatus;
  customer: Customer;
  items?: OrderItem[];
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
}

export const STATUS_LABELS: Record<OrderStatus, string> = {
  pending:   'Pendiente',
  confirmed: 'Confirmado',
  shipped:   'Enviado',
  delivered: 'Entregado',
  cancelled: 'Cancelado',
};

export const STATUS_OPTIONS = (Object.keys(STATUS_LABELS) as OrderStatus[]).map(k => ({
  value: k,
  label: STATUS_LABELS[k],
}));
