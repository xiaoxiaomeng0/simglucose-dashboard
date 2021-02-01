import React, { Component } from "react";
import PatientIDDropdown from "./components/patientIDDropdown";
import Chart from "./components/chart";
import "./App.css";

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: [],
      selectedValue: "adult#001",
    };
  }

  handleChange = (eventKey) => {
    this.setState({ selectedValue: eventKey });
  };

  componentDidMount() {
    this.fetchData(this.state.selectedValue);
  }

  fetchData(patientID) {
    fetch(
      "http://localhost:8000/api/results/" + escape(patientID)
    )
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result,
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error,
          });
        }
      );
  }

  fetchPatientID() {
    fetch(
      "http://localhost:8000/api/results/allPatientID"
    )
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result,
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error,
          });
        }
      );
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.state.selectedValue !== prevState.selectedValue) {
      this.fetchData(this.state.selectedValue);
    }
  }

  render() {
    return (
      <div>
        <PatientIDDropdown
          handleChange={this.handleChange}
          selectedValue={this.state.selectedValue}
        />
        <Chart
          error={this.state.error}
          isLoaded={this.state.isLoaded}
          items={this.state.items}
        />
      </div>
    );
  }
}
