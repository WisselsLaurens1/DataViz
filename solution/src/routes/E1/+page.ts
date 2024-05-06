import { formatPath } from "../../helpers";


const preprocess = (dataDict: any) => {

    
}


export const load = async ({ fetch }: any) => {
  const FILE_PATH = "../data/suncharge/BOM.csv";
  const URL = `http://localhost:3000/data/${formatPath(FILE_PATH)}`;
  const response = await fetch(URL);
  const data = await response.json();
  return {
    result: preprocess({
        "sales": data
    }),
  };
};
