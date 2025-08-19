import { logger } from './logger'

export interface NotificationPayload {
  text: string
  attachments?: Array<{
    color: string
    fields: Array<{
      title: string
      value: string
      short?: boolean
    }>
  }>
}

export async function sendSlackNotification(payload: NotificationPayload): Promise<boolean> {
  const webhookUrl = process.env.DOCTOR_SLACK_WEBHOOK_URL
  
  if (!webhookUrl) {
    logger.debug('No Slack webhook URL configured, skipping notification')
    return false
  }

  try {
    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })

    if (response.ok) {
      logger.info({ webhookUrl }, 'Slack notification sent successfully')
      return true
    } else {
      logger.error({ 
        webhookUrl, 
        status: response.status,
        statusText: response.statusText 
      }, 'Failed to send Slack notification')
      return false
    }
  } catch (error: any) {
    logger.error({ 
      webhookUrl, 
      error: error.message 
    }, 'Error sending Slack notification')
    return false
  }
}

export async function sendDiscordNotification(payload: NotificationPayload): Promise<boolean> {
  const webhookUrl = process.env.DOCTOR_DISCORD_WEBHOOK_URL
  
  if (!webhookUrl) {
    logger.debug('No Discord webhook URL configured, skipping notification')
    return false
  }

  try {
    // Convert Slack format to Discord format
    const discordPayload = {
      content: payload.text,
      embeds: payload.attachments?.map(attachment => ({
        color: parseInt(attachment.color.replace('#', ''), 16),
        fields: attachment.fields
      })) || []
    }

    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(discordPayload),
    })

    if (response.ok) {
      logger.info({ webhookUrl }, 'Discord notification sent successfully')
      return true
    } else {
      logger.error({ 
        webhookUrl, 
        status: response.status,
        statusText: response.statusText 
      }, 'Failed to send Discord notification')
      return false
    }
  } catch (error: any) {
    logger.error({ 
      webhookUrl, 
      error: error.message 
    }, 'Error sending Discord notification')
    return false
  }
}

export async function sendNotifications(payload: NotificationPayload): Promise<void> {
  await Promise.all([
    sendSlackNotification(payload),
    sendDiscordNotification(payload)
  ])
}
