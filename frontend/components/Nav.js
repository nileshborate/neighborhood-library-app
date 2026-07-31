import Link from 'next/link';

export default function Nav() {
  return (
    <nav
      style={{
        padding: '1rem 2rem',
        background: '#222',
        display: 'flex',
        gap: '1.5rem',
      }}
    >
      <Link href="/" style={{ color: 'white' }}>
        Home
      </Link>
      <Link href="/books" style={{ color: 'white' }}>
        Books
      </Link>
      <Link href="/members" style={{ color: 'white' }}>
        Members
      </Link>
      <Link href="/loans" style={{ color: 'white' }}>
        Loans
      </Link>
    </nav>
  );
}
