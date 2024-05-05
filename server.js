// server.js
const express = require('express');
const fs = require('fs');
const csv = require('csv-parser');

const app = express();

app.get('/api/csv-data', (req, res) => {
  console.log(req.query)
  // const filePath = req.query.filePath;

  const filePath = "../data/iris/Iris.csv"
  console.log(filePath)

  // if (!filePath) {
  //   return res.status(400).json({ error: 'File path is required' });
  // }

  // const data = [];
  // fs.createReadStream(filePath)
  //   .pipe(csv())
  //   .on('data', (row) => {
  //     data.push(row);
  //   })
  //   .on('end', () => {
  //     res.json(data);
  //   });
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
