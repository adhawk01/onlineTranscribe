import '../styles/AuthForm.css';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/authService';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await login(email, password);

      if (res.token) {
        setMessage('✅ Logged in successfully!');
        navigate('/');
      } else {
        setMessage(`❌ Login failed: ${res.error || 'Unknown error'}`);
      }
    } catch {
      setMessage('❌ Error connecting to server');
    }
  };

  const isError = message.startsWith('❌');
  const isSuccess = message.startsWith('✅');

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2 className="auth-title">Login</h2>
        <p className="auth-subtitle">Welcome back, please sign in</p>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="auth-field">
            <label className="auth-label" htmlFor="login-email">
              Email
            </label>
            <input
              id="login-email"
              type="email"
              className="auth-input"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
            />
          </div>

          <div className="auth-field">
            <label className="auth-label" htmlFor="login-password">
              Password
            </label>
            <input
              id="login-password"
              type="password"
              className="auth-input"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>

          <button type="submit" className="auth-button">
            Login
          </button>
        </form>

        {message && (
          <p
            className={
              'auth-message ' +
              (isSuccess ? 'auth-message--success ' : '') +
              (isError ? 'auth-message--error ' : '')
            }
          >
            {message}
          </p>
        )}
      </div>
    </div>
  );
}