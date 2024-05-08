import { formatPath } from "../../helpers";


const preprocess = (dataDict: any) => {
  
  
  return dataDict
    
}


export const load = async ({ fetch }: any) => {
  const URL = `http://localhost:3000/json`;

  const response = await fetch(URL);
  const data = await response.json();
  console.log(data)
  return {
    result: data["difference_between_forecast_and_sales"]
  };
};
