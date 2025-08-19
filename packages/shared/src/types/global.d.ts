/// <reference types="@total-typescript/ts-reset" />

// Global type augmentations for PaulyOps
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      NODE_ENV: 'development' | 'production' | 'test'
      DATABASE_URL: string
      NEXTAUTH_SECRET: string
      NEXTAUTH_URL: string
      LOG_LEVEL: string
      DOCTOR_SLACK_WEBHOOK_URL?: string
      DOCTOR_DISCORD_WEBHOOK_URL?: string
      // Add new environment variables for the stack migration
      NEON_DATABASE_URL?: string
      RESEND_API_KEY?: string
      UPLOADTHING_SECRET?: string
      UPLOADTHING_APP_ID?: string
    }
  }
}

export {}
