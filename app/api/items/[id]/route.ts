import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { getTokenFromRequest, verifyJwt } from '@/lib/auth'
import { itemUpdateSchema } from '@/lib/validation'
import { NextRequest } from 'next/server'

export async function GET(_req: NextRequest, { params }: { params: { id: string } }) {
  const item = await prisma.item.findUnique({ where: { id: params.id }, include: { user: { select: { id: true, name: true, avatarUrl: true } } } })
  if (!item) return NextResponse.json({ error: 'Not found' }, { status: 404 })
  return NextResponse.json({ item })
}

export async function PUT(req: NextRequest, { params }: { params: { id: string } }) {
  const token = getTokenFromRequest(req)
  const payload = token && verifyJwt(token)
  if (!payload) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

  const existing = await prisma.item.findUnique({ where: { id: params.id } })
  if (!existing) return NextResponse.json({ error: 'Not found' }, { status: 404 })
  if (existing.userId !== payload.sub && payload.role !== 'ADMIN') return NextResponse.json({ error: 'Forbidden' }, { status: 403 })

  const body = await req.json()
  const parsed = itemUpdateSchema.safeParse(body)
  if (!parsed.success) return NextResponse.json({ error: 'Invalid input', details: parsed.error.flatten() }, { status: 400 })

  const item = await prisma.item.update({ where: { id: params.id }, data: parsed.data })
  return NextResponse.json({ item })
}

export async function DELETE(req: NextRequest, { params }: { params: { id: string } }) {
  const token = getTokenFromRequest(req)
  const payload = token && verifyJwt(token)
  if (!payload) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

  const existing = await prisma.item.findUnique({ where: { id: params.id } })
  if (!existing) return NextResponse.json({ error: 'Not found' }, { status: 404 })
  if (existing.userId !== payload.sub && payload.role !== 'ADMIN') return NextResponse.json({ error: 'Forbidden' }, { status: 403 })

  await prisma.item.delete({ where: { id: params.id } })
  return NextResponse.json({ success: true })
}