const supplierService = require('../services/supplierService');

async function index(req, res) {
  try {
    const { page = 1, limit = 20, country, search } = req.query;
    const data = await supplierService.listSuppliers({ page: +page, limit: +limit, country, search });
    res.render('suppliers/index', { ...data, query: req.query, title: 'Proveedores' });
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

async function show(req, res) {
  try {
    const [supplier, products] = await Promise.all([
      supplierService.getSupplier(req.params.id),
      supplierService.listSupplierProducts(req.params.id),
    ]);
    res.render('suppliers/detail', { supplier, products, title: `Proveedor: ${supplier.companyName}` });
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

function newForm(req, res) {
  res.render('suppliers/form', { supplier: null, errors: null, title: 'Nuevo Proveedor' });
}

async function create(req, res) {
  try {
    const supplier = await supplierService.createSupplier({
      companyName: req.body.companyName,
      contactName: req.body.contactName || null,
      contactTitle: req.body.contactTitle || null,
      city: req.body.city || null,
      country: req.body.country || null,
      phone: req.body.phone || null,
      fax: req.body.fax || null,
    });
    res.redirect(`/suppliers/${supplier.id}`);
  } catch (err) {
    res.render('suppliers/form', { supplier: null, errors: err.data, title: 'Nuevo Proveedor' });
  }
}

async function editForm(req, res) {
  try {
    const supplier = await supplierService.getSupplier(req.params.id);
    res.render('suppliers/form', { supplier, errors: null, title: 'Editar Proveedor' });
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

async function update(req, res) {
  try {
    await supplierService.updateSupplier(req.params.id, {
      companyName: req.body.companyName || undefined,
      contactName: req.body.contactName || null,
      contactTitle: req.body.contactTitle || null,
      city: req.body.city || null,
      country: req.body.country || null,
      phone: req.body.phone || null,
      fax: req.body.fax || null,
    });
    res.redirect(`/suppliers/${req.params.id}`);
  } catch (err) {
    const supplier = await supplierService.getSupplier(req.params.id).catch(() => null);
    res.render('suppliers/form', { supplier, errors: err.data, title: 'Editar Proveedor' });
  }
}

module.exports = { index, show, newForm, create, editForm, update };
