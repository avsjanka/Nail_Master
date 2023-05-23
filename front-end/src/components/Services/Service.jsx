
import React from 'react';

export default class Service extends React.Component {
    render()
    {
        return(
            <div className={'service'}>
                <label className="service_name">{this.props.item.title}</label>
                <button id='price' hidden></button>
                <label for = 'price' className="price_bth">{this.props.item.price}</label>
            </div>
        )
    }
}