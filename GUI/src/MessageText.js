import React, { Component } from 'react';


class MessageText extends Component{

    render(){
    	return(
             <div className="message_input_wrapper">
                <input id="msg_input" className="message_input"
                   placeholder = "Type a message"
                   value = {this.props.message}
                   onChange = {this.props.onChange}
                   onKeyPress = {this.props.handleKeyPress}
                    />
             </div>
     	);
    }


}

export default MessageText; 