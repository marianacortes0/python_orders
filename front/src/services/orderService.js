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

function listOrders({ page = 1, limit = 20, customerId, dateFrom, dateTo, status, sort } = {}) {
  const params = new URLSearchParams({ page, limit });
  if (customerId) params.append('customerId', customerId);
  if (dateFrom) params.append('dateFrom', dateFrom);
  if (dateTo) params.append('dateTo', dateTo);
  if (status) params.append('status', status);
  if (sort) params.append('sort', sort);
  return apiCall(`${API_BASE_URL}/orders?${params}`);
}

function getOrder(id) {
  return apiCall(`${API_BASE_URL}/orders/${id}`);
}

function createOrder(data) {
  return apiCall(`${API_BASE_URL}/orders`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}

function replaceOrder(id, data) {
  return apiCall(`${API_BASE_URL}/orders/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}

function updateOrder(id, data) {
  return apiCall(`${API_BASE_URL}/orders/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}

function deleteOrder(id) {
  return apiCall(`${API_BASE_URL}/orders/${id}`, { method: 'DELETE' });
}

function listItems(orderId) {
  return apiCall(`${API_BASE_URL}/orders/${orderId}/items`);
}

function addItem(orderId, data) {
  return apiCall(`${API_BASE_URL}/orders/${orderId}/items`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}

function updateItem(orderId, itemId, data) {
  return apiCall(`${API_BASE_URL}/orders/${orderId}/items/${itemId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}

function deleteItem(orderId, itemId) {
  return apiCall(`${API_BASE_URL}/orders/${orderId}/items/${itemId}`, { method: 'DELETE' });
}

module.exports = { listOrders, getOrder, createOrder, replaceOrder, updateOrder, deleteOrder, listItems, addItem, updateItem, deleteItem };
