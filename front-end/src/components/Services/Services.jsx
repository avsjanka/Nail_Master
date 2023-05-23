import {Component} from "react";
import Service from "./Service";
import React from 'react';

export default class Services extends React.Component {
    render()
    {
        return (
        <main>
            {this.props.Services.map(el =>(<Service key={el.id} item={el} />))}
        </main>
        );
    }
}