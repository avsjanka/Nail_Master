
import React from 'react';
import Services from "./Services";
import Service from './Service';




export default class ShowServices extends React.Component {
    constructor(props) {
        super(props);

        this.state={
            currentServices: [],
            services: []
        }
        this.state.currentServices = this.state.services
    }
    componentDidMount() {
        this.Services();
    }
    
    async Services()
    {
        async function makeServices() {
            return fetch(`http://127.0.0.1:8000/api/show_services`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            })
                .then(data => data.json());
        };
        const AllPosts = await makeServices();
        let newPosts = [];
        for (let i = AllPosts.length; i--;)
        {
            console.log(AllPosts[i]);
            newPosts = newPosts.concat(<Service fullService = {AllPosts[i]}/>);
        }
        this.setState( {currentServices: newPosts});
    }

    render() {
        return (
            <div className='services'>
                <Services Services={this.state.currentServices} />
            </div>
        );
    }
}
