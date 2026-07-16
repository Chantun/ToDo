import React, { useState } from 'react';
import api, { setAccessToken } from '../api/axios';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/api/auth/login', { email, password });
      
      // Guardamos el token únicamente en memoria (XSS Safe)
      setAccessToken(response.data.access_token);
      alert('¡Inicio de sesión exitoso!');
      
    } catch (err) {
      alert('Error al iniciar sesión: ' + err.response?.data?.detail);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" required />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" required />
      <button type="submit">Ingresar</button>
    </form>
  );
}

export default Login;
