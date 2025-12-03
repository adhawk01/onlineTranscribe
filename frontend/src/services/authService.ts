import { setToken, removeToken } from './tokenService';

const API_URL = import.meta.env.VITE_API_URL || 'https://localhost:5050/api/auth'


export async function login(email: string, password: string) {
  const res = await fetch(`${import.meta.env.VITE_API_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_email: email, user_password: password }),
  });

  const data = await res.json();

  if (res.ok && data.token) {
    setToken(data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
  }

  return data;
}

export async function register(name: string, email: string, password: string) {
  const res = await fetch(`${API_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_name: name, user_email: email, user_password: password }),
  })
  return res.json()
}

export async function logout() {
  removeToken();
  localStorage.removeItem('user');
}
