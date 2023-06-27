
import Service from "./Service";
import React from 'react';

export default class Services extends React.Component {
    render()
    {
        return (
        <main>
            {this.props.Services.map(el =>(<Service key={this.props.Services.id} item={el} />))}
        </main>
        );
    }
}