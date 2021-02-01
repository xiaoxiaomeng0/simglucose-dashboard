import React, { Component } from 'react';
import Dropdown from 'react-bootstrap/Dropdown';

class PatientIDDropdown extends Component {
    
    render()  {
        const {fetchPatientIDItems, handleChange, selectedValue} = this.props
        
        return ( 
            <Dropdown>
            <Dropdown.Toggle variant="success" id="dropdown-basic">
                {selectedValue}
            </Dropdown.Toggle>
            
            <Dropdown.Menu> {
                fetchPatientIDItems.map((patientID) => 
                <Dropdown.Item
                key={patientID}
                eventKey={patientID} 
                onSelect={handleChange}>
                {patientID}
                </Dropdown.Item>)
            }
            </Dropdown.Menu>
            </Dropdown>
         );
        }
}
 
export default PatientIDDropdown;