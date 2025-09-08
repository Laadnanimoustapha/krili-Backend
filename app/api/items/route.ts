import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { getTokenFromRequest, verifyJwt } from '@/lib/auth'
import { itemCreateSchema } from '@/lib/validation'
import { NextRequest } from 'next/server'

// GET /api/items -> list all items (public)
export async function GET() {
  const items = await prisma.item.findMany({
    orderBy: { createdAt: 'desc' },
    include: { user: { select: { id: true, name: true, avatarUrl: true } } }
  })
  return NextResponse.json({ items })
}

// POST /api/items -> create (auth required)
export async function POST(req: NextRequest) {
  const token = getTokenFromRequest(req)
  const payload = token && verifyJwt(token)
  if (!payload) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

  const body = await req.json()
  const parsed = itemCreateSchema.safeParse(body)
  if (!parsed.success) return NextResponse.json({ error: 'Invalid input', details: parsed.error.flatten() }, { status: 400 })

  const { title, description, imageUrl } = parsed.data
  const item = await prisma.item.create({ data: { title, description, imageUrl, userId: payload.sub } })
  return NextResponse.json({ item }, { status: 201 })
}