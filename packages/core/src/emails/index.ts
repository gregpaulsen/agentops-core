import { Resend } from 'resend'

// Email template types
export interface EmailTemplate {
  subject: string
  html: string
  text?: string
}

export interface OnboardingEmailData {
  name: string
  email: string
  organizationName: string
}

export interface JobNotificationEmailData {
  name: string
  email: string
  jobName: string
  jobStatus: 'completed' | 'failed'
  jobResult?: any
}

// Email templates
export const createOnboardingEmail = (data: OnboardingEmailData): EmailTemplate => ({
  subject: `Welcome to PaulyOps, ${data.name}!`,
  html: `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
      <h1 style="color: #2563eb;">Welcome to PaulyOps!</h1>
      <p>Hi ${data.name},</p>
      <p>Welcome to PaulyOps! Your organization <strong>${data.organizationName}</strong> has been set up successfully.</p>
      <p>You can now start using our powerful automation tools to streamline your operations.</p>
      <div style="background-color: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3>Next Steps:</h3>
        <ul>
          <li>Explore your dashboard</li>
          <li>Set up your first automation</li>
          <li>Invite team members</li>
        </ul>
      </div>
      <p>If you have any questions, feel free to reach out to our support team.</p>
      <p>Best regards,<br>The PaulyOps Team</p>
    </div>
  `,
  text: `
    Welcome to PaulyOps!
    
    Hi ${data.name},
    
    Welcome to PaulyOps! Your organization ${data.organizationName} has been set up successfully.
    
    You can now start using our powerful automation tools to streamline your operations.
    
    Next Steps:
    - Explore your dashboard
    - Set up your first automation
    - Invite team members
    
    If you have any questions, feel free to reach out to our support team.
    
    Best regards,
    The PaulyOps Team
  `
})

export const createJobNotificationEmail = (data: JobNotificationEmailData): EmailTemplate => ({
  subject: `Job ${data.jobStatus}: ${data.jobName}`,
  html: `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
      <h1 style="color: ${data.jobStatus === 'completed' ? '#059669' : '#dc2626'};">
        Job ${data.jobStatus === 'completed' ? 'Completed' : 'Failed'}: ${data.jobName}
      </h1>
      <p>Hi ${data.name},</p>
      <p>Your job <strong>${data.jobName}</strong> has ${data.jobStatus}.</p>
      ${data.jobStatus === 'completed' && data.jobResult ? `
        <div style="background-color: #f0fdf4; padding: 20px; border-radius: 8px; margin: 20px 0;">
          <h3>Job Results:</h3>
          <pre style="background-color: white; padding: 10px; border-radius: 4px; overflow-x: auto;">
            ${JSON.stringify(data.jobResult, null, 2)}
          </pre>
        </div>
      ` : ''}
      <p>You can view the full details in your PaulyOps dashboard.</p>
      <p>Best regards,<br>The PaulyOps Team</p>
    </div>
  `,
  text: `
    Job ${data.jobStatus === 'completed' ? 'Completed' : 'Failed'}: ${data.jobName}
    
    Hi ${data.name},
    
    Your job ${data.jobName} has ${data.jobStatus}.
    
    ${data.jobStatus === 'completed' && data.jobResult ? `
    Job Results:
    ${JSON.stringify(data.jobResult, null, 2)}
    ` : ''}
    
    You can view the full details in your PaulyOps dashboard.
    
    Best regards,
    The PaulyOps Team
  `
})

// Email service
export class EmailService {
  private resend: Resend
  
  constructor(apiKey?: string) {
    this.resend = new Resend(apiKey || process.env.RESEND_API_KEY)
  }
  
  async sendOnboardingEmail(data: OnboardingEmailData): Promise<void> {
    const template = createOnboardingEmail(data)
    
    await this.resend.emails.send({
      from: 'noreply@paulyops.com',
      to: data.email,
      subject: template.subject,
      html: template.html,
      text: template.text
    })
  }
  
  async sendJobNotificationEmail(data: JobNotificationEmailData): Promise<void> {
    const template = createJobNotificationEmail(data)
    
    await this.resend.emails.send({
      from: 'noreply@paulyops.com',
      to: data.email,
      subject: template.subject,
      html: template.html,
      text: template.text
    })
  }
}

// Export default email service instance
export const emailService = new EmailService()
