import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { getTokenFromRequest, verifyJwt } from '@/lib/auth'
import { NextRequest } from 'next/server'

export async function GET(req: NextRequest) {
  const token = getTokenFromRequest(req)
  if (!token) return NextResponse.json({ user: null }, { status: 200 })
  const payload = verifyJwt(token)
  if (!payload) return NextResponse.json({ user: null }, { status: 200 })

  const user = await prisma.user.findUnique({ where: { id: payload.sub }, select: { id: true, name: true, email: true, role: true, avatarUrl: true } })
  return NextResponse.json({ user }, { status: 200 })
}