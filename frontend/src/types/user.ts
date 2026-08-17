export interface RegisterUserPayload {
  username: string
  email: string
  password: string
}

export interface User {
  id: number
  username: string
  email: string
  is_active: boolean
  created_at: string
  updated_at: string
}
