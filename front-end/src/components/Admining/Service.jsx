import React from 'react';
import './style.css';


async function ChangeService(credentials) {
    return fetch(`http://127.0.0.1:8000/api/update_service`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    })
      .then(data => data.json());
}

async function DeleteService(credentials) {
    return fetch(`http://127.0.0.1:8000/api/delete_service`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    })
      .then(data => data.json());
}

export default class AdminService extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
         updateOpen : false,
         name : this.props.item.props.fullService.name_service,
         price : this.props.item.props.fullService.price
        };
    }

    handleUdateService  = async () => {
        this.setState({updateOpen: !this.state.updateOpen});
        console.log(this);
    }

    setName = async(event) =>{
        if (!/[А-яа-я \-]/.test(event.key)) {
            event.preventDefault();
        }
        else{
            var newName = document.getElementById('name').value + event.key;
            this.setState({name: newName});
        }
    }

    setPrice = (event) =>{
        console.log(this.props.item.props.fullService.id_service);
        if (!/[0-9]/.test(event.key)) {
              event.preventDefault();
        }
        else{
            var newPrice = document.getElementById('price').value + event.key;
            this.setState({price: newPrice});
        }
    }

    Delete = async () => {
        let id_service = this.props.item.props.fullService.id_service;
        let name_service = this.state.name;
        let price = this.state.price;

        await DeleteService({
            id_service,
            name_service,
            price
        });
        
    }

    Update = async () =>{
        let id_service = this.props.item.props.fullService.id_service;
        let name_service = this.state.name;
        let price_str = this.state.price;
        let price = 0;
        if( typeof(price_str) === "string")
        {
            for(let i = 0; i < price_str.length; i++)
            {
                if ( i === 0)
                    price = price_str[i]-'0';
                else
                    price = price + price_str[i]-'0'; 
            }
        }
        else
            price = price_str;

        await ChangeService({
            id_service,
            name_service,
            price
        });
    }

    render()
    {
        return(
            <div className={'service_admin'}>
                <label className="service_admin_name">{this.props.item.props.fullService.name_service}</label>
                <label  className='price'>{this.props.item.props.fullService.price}</label>
                <div className='doing'>
                    <button id='deletebutton' hidden></button>
                    <label htmlFor='deletebutton' className='btn_delete' onClick={this.Delete}>Delete</label>
                    <button id='dialogbutton' hidden ></button>
                    <label htmlFor='dialogbutton' className='btn_change' onClick={this.handleUdateService}>Update</label>
                </div>
                {this.state.updateOpen && (
                    <div
                        className="change_div"
                        open
                    >
                        <label id = 'change_service'>Изменить услугу</label>
                        <label id = 'name_label'>Название услуги</label>
                        <input type="text" id='name' defaultValue={this.props.item.props.fullService.name_service} maxLength="30" onKeyPress={(event)=>this.setName(event)}></input>
                        <br></br>
                        <label id = 'price_label'>Цена услуги</label>
                        <br></br>
                        <input type="text"  maxLength="5" id='price'  defaultValue={this.props.item.props.fullService.price}  onKeyPress={(event)=> this.setPrice(event)}></input>
                        <button id='confirmbutton' hidden onClick={this.Update}></button>
                        <label htmlFor='confirmbutton' className='btn_confirm'>Confirm</label>
                    </div>
                )}
            </div>
        );
    }
}


