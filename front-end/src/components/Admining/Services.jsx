
import AdminService from "./Service";
import React from 'react';

export default class AdminServices extends React.Component {
    render()
    {
        return (
        <main id = 'main_admin'>
            {this.props.AdServices.map(el =>(<AdminService key={el.key} item={el} />))}
        </main>
        );
    }
}