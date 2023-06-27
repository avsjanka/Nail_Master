import React from 'react';



async function RecordUser(credentials) {
    return fetch(`http://127.0.0.1:8000/api/recording_client`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    })
      .then(data => data.json());
}

export default class Service extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
         recOpen : false,
         date: "",
         time: '9',
         login: "",
         password: ""
        };
    }

    handleShowRec  = async () => {
        this.setState({recOpen: !this.state.recOpen});
    }
    
    setLogin= async () => {
        var newlogin = document.getElementById('login_text_mini').value;
        this.setState({login: newlogin}, function (){console.log(this.state.login)});
    }

    setDate= async () => {
        var newdate = document.getElementById('date').value;
        this.setState({date: newdate});
    }

    setTime =  (event) => {
        var newtime = document.getElementById('time').value;
        this.setState({time: newtime}, function (){console.log(this.state.time)});
    }

    setPassowrd= async () => {
        var newpassword = document.getElementById('password_text_mini').value;
        this.setState({password: newpassword});
    }

    Recording=async () =>{

        let service = this.props.item.props.fullService.id_service;
        let login = this.state.login;
        let password = this.state.password;
        let data = this.state.date;
        let time = this.state.time;
        let result = await RecordUser({
            login,
            password,
            time,
            data,
            service
        });
          console.log(result)
    }

    render()
    {
        return(
            <div className={'service'}>
                <label className="service_name">{this.props.item.props.fullService.name_service}</label>
                <button id='price' hidden></button>
                <label  htmlFor = 'price' className='price_bth' onClick={this.handleShowRec}>{this.props.item.props.fullService.price}</label>
                {this.state.recOpen && (
                    <div
                        className="login_mini"
                        open
                    >
                        <h1 id='name_service' >{this.props.item.props.fullService.name_service}</h1>
                        <input  type='date'  id= 'date'  min="2023-01-01" max="2023-12-31" onChange={this.setDate}></input >
                        <select id="time"  onChange={this.setTime}>
                            <option value='9'>9</option>
                            <option value='11'>11</option>
                            <option value='13'>13</option>
                            <option value='16'>16</option>
                            <option value='18'>18</option>
                        </select>
                        <label id="login_mini">Login</label>
                        <input type="text" id='login_text_mini' onChange={this.setLogin}></input>
                        <label id="password_mini">Password</label>
                        <input type="password" id = 'password_text_mini' onChange={this.setPassowrd}></input>
                        <button id='dialogbutton'
                                onClick={this.Recording} hidden></button>
                        <label htmlFor='dialogbutton' className='btn_mini'>Записаться</label>
                    </div>
                )}
            </div>
        );
    }
}
