export interface RetryOptions {
  retries?: number
  backoffMs?: number
  maxBackoffMs?: number
  onRetry?: (attempt: number, error: Error) => void
}

export async function runWithRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const {
    retries = 2,
    backoffMs = 500,
    maxBackoffMs = 5000,
    onRetry = () => {},
  } = options

  let lastError: Error

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error as Error
      
      if (attempt === retries) {
        throw lastError
      }

      onRetry(attempt + 1, lastError)
      
      // Exponential backoff with jitter
      const delay = Math.min(
        backoffMs * Math.pow(2, attempt) + Math.random() * 100,
        maxBackoffMs
      )
      
      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }

  throw lastError!
}
