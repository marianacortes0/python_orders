const { Router } = require('express');
const customerRoutes = require('./customerRoutes');
const supplierRoutes = require('./supplierRoutes');
const productRoutes = require('./productRoutes');
const orderRoutes = require('./orderRoutes');

const router = Router();

router.get('/', (req, res) => res.render('index', { title: 'Dashboard - Python Orders' }));

router.use('/customers', customerRoutes);
router.use('/suppliers', supplierRoutes);
router.use('/products', productRoutes);
router.use('/orders', orderRoutes);

module.exports = router;
