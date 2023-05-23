import React, { useState} from 'react';
import Login from './Logining/Login_admin';

export default function Admin(){
    const [showModal, setShowModal] = useState(false);
    const [token, setToken] = useState();

    const toggleShowModal = () => {
        setShowModal(!showModal);
    };

  function logout()
  {
    document.cookie = null;
    localStorage.setItem('jwt',null);
    setToken(null);
  }

  if(token==null)
  {
    return <Login setToken={setToken} />
  }
    return(
        <div>
            <p>Admin panel</p>
        </div>
    );
}