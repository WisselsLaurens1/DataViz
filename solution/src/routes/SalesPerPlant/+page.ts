import { formatPath } from "../../helpers";

export const load = async ({ fetch }: any) => {
  const URL = `http://localhost:3000/json`;

  const response = await fetch(URL);
  const data = await response.json();
  return data["sales_per_plant_through_time"]

};
