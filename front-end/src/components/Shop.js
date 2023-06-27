import React from 'react';
import ShowServices from './Services/ShowServices';
import { Link } from 'react-router-dom';

export default function Shop(){


    return(
    <>
        <div id="margo">
            <label id="margo_label">Margo Nails</label>
            <ul className = 'nav'>
                <Link to = "https://t.me/NailMasterMargo_bot"><li id = 'tg'>Record in Telegramm</li></Link>
                <li>Contacts</li>
                <Link to = "/user"><li id='link'>Log in</li></Link>
            </ul> 
        </div>
        <div>
            <ShowServices />
        </div>
        <br></br>
    </>
    );
}


