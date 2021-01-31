import React, { PureComponent } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

class Chart extends PureComponent {
  render() {
    const { isLoaded, items, error } = this.props;

    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
        <LineChart
          width={500}
          height={300}
          data={items}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis>Bloodglucose</YAxis>
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="bg"
            stroke="#8884d8"
            activeDot={{ r: 8 }}
          />
          <Line type="monotone" dataKey="cgm" stroke="#82ca9d" />
        </LineChart>
      );
    }
  }
}

export default Chart;
