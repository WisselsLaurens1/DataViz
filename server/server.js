// server.js
const express = require("express");
const fs = require("fs");
const csv = require("csv-parser");
const cors = require("cors"); // Import cors middleware


const app = express();
app.use(cors({
  origin: "*" // Allow requests from any origin
}));

app.get("/data/:path", (req, res) => {
  let filePath = req.params.path;
  filePath = filePath.replace(/:/g, "/");

  if (!filePath) {
    return res.status(400).json({ error: "File path is required" });
  }
  try {
    const data = [];
    fs.createReadStream(filePath)
      .pipe(csv())
      .on("data", (row) => {
        data.push(row);
      })
      .on("end", () => {
        res.json(data);
      });
  } catch (e) {
    return res.status(400).json({ error: "Failed to retrieve data" });
  }
});

app.get("/json", (req, res) => {
  fs.readFile('../data/data.json', 'utf8', (err, data) => {
    if (err) {
      return res.status(400).json({ error: "Failed to retrieve data" });
    }
    try {
      const jsonData = JSON.parse(data);
      return res.json(jsonData);
    } catch (error) {
      return res.status(400).json({ error: "Failed to retrieve data" });    }
  });
})

app.listen(3000, () => {
  console.log("Server is running on port 3000");
});
