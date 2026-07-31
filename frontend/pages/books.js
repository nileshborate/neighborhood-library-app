import { useEffect, useState } from 'react';
import { api } from '../lib/api';

export default function Books() {
  const [books, setBooks] = useState([]);
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

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Books</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
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
