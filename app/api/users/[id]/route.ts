import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { getTokenFromRequest, verifyJwt } from '@/lib/auth'
import { userUpdateSchema } from '@/lib/validation'
import { NextRequest } from 'next/server'

export async function GET(_req: NextRequest, { params }: { params: { id: string } }) {
  const user = await prisma.user.findUnique({ where: { id: params.id }, select: { id: true, name: true, email: true, avatarUrl: true, role: true, createdAt: true } })
  if (!user) return NextResponse.json({ error: 'Not found' }, { status: 404 })
  return NextResponse.json({ user })
}

export async function PUT(req: NextRequest, { params }: { params: { id: string } }) {
  const token = getTokenFromRequest(req)
  const payload = token && verifyJwt(token)
  if (!payload) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  if (payload.sub !== params.id && payload.role !== 'ADMIN') return NextResponse.json({ error: 'Forbidden' }, { status: 403 })

  const body = await req.json()
  const parsed = userUpdateSchema.safeParse(body)
  if (!parsed.success) return NextResponse.json({ error: 'Invalid input', details: parsed.error.flatten() }, { status: 400 })

  const user = await prisma.user.update({ where: { id: params.id }, data: parsed.data, select: { id: true, name: true, email: true, avatarUrl: true, role: true } })
  return NextResponse.json({ user })
}

export async function DELETE(req: NextRequest, { params }: { params: { id: string } }) {
  const token = getTokenFromRequest(req)
  const payload = token && verifyJwt(token)
  if (!payload) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  if (payload.sub !== params.id && payload.role !== 'ADMIN') return NextResponse.json({ error: 'Forbidden' }, { status: 403 })

  await prisma.user.delete({ where: { id: params.id } })
  return NextResponse.json({ success: true })
}