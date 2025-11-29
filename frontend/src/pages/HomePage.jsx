import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { logout } from '../services/authService';
import { getToken } from '../services/tokenService'; // <-- make sure you have this

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

  return (
    <div className="home-container">
      <h1>Welcome to OnlineTranscribe</h1>
      <h2>Hello {username}</h2>
      {message && <p>{message}</p>}

      {username === 'guest' ? (
        <div>
          <Link to="/login"><button>Login</button></Link>
          <Link to="/register"><button>Register</button></Link>
          <button onClick={handleCheckProtected}>Check Protected Endpoint</button>
        </div>
      ) : (
        <div>
          <button onClick={handleLogout}>Logout</button>
          <button onClick={handleCheckProtected}>Check Protected Endpoint</button>
        </div>
      )}
    </div>
  );
}

export default HomePage;