import React, { useState} from 'react';
import ShowServices from './Services/ShowServices';

export default function Shop(){
    return(
    <>
        <div id="margo">
            <label id="margo_label">Margo Nails</label>
        </div>
        <div>
            <ShowServices />
        </div>
        <br></br>
        <div id = "contacts"></div>
    </>
    );
}


