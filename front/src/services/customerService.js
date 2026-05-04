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

function listCustomers({ page = 1, limit = 20, country, city, search } = {}) {
  const params = new URLSearchParams({ page, limit });
  if (country) params.append('country', country);
  if (city) params.append('city', city);
  if (search) params.append('search', search);
  return apiCall(`${API_BASE_URL}/customers?${params}`);
}

function getCustomer(id) {
  return apiCall(`${API_BASE_URL}/customers/${id}`);
}

function createCustomer(data) {
  return apiCall(`${API_BASE_URL}/customers`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}

function updateCustomer(id, data) {
  return apiCall(`${API_BASE_URL}/customers/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}

function listCustomerOrders(id) {
  return apiCall(`${API_BASE_URL}/customers/${id}/orders`);
}

module.exports = { listCustomers, getCustomer, createCustomer, updateCustomer, listCustomerOrders };
