import { formatPath } from "../../helpers";


const preprocess = (dataDict: any) => {
}

export const load = async ({ fetch }: any) => {
  const FILE_PATH = "../data/suncharge/Sales.csv";
  const URL = `http://localhost:3000/json`;

  const response = await fetch(URL);
  const data = await response.json();
  return {
    result: data["average_delay_of_sales_per_month"]
  };
};
