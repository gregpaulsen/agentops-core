import { GET } from './route'
import { NextRequest } from 'next/server'

describe('/api/health', () => {
  it('should return ok: true and db status', async () => {
    const req = new NextRequest('http://localhost:3001/api/health')
    const response = await GET(req)
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(data.ok).toBe(true)
    expect(typeof data.time).toBe('string')
    expect(['up', 'down']).toContain(data.db)
  })
})
