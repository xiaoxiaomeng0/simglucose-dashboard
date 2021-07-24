import { csv } from "d3";

const csvUrl =
  "https://gist.githubusercontent.com/xiaoxiaomeng0/83a31edc87e3864dbba8a7ccd263af71/raw/simglucose_test.csv";

export const getData = async () => {
  const data = await csv(csvUrl);

  // Have a look at the attributes available in the console!
  console.log(data[0]);

  return data;
};
