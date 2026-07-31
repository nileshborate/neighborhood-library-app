const API_BASE_URL = 'http://localhost:8000/api';

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || detail;
    } catch (_) {}
    throw new Error(detail);
  }

  return res.json();
}

export const api = {
  listBooks: () => request('/books'),
  createBook: (data) =>
    request('/books', { method: 'POST', body: JSON.stringify(data) }),

  listMembers: () => request('/members'),
  createMember: (data) =>
    request('/members', { method: 'POST', body: JSON.stringify(data) }),

  listLoans: (params = {}) => request(`/loans?${new URLSearchParams(params)}`),
  borrowBook: (data) =>
    request('/loans', { method: 'POST', body: JSON.stringify(data) }),
  returnLoan: (loanId) =>
    request(`/loans/${loanId}/return`, {
      method: 'POST',
      body: JSON.stringify({}),
    }),
};
