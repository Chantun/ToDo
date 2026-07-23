import React, { useState } from 'react';
import api, { setAccessToken } from '../api/axios';
import "../modules/Header";
import "../style/login.css";
import Header from '../modules/Header';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/auth/login', { email, password });
      setAccessToken(response.data.access_token);
      window.location.href = "/";
    } catch (err) {
      if (err.response.status == 401) {
        setError("Credenciales incorrectas");
      } else if (err.response.status == 422) {
        setError("Correo electronico invalido");
      } else {
        setError(err.response?.data?.detail);
      }
    }
  };

  return (
    <>
      <Header />
      <main>
        <div className="title__container">
          <h2 className="title">LOGIN</h2>
        </div>
        <div className="container">
          <form onSubmit={handleLogin}>
            <label>
              Email:
              <input type="email" className='login__input' value={email} onChange={e => setEmail(e.target.value)} placeholder='example@test.com' required/>
            </label>
            <label>
              Password:
              <input type="password" className='login__input' onChange={e => setPassword(e.target.value)} placeholder='1234' required/>
            </label>
            <span className="error_span">{error}</span>
            <div className="button__container">
              <button type="submit" className='submit'>Iniciar sesion</button>
              <button onClick={() => {window.location.href = "/register"}} className='submit'>Registrarme</button>
            </div>
          </form>
        </div>
      </main>
    </>
  )
}

export default Login;
