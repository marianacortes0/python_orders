const orderService = require('../services/orderService');
const customerService = require('../services/customerService');
const productService = require('../services/productService');

const ORDER_STATUSES = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled'];

async function index(req, res) {
  try {
    const { page = 1, limit = 20, customerId, dateFrom, dateTo, status, sort } = req.query;
    const data = await orderService.listOrders({ page: +page, limit: +limit, customerId, dateFrom, dateTo, status, sort });
    res.render('orders/index', { ...data, query: req.query, statuses: ORDER_STATUSES, title: 'Pedidos' });
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

async function show(req, res) {
  try {
    const order = await orderService.getOrder(req.params.id);
    const productsData = await productService.listProducts({ limit: 200 });
    res.render('orders/detail', { order, products: productsData.items, statuses: ORDER_STATUSES, title: `Pedido #${order.orderNumber}` });
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

async function newForm(req, res) {
  try {
    const [customersData, productsData] = await Promise.all([
      customerService.listCustomers({ limit: 200 }),
      productService.listProducts({ limit: 200 }),
    ]);
    res.render('orders/form', {
      order: null,
      customers: customersData.items,
      products: productsData.items,
      errors: null,
      title: 'Nuevo Pedido',
    });
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

async function create(req, res) {
  try {
    const productIds = [].concat(req.body.productId || []);
    const quantities = [].concat(req.body.quantity || []);
    const unitPrices = [].concat(req.body.unitPrice || []);

    const items = productIds.map((productId, i) => ({
      productId: +productId,
      quantity: +quantities[i],
      unitPrice: unitPrices[i] ? +unitPrices[i] : undefined,
    }));

    const order = await orderService.createOrder({
      customerId: +req.body.customerId,
      orderNumber: req.body.orderNumber || undefined,
      orderDate: req.body.orderDate || undefined,
      items,
    });
    res.redirect(`/orders/${order.id}`);
  } catch (err) {
    const [customersData, productsData] = await Promise.all([
      customerService.listCustomers({ limit: 200 }).catch(() => ({ items: [] })),
      productService.listProducts({ limit: 200 }).catch(() => ({ items: [] })),
    ]);
    res.render('orders/form', {
      order: null,
      customers: customersData.items,
      products: productsData.items,
      errors: err.data,
      title: 'Nuevo Pedido',
    });
  }
}

async function updateStatus(req, res) {
  try {
    await orderService.updateOrder(req.params.id, { status: req.body.status });
    res.redirect(`/orders/${req.params.id}`);
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

async function destroy(req, res) {
  try {
    await orderService.deleteOrder(req.params.id);
    res.redirect('/orders');
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

async function addItem(req, res) {
  try {
    await orderService.addItem(req.params.id, {
      productId: +req.body.productId,
      quantity: +req.body.quantity,
      unitPrice: req.body.unitPrice ? +req.body.unitPrice : undefined,
    });
    res.redirect(`/orders/${req.params.id}`);
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

async function updateItem(req, res) {
  try {
    await orderService.updateItem(req.params.id, req.params.itemId, {
      quantity: req.body.quantity ? +req.body.quantity : undefined,
      unitPrice: req.body.unitPrice ? +req.body.unitPrice : undefined,
    });
    res.redirect(`/orders/${req.params.id}`);
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

async function deleteItem(req, res) {
  try {
    await orderService.deleteItem(req.params.id, req.params.itemId);
    res.redirect(`/orders/${req.params.id}`);
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

module.exports = { index, show, newForm, create, updateStatus, destroy, addItem, updateItem, deleteItem };
