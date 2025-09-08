export function getBaseUrl() {
  const envUrl = process.env.NEXT_PUBLIC_SITE_URL || process.env.SITE_URL
  if (envUrl) return envUrl.replace(/\/$/, '')
  // Fallback to Vercel URL
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`
  // Local dev default
  return 'http://localhost:3000'
}export function getBaseUrl() {
  const envUrl = process.env.NEXT_PUBLIC_SITE_URL || process.env.SITE_URL
  if (envUrl) return envUrl.replace(/\/$/, '')
  // Fallback to Vercel URL
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`
  // Local dev default
  return 'http://localhost:3000'
}export function getBaseUrl() {
  const envUrl = process.env.NEXT_PUBLIC_SITE_URL || process.env.SITE_URL
  if (envUrl) return envUrl.replace(/\/$/, '')
  // Fallback to Vercel URL
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`
  // Local dev default
  return 'http://localhost:3000'
}