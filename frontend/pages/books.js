import { useEffect, useState } from 'react';
import { api } from '../lib/api';

const EMPTY_FORM = { title: '', author: '', isbn: '', total_copies: 1 };

export default function Books() {
  const [books, setBooks] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [error, setError] = useState('');

  useEffect(() => {
    loadBooks();
  }, []);

  async function loadBooks() {
    try {
      const data = await api.listBooks();
      setBooks(data);
    } catch (e) {
      setError(e.message);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    try {
      await api.createBook({
        ...form,
        isbn: form.isbn || null,
        total_copies: Number(form.total_copies),
      });
      setForm(EMPTY_FORM);
      await loadBooks();
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Books</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <form onSubmit={handleSubmit} style={{ marginBottom: '1.5rem' }}>
        <input
          placeholder="Title"
          required
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
        />{' '}
        <input
          placeholder="Author"
          required
          value={form.author}
          onChange={(e) => setForm({ ...form, author: e.target.value })}
        />{' '}
        <input
          placeholder="ISBN (optional)"
          value={form.isbn}
          onChange={(e) => setForm({ ...form, isbn: e.target.value })}
        />{' '}
        <input
          type="number"
          min="0"
          placeholder="Copies"
          required
          value={form.total_copies}
          onChange={(e) => setForm({ ...form, total_copies: e.target.value })}
        />{' '}
        <button type="submit">Add book</button>
      </form>

      <table border="1" cellPadding="8" style={{ borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>Title</th>
            <th>Author</th>
            <th>Available</th>
          </tr>
        </thead>
        <tbody>
          {books.map((b) => (
            <tr key={b.id}>
              <td>{b.title}</td>
              <td>{b.author}</td>
              <td>
                {b.available_copies} / {b.total_copies}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
