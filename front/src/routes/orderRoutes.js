const { Router } = require('express');
const ctrl = require('../controllers/orderController');

const router = Router();

router.get('/', ctrl.index);
router.get('/new', ctrl.newForm);
router.post('/', ctrl.create);
router.get('/:id', ctrl.show);
router.post('/:id/status', ctrl.updateStatus);
router.post('/:id/delete', ctrl.destroy);
router.post('/:id/items', ctrl.addItem);
router.post('/:id/items/:itemId/update', ctrl.updateItem);
router.post('/:id/items/:itemId/delete', ctrl.deleteItem);

module.exports = router;
