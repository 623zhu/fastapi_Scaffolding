import { request } from '@/api/client'
import type { RegisterUserPayload, User } from '@/types/user'

export function registerUser(payload: RegisterUserPayload): Promise<User> {
  return request<User>('/api/v1/users', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
