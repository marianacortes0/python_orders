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

function listSuppliers({ page = 1, limit = 20, country, search } = {}) {
  const params = new URLSearchParams({ page, limit });
  if (country) params.append('country', country);
  if (search) params.append('search', search);
  return apiCall(`${API_BASE_URL}/suppliers?${params}`);
}

function getSupplier(id) {
  return apiCall(`${API_BASE_URL}/suppliers/${id}`);
}

function createSupplier(data) {
  return apiCall(`${API_BASE_URL}/suppliers`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}

function updateSupplier(id, data) {
  return apiCall(`${API_BASE_URL}/suppliers/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}

function listSupplierProducts(id) {
  return apiCall(`${API_BASE_URL}/suppliers/${id}/products`);
}

module.exports = { listSuppliers, getSupplier, createSupplier, updateSupplier, listSupplierProducts };
