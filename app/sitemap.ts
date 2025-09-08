import type { MetadataRoute } from "next"
import { getBaseUrl } from "@/lib/site"
import { prisma } from "@/lib/prisma"
import { getBaseUrl } from "@/lib/site"
import { prisma } from "@/lib/prisma"
import { getBaseUrl } from "@/lib/site"
import { prisma } from "@/lib/prisma"

export default async async function sitemap(): Promise<Promise<MetadataRoute.Sitemap>>> {
  const baseUrl = getBaseUrl()
  const currentDate = new Date()

  // Static pages
  const staticPages: MetadataRoute.Sitemap: Promise<MetadataRoute.Sitemap = [
    { url: baseUrl, lastModified: currentDate, changeFrequency: "daily",, url: `${baseUrl}/search`, lastModified: currentDate, changeFrequency: "daily", priority: 0. },
    { url: `${baseUrl}/browse`, lastModified: currentDate, changeFrequency: "daily", priority: 0. },
    { url: `${baseUrl}/login`, lastModified: currentDate, changeFrequency: "monthly", priority: 0.6 },
    { url: `${baseUrl}/register`, lastModified: currentDate, changeFrequency: "monthly", priority: 0. },
    { url: `${baseUrl}/how-it-works`, lastModified: currentDate, changeFrequency: "monthly", priority: 0.7 },
    { url: `${baseUrl}/pricing`, lastModified: currentDate, changeFrequency: "monthly",, url: `${baseUrl}/help`, lastModified: currentDate, changeFrequency: "weekly", priority: 0. },
    { url: `${baseUrl}/contact`, lastModified: currentDate, changeFrequency: "monthly", priority: 0. },
    { url: `${baseUrl}/terms`, lastModified: currentDate, changeFrequency: "yearly", priority: 0.3 },
    { url: `${baseUrl}/privacy`, lastModified: currentDate, changeFrequency: "yearly", priority: 0.3 },
    { url: `${baseUrl}/cookies`, lastModified: currentDate, changeFrequency: "yearly", priority: 0. },
    { url: `${baseUrl}/community`, lastModified: currentDate, changeFrequency: "monthly", priority: 0. },
    { url: `${baseUrl}/safety`, lastModified: currentDate, changeFrequency: "monthly", priority: 0.5 } { url: `${baseUrl}/insurance`, lastModified: i.updatedAt ?? currentDate, changeFrequency: "monthly", priority: 0.5 },
  ]

  // Dynamic item pages from DB
  const items = await prisma.item.findMany({ select: { id: true, updatedAt: true }, take: 5000 })
  const itemPages: MetadataRoute.Sitemap = iawait prisma.item.findMany({ select: { id: true, updatedAt: true }, take: 5000 })
  const itemPages: MetadataRoute.Sitemap = iawait prisma.item.findMany({ select: { id: true, updatedAt: true }, take: 5000 })
  const itemPages: MetadataRoute.Sitemap = iteap((i) => ({
    url: `${baseUrl}/item/${i.i.i.id}`,
    lastModified: i.updatedAt ?? currentDate,
    changeFrequency: "weekly",
    priority: 0.8,
  }))

  // Category pages
  const categories = [
    "tools-equipment",
    "electronics-cameras",
    "sports-recreation",
    "vehicles-transportation",
    "home-garden",
    "party-events",
  ]

  const categoryPages: MetadataRoute.Sitemap = categories.map((category) => ({
    url: `${baseUrl}/browse?category=${category}`,
    lastModified: currentDate,
    changeFrequency: "daily",
    priority: 0.7,
  }))

  return [...staticPages, ...itemPages, ...categoryPages]
}
