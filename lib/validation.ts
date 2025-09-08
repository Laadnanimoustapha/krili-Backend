import { z } from 'zod'

export const signupSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  password: z.string().min(8).max(100)
})

export const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(100)
})

export const userUpdateSchema = z.object({
  name: z.string().min(1).max(100).optional(),
  avatarUrl: z.string().url().optional()
})

export const itemCreateSchema = z.object({
  title: z.string().min(1).max(120),
  description: z.string().min(1).max(2000),
  imageUrl: z.string().url().optional()
})

export const itemUpdateSchema = itemCreateSchema.partial()

export const notificationCreateSchema = z.object({
  userId: z.string().cuid(),
  type: z.string().min(1).max(50),
  message: z.string().min(1).max(500)
})