import React, { useState} from 'react';
import Login_User from './Logining/Login_user';
export default function User(){
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
    return <Login_User setToken={setToken} />
  }
    return(
        <div>
            <p>User  panel</p>
        </div>
    );
}