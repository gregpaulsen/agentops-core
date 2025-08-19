'use client'

import { useRive } from '@rive-app/react-canvas'
import { motion } from 'framer-motion'

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  useRiveAnimation?: boolean
  riveSrc?: string
  className?: string
}

export function LoadingSpinner({ 
  size = 'md', 
  useRiveAnimation = false, 
  riveSrc = '/rive/spinner.riv',
  className = ''
}: LoadingSpinnerProps) {
  const { RiveComponent } = useRive({
    src: riveSrc,
    autoplay: true,
    stateMachines: 'State Machine 1'
  })

  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  }

  if (useRiveAnimation) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.2 }}
        className={`${sizeClasses[size]} ${className}`}
      >
        <RiveComponent />
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, rotate: -180 }}
      animate={{ opacity: 1, rotate: 0 }}
      transition={{ duration: 0.3 }}
      className={`${sizeClasses[size]} ${className}`}
    >
      <div className="animate-spin rounded-full border-2 border-gray-300 border-t-blue-600 w-full h-full"></div>
    </motion.div>
  )
}

export function LoadingPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <LoadingSpinner size="lg" className="mx-auto mb-4" />
        <p className="text-gray-600">Loading...</p>
      </div>
    </div>
  )
}
