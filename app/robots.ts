import type { MetadataRoute } from 'next'
import { getBaseUrl } from '@/lib/site'

export default function robots(): MetadataRoute.Robots {
  const baseUrl = getBaseUrl()
  return {
    rules: [
      {
        userAgent: '*',
        allow: ['/'],
        disallow: ['/admin/', '/api/', '/dashboard/', '/_next/', '/private/'],
      },
      { userAgent: 'Googlebot', allow: ['/'] },
      { userAgent: 'Bingbot', allow: ['/'] },
      { userAgent: 'facebookexternalhit', allow: ['/'] },
      { userAgent: 'Twitterbot', allow: ['/'] },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
  }
}import type { MetadataRoute } from 'next'
import { getBaseUrl } from '@/lib/site'

export default function robots(): MetadataRoute.Robots {
  const baseUrl = getBaseUrl()
  return {
    rules: [
      {
        userAgent: '*',
        allow: ['/'],
        disallow: ['/admin/', '/api/', '/dashboard/', '/_next/', '/private/'],
      },
      { userAgent: 'Googlebot', allow: ['/'] },
      { userAgent: 'Bingbot', allow: ['/'] },
      { userAgent: 'facebookexternalhit', allow: ['/'] },
      { userAgent: 'Twitterbot', allow: ['/'] },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
  }
}import type { MetadataRoute } from 'next'
import { getBaseUrl } from '@/lib/site'

export default function robots(): MetadataRoute.Robots {
  const baseUrl = getBaseUrl()
  return {
    rules: [
      {
        userAgent: '*',
        allow: ['/'],
        disallow: ['/admin/', '/api/', '/dashboard/', '/_next/', '/private/'],
      },
      { userAgent: 'Googlebot', allow: ['/'] },
      { userAgent: 'Bingbot', allow: ['/'] },
      { userAgent: 'facebookexternalhit', allow: ['/'] },
      { userAgent: 'Twitterbot', allow: ['/'] },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
  }
}import type { MetadataRoute } from 'next'
import { getBaseUrl } from '@/lib/site'

export default function robots(): MetadataRoute.Robots {
  const baseUrl = getBaseUrl()
  return {
    rules: [
      {
        userAgent: '*',
        allow: ['/'],
        disallow: ['/admin/', '/api/', '/dashboard/', '/_next/', '/private/'],
      },
      { userAgent: 'Googlebot', allow: ['/'] },
      { userAgent: 'Bingbot', allow: ['/'] },
      { userAgent: 'facebookexternalhit', allow: ['/'] },
      { userAgent: 'Twitterbot', allow: ['/'] },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
  }
}