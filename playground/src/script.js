const names = [
    "Laurens",
    "Arnaud",
    "Wout"
]


const getData = async () => {
    const data = await fetch("http://localhost:3000/..:data:iris:Iris.csv")
    return data
}

let data = getData()