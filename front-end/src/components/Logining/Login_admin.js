import React, {useState} from "react";
import PropTypes from 'prop-types';
import './Login.css'

async function loginUser(credentials) {
  return fetch(`http://127.0.0.1:8000/api/login_admin`, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  })
    .then(data => data.json());
}

export default function Login({setToken}){

    const [login, setLogin] = useState();
    const [password, setPassword] = useState();

    const handleSubmit = async e => {
      e.preventDefault();

      let token = await loginUser({
          login,
          password
      });
        console.log(token)
        let myObject = JSON.stringify(token);
        if( myObject === '{"detail":"Forbidden"}' || myObject.startsWith('{"type":"https://tools.ietf.org/html/rfc7231#section-6.5.1","title":"One or more validation errors occurred."') )
        {
          myObject = null;
          <p>Неверный пароль</p>
        }
      localStorage.setItem('jwt',myObject);
      setToken(myObject);
  }

    return (
            <div>
                <div className="login">
                  <div>
                    <label id="margo_label_reg">Margo Nails</label>
                  </div>
                    <div>
                        <label id="login">Login</label>
                        <input id="login_text" type="text" className="TextPlace"  onChange={e => setLogin(e.target.value)}></input>
                    </div>
                    <div>
                        <label id="password">Password</label>
                        <input id="password_text" type="password" className="TextPlace" onChange={e => setPassword(e.target.value)}></input>
                    </div>
                    <div>
                        <button type="submit" id = "submit" onClick ={handleSubmit} hidden>Login</button>
                        <label for = "submit" className="button">Login</label>
                    </div>
                </div>
            </div>
    );
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired
 };