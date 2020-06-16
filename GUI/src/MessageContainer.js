import React, { Component } from 'react';
import UserBox from './UserBox';


class MessageContainer extends Component{
     
     constructor(props)
     {
     	super(props);
     	this.displayMessages = this.displayMessages.bind(this);
     }


    scrollToBottom = () =>{
    	//let el = this.refs.scroll;
    	//el.scrollTop = el.scrollHeight;
    	console.log('hi');
    }

     componentDidMount()
     {
         this.scrollToBottom();
     }
     
     componentDidUpdate()
     {
         console.log('z');
         this.scrollToBottom();
     }

     displayMessages()
     {
     	 return this.props.messages.map((message,idx) => (
               <UserBox key = {idx} message = {message["message"]} appearance = {message["isbotmessage"]?"left":"right"}/>
     	));
     }

     render(){
        
     	return(
               <ul className="messages" ref="scroll">
                 {this.displayMessages()}
               </ul>
     		);
     }

}


export default MessageContainer;