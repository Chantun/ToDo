import React, { useState } from 'react';
import api from '../api/axios';
import '../style/entry.css';

function Entry({ msg, active, id, setNotes }) {
  const [value, setValue] = useState(active)

  const toggle = (id) => {
    setValue(prev => {
      const next = !prev;
      try {
        api.post('/note/toggle', {id: id, value: next})
        setNotes(prev =>
          prev.map(item => 
            item.id === id
              ? { ...item, active: next }
              : item
          )
        );
        return next;
      } catch (err) {
        console.log(err);
        return prev;
      }
    });
  }

  return (
    <div className="entry">
      <button className={`check ${value ? "check--active" : undefined}`} onClick={() => toggle(id)} >{active ? '✓' : undefined}</button>
      <p className={`note ${value ? "note--active" : undefined}`}>{msg}</p>
    </div>
  )
}

export default Entry;
