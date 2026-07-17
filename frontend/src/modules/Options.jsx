import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import '../style/entry.css';

function Options({ setClear, setFilter, filter, count }) {

  const handleClear = async () => {
    await api.delete("/api/note/clear");
    setClear(prev => !prev);
  }

  return (
    <div className="entry entry--options entry--no-border">
      <span className="option option--left">{count} items</span>
      <div className="filter__box">
        <span className={filter === 'all' ? 'option option--selected' : 'option'} onClick={() => setFilter('all')} >All</span>
        <span className={filter === 'active' ? 'option option--selected' : 'option'} onClick={() => setFilter('active')} >Active</span>
        <span className={filter === 'completed' ? 'option option--selected' : 'option'} onClick={() => setFilter('completed')} >Completed</span>
      </div>
      <span className="option option--clear" onClick={handleClear}>Clear Completed</span>
    </div>
  )
}

export default Options;
