import React, { useState } from 'react';
import api, { setAccessToken } from '../api/axios';
import "../modules/Header";
import "../style/login.css";
import Header from '../modules/Header';

function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    if (password != confirm) {
      setError("Las contrasenas no coinciden");
      return;
    }

    try {
      const response = await api.post('/api/auth/register', { email, password });
      window.location.href = "/login";
    } catch (err) {
      if (err.response.status == 422) {
        setError("Correo electronico invalido");
      } else {
        setError(err.response?.data?.detail);
      }
    }
  }

  return (
    <>
      <Header />
      <main>
        <div className="title__container">
          <h2 className="title">REGISTER</h2>
        </div>
        <div className="container">
          <form onSubmit={handleRegister}>
            <label>
              Email:
              <input type="email" className='login__input' value={email} onChange={e => setEmail(e.target.value)} placeholder='example@test.com' required/>
            </label>
            <label>
              Password:
              <input type="password" className='login__input' onChange={e => setPassword(e.target.value)} placeholder='1234' required/>
            </label>
            <label>
              Password x2:
              <input type="password" className='login__input' onChange={e => setConfirm(e.target.value)} placeholder='1234' required/>
            </label>
            <span className="error_span">{error}</span>
            <div className="button__container">
              <button type="submit" className='submit'>Registrarme</button>
              <button className='submit' onClick={() => {window.location.href = "/login"}}>Iniciar sesion</button>
            </div>
          </form>
        </div>
      </main>
    </>
  )
}

export default Register;
