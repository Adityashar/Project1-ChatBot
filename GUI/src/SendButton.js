import React, { Component } from 'react';
import image from './Styling/send-button-png-6.png';

class SendBUtton extends Component{
 
 render()
 {
       return(
                 
            <div className="send_message" onClick = {this.props.handleClick}>
              <div ><img src={image}></img></div>
            </div>

           
                
       	);
 }

}

export default SendBUtton; 
