import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { comparePassword, signJwt } from '@/lib/auth'
import { loginSchema } from '@/lib/validation'

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const parsed = loginSchema.safeParse(body)
    if (!parsed.success) {
      return NextResponse.json({ error: 'Invalid input', details: parsed.error.flatten() }, { status: 400 })
    }

    const { email, password } = parsed.data
    const user = await prisma.user.findUnique({ where: { email } })
    if (!user) return NextResponse.json({ error: 'Invalid credentials' }, { status: 401 })

    const ok = await comparePassword(password, user.passwordHash)
    if (!ok) return NextResponse.json({ error: 'Invalid credentials' }, { status: 401 })

    const token = signJwt({ sub: user.id, role: user.role })
    const res = NextResponse.json({ user: { id: user.id, name: user.name, email: user.email, role: user.role } }, { status: 200 })
    res.cookies.set('token', token, { httpOnly: true, sameSite: 'lax', secure: process.env.NODE_ENV === 'production', maxAge: 60 * 60 * 24 * 7, path: '/' })
    return res
  } catch (e) {
    return NextResponse.json({ error: 'Server error' }, { status: 500 })
  }
}