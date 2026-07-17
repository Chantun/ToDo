import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import '../style/content.css';
import '../style/entry.css';

function Filter({ setUpdate: setUpdate }) {
  const [value, setValue] = useState('');
  const [error, setError] = useState('');

  const addNote = async () => {
    try {
      const response = await api.post('/api/note/add', {content: value})
      console.log(response.data.note);
      setUpdate(prev => !prev);
    } catch (err) {
      setError(err.response?.data?.detail);
    }
  }

  return (
    <div className="container container--filter">
      <div className="entry entry--no-border">
        <button onClick={addNote} />
        <input type="text" className="filter" onChange={e => setValue(e.target.value)} placeholder='Create a new todo...' />
      </div>
      <span className="error_span"></span>
    </div>
  )
}

export default Filter;
