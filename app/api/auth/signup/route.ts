import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { hashPassword, signJwt } from '@/lib/auth'
import { signupSchema } from '@/lib/validation'

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const parsed = signupSchema.safeParse(body)
    if (!parsed.success) {
      return NextResponse.json({ error: 'Invalid input', details: parsed.error.flatten() }, { status: 400 })
    }

    const { name, email, password } = parsed.data

    const existing = await prisma.user.findUnique({ where: { email } })
    if (existing) return NextResponse.json({ error: 'Email already in use' }, { status: 409 })

    const passwordHash = await hashPassword(password)
    const user = await prisma.user.create({ data: { name, email, passwordHash } })

    const token = signJwt({ sub: user.id, role: user.role })
    const res = NextResponse.json({ user: { id: user.id, name: user.name, email: user.email, role: user.role } }, { status: 201 })
    res.cookies.set('token', token, { httpOnly: true, sameSite: 'lax', secure: process.env.NODE_ENV === 'production', maxAge: 60 * 60 * 24 * 7, path: '/' })
    return res
  } catch (e) {
    return NextResponse.json({ error: 'Server error' }, { status: 500 })
  }
}