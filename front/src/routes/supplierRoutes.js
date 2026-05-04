const { Router } = require('express');
const ctrl = require('../controllers/supplierController');

const router = Router();

router.get('/', ctrl.index);
router.get('/new', ctrl.newForm);
router.post('/', ctrl.create);
router.get('/:id', ctrl.show);
router.get('/:id/edit', ctrl.editForm);
router.post('/:id', ctrl.update);

module.exports = router;
