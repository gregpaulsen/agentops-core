'use client'

import { api } from '../lib/trpc'
import { Button, Card, CardContent, CardDescription, CardHeader, CardTitle } from '@paulyops/ui'
import { motion } from 'framer-motion'

export default function HomePage() {
  const { data: projects, isLoading } = api.projectRouter.list.useQuery()

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Welcome to PaulyOps
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Blazingly fast operations platform with AI-powered automation
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <Card>
              <CardHeader>
                <CardTitle>Projects</CardTitle>
                <CardDescription>
                  Manage your automation projects
                </CardDescription>
              </CardHeader>
              <CardContent>
                {isLoading ? (
                  <div className="text-center py-4">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {projects?.map((project) => (
                      <div key={project.id} className="p-3 bg-gray-50 rounded-lg">
                        <h3 className="font-medium">{project.name}</h3>
                        <p className="text-sm text-gray-500">
                          Created {new Date(project.createdAt).toLocaleDateString()}
                        </p>
                      </div>
                    ))}
                    {projects?.length === 0 && (
                      <p className="text-gray-500 text-center py-4">
                        No projects yet. Create your first one!
                      </p>
                    )}
                  </div>
                )}
                <Button className="w-full mt-4">
                  Create Project
                </Button>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Card>
              <CardHeader>
                <CardTitle>Automations</CardTitle>
                <CardDescription>
                  Set up AI-powered workflows
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="p-3 bg-green-50 rounded-lg border border-green-200">
                    <h3 className="font-medium text-green-800">Email Processing</h3>
                    <p className="text-sm text-green-600">Automated inbox management</p>
                  </div>
                  <div className="p-3 bg-purple-50 rounded-lg border border-purple-200">
                    <h3 className="font-medium text-purple-800">Data Analysis</h3>
                    <p className="text-sm text-purple-600">AI-powered insights</p>
                  </div>
                </div>
                <Button variant="outline" className="w-full mt-4">
                  View All
                </Button>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Card>
              <CardHeader>
                <CardTitle>Analytics</CardTitle>
                <CardDescription>
                  Monitor system performance
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Uptime</span>
                    <span className="font-medium text-green-600">99.9%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Active Jobs</span>
                    <span className="font-medium text-blue-600">12</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Success Rate</span>
                    <span className="font-medium text-green-600">98.5%</span>
                  </div>
                </div>
                <Button variant="outline" className="w-full mt-4">
                  View Details
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  )
}
