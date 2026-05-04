const { Router } = require('express');
const customerRoutes = require('./customerRoutes');
const supplierRoutes = require('./supplierRoutes');
const productRoutes = require('./productRoutes');
const orderRoutes = require('./orderRoutes');
const apiProxy = require('./apiProxy');

const router = Router();

// Proxy transparente hacia el backend — el browser llama /api/* sin CORS
router.use('/api', apiProxy);

router.get('/', (req, res) => res.render('index', { title: 'Dashboard - Python Orders' }));

router.use('/customers', customerRoutes);
router.use('/suppliers', supplierRoutes);
router.use('/products', productRoutes);
router.use('/orders', orderRoutes);

module.exports = router;
