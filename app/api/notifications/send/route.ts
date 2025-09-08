import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { getTokenFromRequest, verifyJwt } from '@/lib/auth'
import { notificationCreateSchema } from '@/lib/validation'

export async function POST(request: Request) {
  const token = request.headers.get('authorization')?.startsWith('Bearer ')
    ? request.headers.get('authorization')!.slice('Bearer '.length)
    : null
  const payload = token && verifyJwt(token)
  if (!payload || payload.role !== 'ADMIN') return NextResponse.json({ error: 'Forbidden' }, { status: 403 })

  const body = await request.json()
  const parsed = notificationCreateSchema.safeParse(body)
  if (!parsed.success) return NextResponse.json({ error: 'Invalid input', details: parsed.error.flatten() }, { status: 400 })

  const notif = await prisma.notification.create({ data: parsed.data })
  return NextResponse.json({ notification: notif }, { status: 201 })
}