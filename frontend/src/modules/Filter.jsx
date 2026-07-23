import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import '../style/entry.css';

function Filter({ setUpdate: setUpdate }) {
  const [value, setValue] = useState('');
  const [error, setError] = useState('');

  const addNote = async () => {
    try {
      const response = await api.post('/note/add', {content: value})
      console.log(response.data.note);
      setValue('');
      setError('');
      setUpdate(prev => !prev);
    } catch (err) {
      setError(err.response?.data?.detail);
    }
  }

  const handleKey = async (e) => {
    if (e.key === "Enter") {
      await addNote();
    }
  }

  return (
    <div className="container container--filter">
      <div className="entry entry--no-border">
        <button className="check check--add" onClick={addNote} />
        <input type="text" className="filter" value={value} onChange={e => setValue(e.target.value)} onKeyDown={handleKey} placeholder='Create a new todo...' />
      </div>
      <span className="error_span">{error}</span>
    </div>
  )
}

export default Filter;
