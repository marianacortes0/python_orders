const customerService = require('../services/customerService');

async function index(req, res) {
  try {
    const { page = 1, limit = 20, country, city, search } = req.query;
    const data = await customerService.listCustomers({ page: +page, limit: +limit, country, city, search });
    res.render('customers/index', { ...data, query: req.query, title: 'Clientes' });
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

async function show(req, res) {
  try {
    const [customer, orders] = await Promise.all([
      customerService.getCustomer(req.params.id),
      customerService.listCustomerOrders(req.params.id),
    ]);
    res.render('customers/detail', { customer, orders, title: `Cliente: ${customer.firstName} ${customer.lastName}` });
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

function newForm(req, res) {
  res.render('customers/form', { customer: null, errors: null, title: 'Nuevo Cliente' });
}

async function create(req, res) {
  try {
    const customer = await customerService.createCustomer({
      firstName: req.body.firstName,
      lastName: req.body.lastName,
      city: req.body.city || null,
      country: req.body.country || null,
      phone: req.body.phone || null,
    });
    res.redirect(`/customers/${customer.id}`);
  } catch (err) {
    res.render('customers/form', { customer: null, errors: err.data, title: 'Nuevo Cliente' });
  }
}

async function editForm(req, res) {
  try {
    const customer = await customerService.getCustomer(req.params.id);
    res.render('customers/form', { customer, errors: null, title: 'Editar Cliente' });
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

async function update(req, res) {
  try {
    await customerService.updateCustomer(req.params.id, {
      firstName: req.body.firstName || undefined,
      lastName: req.body.lastName || undefined,
      city: req.body.city || null,
      country: req.body.country || null,
      phone: req.body.phone || null,
    });
    res.redirect(`/customers/${req.params.id}`);
  } catch (err) {
    const customer = await customerService.getCustomer(req.params.id).catch(() => null);
    res.render('customers/form', { customer, errors: err.data, title: 'Editar Cliente' });
  }
}

module.exports = { index, show, newForm, create, editForm, update };
