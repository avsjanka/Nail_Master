
import React from 'react';
import Services from "./Services";
import Service from './Service';

export default class ShowServices extends React.Component {
    constructor(props) {
        super(props);

        this.state={
            currentServices: [],
            services: [
                {
                    id: 0,
                    title: 'Lab0',
                    price: '100'
                },
                {
                    id: 1,
                    title: 'Lab1',
                    price: '100'
                },
                {
                    id: 3,
                    title: 'Lab3',
                    price: '10'
                },
                {
                    id: 4,
                    title: 'Lab4',
                    price: '10000'
                },
                {
                    id: 2,
                    title: 'Lab2',
                    price: '101'
                },
                {
                    id: 5,
                    title: 'Lab55',
                    price: '101'
                }
            ]
        }
        this.state.currentServices = this.state.services
    }

    render() {
        return (
            <div className='services'>
                <Services Services={this.state.currentServices} />
            </div>
        );
    }
}
