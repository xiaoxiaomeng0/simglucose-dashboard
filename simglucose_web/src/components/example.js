import React, { Component } from 'react';
import Dropdown from 'react-bootstrap/Dropdown';

class Example extends Component {
  state = {
    selectedValue: "Select Patient Name",
  }

  handleChange = (eventKey) => {
    // key_to_show = {'adult#001': 'adult1', 'adult#002': 'adult2', 'adult#003': 'adult3'}
    this.setState({ selectedValue: eventKey })
    // this.setState({ selectedValue: event.target.value })
    // console.log(this.state.selectedValue)
    // yarnconsole.log(eventKey)
    // console.log(event)
  }

  render() { 

    return ( 
      <div>
      <Dropdown>
      <Dropdown.Toggle variant="success" id="dropdown-basic">
          {this.state.selectedValue}
      </Dropdown.Toggle>
      
      <Dropdown.Menu>
        {/* onChange={this.handleChange} */}
          <Dropdown.Item eventKey='adult#001' onSelect={this.handleChange}>adult#001</Dropdown.Item>
          <Dropdown.Item eventKey="adult#002" onSelect={this.handleChange}>adult#002</Dropdown.Item>
          <Dropdown.Item eventKey="adult#003" onSelect={this.handleChange}>adult#003</Dropdown.Item>
      </Dropdown.Menu>
      </Dropdown>
      <h4>The Selected is : {this.state.selectedValue}</h4>
      
      </div>

    );
  }
}
 
export default Example;