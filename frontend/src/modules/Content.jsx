import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import Entry from './Entry';
import '../style/content.css';

function Content({ update }) {
  const [notes, setNotes] = useState([]);

  useEffect(() => {
    const getNotes = async () => {
      try {
        const response = await api.get("/api/note/get");
        setNotes(response.data);
      } catch (err) {
        console.error(err);
      }
    }

    getNotes()
  }, [update])

  return (
    <div className="container">
      {notes.map((note) => (
        <Entry msg={note.content} active={note.active} id={note.id} key={note.id} />
      ))}
    </div>
  );
}

export default Content;
