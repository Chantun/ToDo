import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import '../style/title.css';

function Title() {
  const [user, setUser] = useState('');

  const handleLogout = async () => {
    await api.post(
      'api/auth/logout'
    );
    window.location.href = "/";
  }

  useEffect(() => {
    async function loadUser() {
      try {
        const response = await api.get('/api/me');
        setUser(response.data);
      } catch (err) {
        console.error(err);
      }
    }

    loadUser();
  }, [])

  return (
    <div className='title__container'>
      <h2 className="title">TODO</h2>
      <div className="title--credentials">
        <p className="user">{user}</p>
        <span className="logout" onClick={handleLogout}>Cerrar Sesion</span>
      </div>
    </div>
  )
}

export default Title;
