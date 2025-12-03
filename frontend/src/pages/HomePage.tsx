import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { logout } from '../services/authService';
import { getToken } from '../services/tokenService';
import '../styles/HomePage.css';

function HomePage() {
  const [username, setUsername] = useState('guest');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      const user = JSON.parse(storedUser);
      setUsername(user.username || 'guest');
    }
  }, []);

  const handleLogout = () => {
    logout();
    setUsername('guest');
    navigate('/');
  };

  const handleCheckProtected = async () => {
    const token = getToken();
    if (!token) {
      setMessage('❌ No token found');
      return;
    }

    try {
      const res = await fetch('http://localhost:5050/api/auth/protected', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await res.json();

      if (res.ok) {
        setMessage(`✅ ${data.message}`);
      } else {
        setMessage(`❌ ${data.error || 'Access denied'}`);
      }
    } catch (err) {
      setMessage('❌ Failed to connect to server');
    }
  };

  const isError = message.startsWith('❌');
  const isSuccess = message.startsWith('✅');

  return (
    <div className="home-page">
      <header className="home-header">
        <div className="home-logo">OnlineTranscribe</div>
        <div className="home-user">
          {username === 'guest' ? 'Guest' : `Signed in as ${username}`}
        </div>
      </header>

      <main className="home-main">
        <div className="home-card">
          <h1 className="home-title">Welcome to OnlineTranscribe</h1>
          <h2 className="home-subtitle">
            {username === 'guest'
              ? 'Log in or create an account to start transcribing your audio files.'
              : 'You are logged in. You can now access protected features.'}
          </h2>

          {message && (
            <div
              className={
                'home-message ' +
                (isSuccess ? 'home-message-success ' : '') +
                (isError ? 'home-message-error ' : '')
              }
            >
              <span>{message}</span>
            </div>
          )}

          <div style={{ marginTop: '2rem' }}>
            <div className="home-section-label">Actions</div>

            {username === 'guest' ? (
              <div className="home-actions">
                <Link to="/login">
                  <button className="home-btn home-btn-primary">Login</button>
                </Link>
                <Link to="/register">
                  <button className="home-btn home-btn-secondary">Register</button>
                </Link>
                <button
                  className="home-btn home-btn-ghost"
                  onClick={handleCheckProtected}
                >
                  Check Protected Endpoint
                </button>
              </div>
            ) : (
              <div className="home-actions">
                <button
                  className="home-btn home-btn-secondary"
                  onClick={handleLogout}
                >
                  Logout
                </button>
                <button
                  className="home-btn home-btn-ghost"
                  onClick={handleCheckProtected}
                >
                  Check Protected Endpoint
                </button>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default HomePage;