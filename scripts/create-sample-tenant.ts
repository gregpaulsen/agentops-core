#!/usr/bin/env tsx

import { db } from '@paulyops/db'
import { organizations, users, memberships } from '@paulyops/db'

async function createSampleTenant() {
  try {
    console.log('Creating sample tenant...')
    
    // Create a sample organization
    const [org] = await db.insert(organizations).values({
      name: 'Sample Organization',
      slug: 'sample-org',
    }).returning()
    
    console.log(`Created organization: ${org.name} (${org.id})`)
    
    // Create a sample user
    const [user] = await db.insert(users).values({
      email: 'admin@sample-org.com',
      name: 'Sample Admin',
    }).returning()
    
    console.log(`Created user: ${user.name} (${user.email})`)
    
    // Create membership
    const [membership] = await db.insert(memberships).values({
      userId: user.id,
      organizationId: org.id,
      role: 'owner',
    }).returning()
    
    console.log(`Created membership: ${membership.role} role`)
    
    console.log('\n✅ Sample tenant created successfully!')
    console.log(`Organization: ${org.name}`)
    console.log(`Admin: ${user.name} (${user.email})`)
    console.log(`Role: ${membership.role}`)
    
  } catch (error) {
    console.error('❌ Error creating sample tenant:', error)
    process.exit(1)
  }
}

// Run the script
createSampleTenant()
