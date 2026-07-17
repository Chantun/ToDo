import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import Header from '../modules/Header';
import Title from '../modules/Title';
import Filter from '../modules/Filter';
import Content from '../modules/Content';

function Main() {
  const [user, setUser] = useState('');
  const [update, setUpdate] = useState(false);

  return (
    <>
      <Header />
      <main>
        <Title />
        <Filter setUpdate={setUpdate} />
        <Content update={ update } />
      </main>
    </>
  )
}

export default Main;