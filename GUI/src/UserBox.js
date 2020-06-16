import React, { Component } from 'react';


class UserBox extends Component{

    render(){
    	return(
    		<li className={`message ${this.props.appearance} appeared`}>
            
            <div className="text_wrapper">
                <div className="text">
                    {this.props.message}
                </div> 
            </div>
            </li>
    	);
    }
}


export default UserBox;