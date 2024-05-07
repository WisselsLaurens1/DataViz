import { formatPath } from "../../helpers";


const preprocess = (dataDict: any) => {
}


export const load = async ({ fetch }: any) => {
  const URL = `http://localhost:3000/json`;

  const response = await fetch(URL);
  const data = await response.json();
  return data
};