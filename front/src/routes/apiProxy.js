const { Router } = require('express');
const { API_BASE_URL } = require('../config/api');

const router = Router();

router.all('*', async (req, res) => {
  try {
    const backendUrl = `${API_BASE_URL}${req.url}`;
    const options = { method: req.method, headers: {} };

    if (['POST', 'PUT', 'PATCH'].includes(req.method) && req.body && Object.keys(req.body).length) {
      options.headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(req.body);
    }

    const response = await fetch(backendUrl, options);

    if (response.status === 204) return res.status(204).send();

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    res.status(502).json({ message: 'No se pudo conectar con el backend', detail: err.message });
  }
});

module.exports = router;
