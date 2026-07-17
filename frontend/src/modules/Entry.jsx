import React, { useState } from 'react';
import api from '../api/axios';
import '../style/entry.css';

function Entry({ msg, active, id }) {
  const [value, setValue] = useState(active)

  const toggle = (id) => {
    setValue(prev => {
      const next = !prev;
      try {
        api.post('/api/note/toggle', {id: id, value: next})
        return next;
      } catch (err) {
        console.log(err);
        return prev;
      }
    });
  }

  return (
    <div className="entry">
      <input type="checkbox" className="check" defaultChecked={active} onChange={() => toggle(id)} />
      <p className="note">{msg}</p>
    </div>
  )
}

export default Entry;
