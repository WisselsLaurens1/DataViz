export const load = async ({ fetch }: any) => {
  const response = await fetch("http://localhost:3000/data/..:data:iris:Iris.csv")
  const data = await response.json()
  console.log(data)
  return {
    data: data
  }
}