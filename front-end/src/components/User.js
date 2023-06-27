import React, { useState} from 'react';
import Login_User from './Logining/Login_user';





export default function User(){
    const [showModal, setShowModal] = useState(false);
    const [token, setToken] = useState();
    let [currentMonth, setCurrentMonth] = useState();
    const toggleShowModal = () => {
        setShowModal(!showModal);
    };

  function logout()
  {
    document.cookie = null;
    localStorage.setItem('jwt',null);
    setToken(null);
  }

  function MyMonthlyCalendar (){
    const current = new Date();
    currentMonth = current.getMonth()+1;
    
  }
  

  if(token==null)
  {
    const current = new Date();
    const date = `${current.getDate()}/${current.getMonth()+1}/${current.getFullYear()}`;
    console.log(date);
    console.log(currentMonth);
    return <Login_User setToken={setToken} />
  }
  return(
    <div className="user_panel">
      <label id = "label_user" >User  panel</label>
    </div>
  );
}
