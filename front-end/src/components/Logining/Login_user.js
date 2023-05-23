import React, {useState} from "react";
import axios from "axios";
import PropTypes from 'prop-types';
import './Login.css'
import {loginUser} from './login_func.js'



export default function Login_User({setToken}){

    const [login, setLogin] = useState();
    const [password, setPassword] = useState();

    function registrate()
    {
        const url = `${window.location.origin}/backend/adduser`;
        return axios.post(url,{
            login,
            password
        }).then(response => response.status);
    }

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
                    <label for = "submit" className="btn">Login</label>
                    <button type="submit" id = "reg" hidden onClick={registrate} >Registrate</button>
                    <label  for = "reg" className="reg_button" >Registrate</label>
                </div>
            </div>
        </div>
);
}

Login_User.propTypes = {
setToken: PropTypes.func.isRequired
};
