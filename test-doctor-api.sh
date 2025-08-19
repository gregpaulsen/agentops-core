#!/bin/bash

echo "🧪 Testing PaulyOps System Doctor API"
echo "====================================="

# Start the API server in the background
echo "Starting API server..."
pnpm --filter @paulyops/api dev &
API_PID=$!

# Wait for server to start
sleep 5

echo ""
echo "📊 Testing /api/doctor/status"
echo "-----------------------------"
curl -s http://localhost:3000/api/doctor/status | jq '.'

echo ""
echo "🔧 Testing /api/doctor/run (scan mode)"
echo "--------------------------------------"
curl -s -X POST http://localhost:3000/api/doctor/run \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer mock-token' \
  -d '{"mode":"scan"}' | jq '.'

echo ""
echo "🛑 Stopping API server..."
kill $API_PID

echo ""
echo "✅ Doctor API tests completed!"
