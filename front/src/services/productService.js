const { API_BASE_URL } = require('../config/api');

async function apiCall(url, options = {}) {
  const res = await fetch(url, options);
  if (res.status === 204) return null;
  const data = await res.json();
  if (!res.ok) {
    const err = new Error(data.detail || data.message || `Error HTTP ${res.status}`);
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}

function listProducts({ page = 1, limit = 20, supplierId, search, discontinued } = {}) {
  const params = new URLSearchParams({ page, limit });
  if (supplierId) params.append('supplierId', supplierId);
  if (search) params.append('search', search);
  if (discontinued !== undefined && discontinued !== '') params.append('discontinued', discontinued);
  return apiCall(`${API_BASE_URL}/products?${params}`);
}

function getProduct(id) {
  return apiCall(`${API_BASE_URL}/products/${id}`);
}

function createProduct(data) {
  return apiCall(`${API_BASE_URL}/products`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}

function replaceProduct(id, data) {
  return apiCall(`${API_BASE_URL}/products/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}

function updateProduct(id, data) {
  return apiCall(`${API_BASE_URL}/products/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}

function deleteProduct(id) {
  return apiCall(`${API_BASE_URL}/products/${id}`, { method: 'DELETE' });
}

module.exports = { listProducts, getProduct, createProduct, replaceProduct, updateProduct, deleteProduct };
