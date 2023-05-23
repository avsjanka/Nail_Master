import React, {useState} from "react";
import PropTypes from 'prop-types';
import './Login.css'
import {loginUser} from './login_func.js';



export default function Login({setToken}){

    const [login, setLogin] = useState();
    const [password, setPassword] = useState();

    const handleSubmit = async e => {
        e.preventDefault();

        let token = await loginUser({
            login,
            password
        });
        
       
          let myObject = JSON.stringify(token);
          if( myObject === '{"errorText":"Invalid username or password."}' || myObject.startsWith('{"type":"https://tools.ietf.org/html/rfc7231#section-6.5.1","title":"One or more validation errors occurred."') )
          {
            myObject = null;
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