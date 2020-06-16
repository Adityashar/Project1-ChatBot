import React, { Component } from 'react';
import MessageContainer from './MessageContainer';
import MessageText from './MessageText'
import SendButton from './SendButton'
import './App.css';
import './Styling/style.css'; 
import './Styling/chat_interface.css'; 
import './Styling/temporary.css'; 


//import './chatappStyle/css/bootstrap.css'; 
//import './chatappStyle/css/style.css';

class App extends Component{
    
    constructor()
    {
       super()
       this.state = {
           "messages" : [],
           "current_message" : ""
       }

       this.handleClick = this.handleClick.bind(this);
       this.handleKeyPress = this.handleKeyPress.bind(this);
       this.onChange = this.onChange.bind(this);
       this.messageBox = this.messageBox.bind(this);
    }

    messageBox(Enter)
    {
        let messages = this.state.messages;
        let c_message = this.state.current_message;

         
        if(c_message && Enter)
        {
               messages = [...messages,{"message" : c_message}];

               this.setState({messages:messages});
               
               messages = [...messages,{"message" : "hi champ", "isbotmessage":true}];               
               this.setState({messages:messages});

               c_message ="";
               this.setState({current_message:c_message});               
        }
    }

    handleClick(event)
    {
          this.messageBox(true);
    }

    onChange(event)
    {
        this.setState({current_message:event.target.value});
    }

    handleKeyPress(event)
    {
         let key_pressed = false;
         if(event.key === 'Enter')
         {
             key_pressed = true;
         }

         this.messageBox(key_pressed);
    }

    render(){
       return(
           <div className="chat_window">
              <MessageContainer messages = {this.state.messages}/>
              <div className="bottom_wrapper clearfix">
                 <MessageText 
                 message = {this.state.current_message}
                 onChange = {this.onChange}
                 handleKeyPress = {this.handleKeyPress}/>
                 <SendButton handleClick = {this.handleClick}/>
              </div>
           </div> 
        );
    }
   

}


export default App;