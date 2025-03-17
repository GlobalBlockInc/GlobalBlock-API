// Auto-generated API Server Skeleton for GlobalBlockInc
const express = require('express');
const app = express();
const port = 4000;

app.get('/status', (req, res) => {
  res.send('GlobalBlock API Server is running!');
});

app.listen(port, () => {
  console.log(`GlobalBlock API listening on port ${port}`);
});
