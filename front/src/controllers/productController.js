const productService = require('../services/productService');
const supplierService = require('../services/supplierService');

async function index(req, res) {
  try {
    const { page = 1, limit = 20, supplierId, search, discontinued } = req.query;
    const data = await productService.listProducts({ page: +page, limit: +limit, supplierId, search, discontinued });
    res.render('products/index', { ...data, query: req.query, title: 'Productos' });
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

async function show(req, res) {
  try {
    const product = await productService.getProduct(req.params.id);
    res.render('products/detail', { product, title: `Producto: ${product.productName}` });
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

async function newForm(req, res) {
  try {
    const suppliersData = await supplierService.listSuppliers({ limit: 200 });
    res.render('products/form', { product: null, suppliers: suppliersData.items, errors: null, title: 'Nuevo Producto' });
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

async function create(req, res) {
  try {
    const product = await productService.createProduct({
      productName: req.body.productName,
      supplierId: +req.body.supplierId,
      unitPrice: +req.body.unitPrice,
      package: req.body.package || null,
      isDiscontinued: req.body.isDiscontinued === 'true',
    });
    res.redirect(`/products/${product.id}`);
  } catch (err) {
    const suppliersData = await supplierService.listSuppliers({ limit: 200 }).catch(() => ({ items: [] }));
    res.render('products/form', { product: null, suppliers: suppliersData.items, errors: err.data, title: 'Nuevo Producto' });
  }
}

async function editForm(req, res) {
  try {
    const [product, suppliersData] = await Promise.all([
      productService.getProduct(req.params.id),
      supplierService.listSuppliers({ limit: 200 }),
    ]);
    res.render('products/form', { product, suppliers: suppliersData.items, errors: null, title: 'Editar Producto' });
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

async function update(req, res) {
  try {
    await productService.updateProduct(req.params.id, {
      productName: req.body.productName || undefined,
      supplierId: req.body.supplierId ? +req.body.supplierId : undefined,
      unitPrice: req.body.unitPrice ? +req.body.unitPrice : undefined,
      package: req.body.package || null,
      isDiscontinued: req.body.isDiscontinued !== undefined ? req.body.isDiscontinued === 'true' : undefined,
    });
    res.redirect(`/products/${req.params.id}`);
  } catch (err) {
    const [product, suppliersData] = await Promise.all([
      productService.getProduct(req.params.id).catch(() => null),
      supplierService.listSuppliers({ limit: 200 }).catch(() => ({ items: [] })),
    ]);
    res.render('products/form', { product, suppliers: suppliersData.items, errors: err.data, title: 'Editar Producto' });
  }
}

async function destroy(req, res) {
  try {
    await productService.deleteProduct(req.params.id);
    res.redirect('/products');
  } catch (err) {
    res.render('error', { title: 'Error', message: err.message });
  }
}

module.exports = { index, show, newForm, create, editForm, update, destroy };
