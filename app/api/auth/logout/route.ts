import { NextResponse } from 'next/server'

export async function POST() {
  const res = NextResponse.json({ success: true })
  // Overwrite the cookie to expire it
  res.cookies.set('token', '', { httpOnly: true, sameSite: 'lax', secure: process.env.NODE_ENV === 'production', maxAge: 0, path: '/' })
  return res
}