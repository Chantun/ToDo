import axios from 'axios';

function Main() {

  async function logout() {
    await axios.post(
      'http://localhost:8000/api/auth/logout',
      {},
      { withCredentials: true }
    );
  }

  return (
    <>
    <button onClick={logout}>
      Click Me
    </button>
    </>
  )
}

export default Main;