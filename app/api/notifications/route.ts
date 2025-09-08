import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { getTokenFromRequest, verifyJwt } from '@/lib/auth'
import { NextRequest } from 'next/server'

// GET /api/notifications -> list for logged-in user
export async function GET(req: NextRequest) {
  const token = getTokenFromRequest(req)
  const payload = token && verifyJwt(token)
  if (!payload) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

  const notifications = await prisma.notification.findMany({ where: { userId: payload.sub }, orderBy: { createdAt: 'desc' } })
  return NextResponse.json({ notifications })
}