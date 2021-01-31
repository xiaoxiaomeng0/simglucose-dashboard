import React, { Component } from 'react';
import Dropdown from 'react-bootstrap/Dropdown';

class PatientIDDropdown extends Component {
    
    render()  {
        const {handleChange, selectedValue} = this.props 
        return ( 
            <Dropdown>
            <Dropdown.Toggle variant="success" id="dropdown-basic">
                {selectedValue}
            </Dropdown.Toggle>
            
            <Dropdown.Menu>
                <Dropdown.Item eventKey="adult#001" onSelect={handleChange}>adult#001</Dropdown.Item>
                <Dropdown.Item eventKey="adult#002" onSelect={handleChange}>adult#002</Dropdown.Item>
                <Dropdown.Item eventKey="adult#003" onSelect={handleChange}>adult#003</Dropdown.Item>
            </Dropdown.Menu>
            </Dropdown>
         );
        }
}
 
export default PatientIDDropdown;