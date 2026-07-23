import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import Entry from './Entry';
import Options from './Options';

function Content({ update }) {
  const [notes, setNotes] = useState([]);
  const [clear, setClear] = useState(false);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    const getNotes = async () => {
      try {
        const response = await api.get("/note/get");
        setNotes(response.data);
      } catch (err) {
        console.error(err);
      }
    }

    getNotes()
  }, [update, clear])

  const filteredNotes = notes.filter(e => {
    if (filter === 'active')
      return !e.active;
    if (filter === 'completed')
      return e.active;
    return true;
  });

  return (
    <div className="container">
      <div className="container--notes">
        {filteredNotes.map((note) => (
          <Entry msg={note.content} active={note.active} id={note.id} setNotes={setNotes} key={note.id} />
        ))}
      </div>
      <Options setClear={setClear} setFilter={setFilter} filter={filter} count={filteredNotes.length} />
    </div>
  );
}

export default Content;
