import React, { useState} from 'react';
import Login from './Logining/Login_admin';
import AdminShowServices from './Admining/ShowServices';
import './Admining/style.css';

async function AddService(credentials) {
  return fetch(`http://127.0.0.1:8000/api/add_service`, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  })
    .then(data => data.json());
}



export default function Admin(){
    
    const [token, setToken] = useState();
    let [newService, openNewService] = useState(false);
    let name_service = "";
    let price = 0;
    let showModal = () => {
      openNewService(!newService);
    };

    async function AddFunction (){
      let id_service = 0;
      console.log(JSON.stringify({
        id_service,
        name_service,
        price
    }));
      let result =  await AddService({
            id_service,
            name_service,
            price
        });
        console.log(result);
    }

    function setName (event){
      if (!/[А-яа-я \-]/.test(event.key)) {
          event.preventDefault();
          
      }
      else{
        var newName = document.getElementById('name').value + event.key;
        name_service = newName;
      }
      console.log('name is',name_service);
    }

    function setPrice (event){
      if (!/[0-9]/.test(event.key)) {
          event.preventDefault();
          
      }
      else{
        var newPrice = document.getElementById('price').value + event.key;        
        for(let i = 0; i < newPrice.length; i++)
        {
            if ( i === 0)
                price = newPrice[i]-'0';
            else
                price = price + newPrice[i]-'0'; 
        }
      }
    }

  if(token==null)
  {
    return <Login setToken={setToken} />
  }
    return(
        <div className='admin_div'>
            <label id="admin_label">Admin panel</label>
            <button id='add_div' onClick={showModal} hidden></button>
            <label htmlFor='add_div' className='btn_add'>+</label>
            {newService  && (
              <div
                className="change_div"
                open
              >
                <label id = 'change_service'>Добавить услугу</label>
                <label id = 'name_label'>Название услуги</label>
                <input type="text" id='name' maxLength="30" onKeyPress={(event) => setName(event)}></input>
                <br></br>
                <label id = 'price_label'>Цена услуги</label>
                <br></br>
                <input type="text" maxLength="5"  id='price'  onKeyPress={(event) => setPrice(event)}></input>
                <button id='add_btn' hidden onClick={AddFunction}></button>
                <label htmlFor='add_btn' className='btn_confirm'>Confirm</label>
              </div>
            )}
            <AdminShowServices/>
        </div>
    );
}

