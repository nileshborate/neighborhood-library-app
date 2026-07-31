import { useEffect, useState } from 'react';
import { api } from '../lib/api';

export default function Loans() {
  const [books, setBooks] = useState([]);
  const [members, setMembers] = useState([]);
  const [loans, setLoans] = useState([]);
  const [form, setForm] = useState({
    book_id: '',
    member_id: '',
    loan_days: 14,
  });
  const [error, setError] = useState('');

  async function loadAll() {
    try {
      const [b, m, l] = await Promise.all([
        api.listBooks(),
        api.listMembers(),
        api.listLoans({ active_only: true }),
      ]);
      setBooks(b);
      setMembers(m);
      setLoans(l);
    } catch (e) {
      setError(e.message);
    }
  }

  useEffect(() => {
    loadAll();
  }, []);

  async function handleBorrow(e) {
    e.preventDefault();
    setError('');
    try {
      await api.borrowBook({
        book_id: Number(form.book_id),
        member_id: Number(form.member_id),
        loan_days: Number(form.loan_days),
      });
      setForm({ book_id: '', member_id: '', loan_days: 14 });
      await loadAll();
    } catch (e) {
      setError(e.message);
    }
  }

  async function handleReturn(loanId) {
    setError('');
    try {
      await api.returnLoan(loanId);
      await loadAll();
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Loans</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <h2>Borrow a book</h2>
      <form onSubmit={handleBorrow} style={{ marginBottom: '1.5rem' }}>
        <select
          required
          value={form.book_id}
          onChange={(e) => setForm({ ...form, book_id: e.target.value })}
        >
          <option value="">Select a book…</option>
          {books.map((b) => (
            <option key={b.id} value={b.id}>
              {b.title} ({b.available_copies} left)
            </option>
          ))}
        </select>{' '}
        <select
          required
          value={form.member_id}
          onChange={(e) => setForm({ ...form, member_id: e.target.value })}
        >
          <option value="">Select a member…</option>
          {members.map((m) => (
            <option key={m.id} value={m.id}>
              {m.name}
            </option>
          ))}
        </select>{' '}
        <input
          type="number"
          min="1"
          value={form.loan_days}
          onChange={(e) => setForm({ ...form, loan_days: e.target.value })}
        />{' '}
        <button type="submit">Borrow</button>
      </form>

      <h2>Currently borrowed</h2>
      <table border="1" cellPadding="8" style={{ borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>Book</th>
            <th>Member</th>
            <th>Due</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {loans.map((loan) => (
            <tr key={loan.id}>
              <td>{loan.book.title}</td>
              <td>{loan.member.name}</td>
              <td>{new Date(loan.due_date).toLocaleDateString()}</td>
              <td>
                <button onClick={() => handleReturn(loan.id)}>
                  Mark returned
                </button>
              </td>
            </tr>
          ))}
          {loans.length === 0 && (
            <tr>
              <td colSpan={4}>No books currently borrowed.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
