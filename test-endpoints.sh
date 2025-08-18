#!/bin/bash

echo "🧪 Testing PaulyOps API Endpoints"
echo "=================================="

# Start the API server in background
echo "🚀 Starting API server..."
cd apps/api && pnpm dev &
API_PID=$!

# Wait for server to start
sleep 5

# Test health endpoint
echo ""
echo "📊 Testing /api/health"
curl -s http://localhost:3001/api/health | jq '.'

# Test authenticated endpoints with mock auth header
echo ""
echo "🔐 Testing authenticated endpoints..."

# Test telemetry endpoint
echo "📈 Testing /api/telemetry/event"
curl -s -X POST http://localhost:3001/api/telemetry/event \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mock-token" \
  -d '{"type": "test.event", "payload": {"test": true}}' | jq '.'

# Test incident reporting
echo ""
echo "🚨 Testing /api/incident/report"
curl -s -X POST http://localhost:3001/api/incident/report \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mock-token" \
  -d '{"message": "Test incident", "severity": "low"}' | jq '.'

# Test digest rendering
echo ""
echo "📋 Testing /api/digest/render"
curl -s -X POST http://localhost:3001/api/digest/render \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mock-token" \
  -d '{"days": 7}' | jq '.'

# Test inbox action
echo ""
echo "📬 Testing /api/inbox/action"
curl -s -X POST http://localhost:3001/api/inbox/action \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mock-token" \
  -d '{"action": "archive", "messageIds": ["msg1", "msg2"]}' | jq '.'

# Test NDVI job creation
echo ""
echo "🌱 Testing /api/ndvi/jobs"
curl -s -X POST http://localhost:3001/api/ndvi/jobs \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mock-token" \
  -d '{"source": "upload", "acres": 100}' | jq '.'

# Test unauthenticated request
echo ""
echo "🚫 Testing unauthenticated request"
curl -s -X POST http://localhost:3001/api/telemetry/event \
  -H "Content-Type: application/json" \
  -d '{"type": "test.event"}' | jq '.'

# Stop the API server
echo ""
echo "🛑 Stopping API server..."
kill $API_PID

echo ""
echo "✅ Testing complete!"
