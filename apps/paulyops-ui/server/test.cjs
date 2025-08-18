const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.json({ message: 'Test server working!', timestamp: new Date().toISOString() });
});

app.get('/api/test', (req, res) => {
  res.json({ status: 'ok', message: 'API endpoint working!' });
});

const PORT = 8787;
app.listen(PORT, () => {
  console.log(`✅ Test server listening on http://localhost:${PORT}`);
  console.log(`📡 Try: curl http://localhost:${PORT}/api/test`);
});
