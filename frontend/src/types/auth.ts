export interface User {
  id: number
  name: string
  email?: string
  is_active?: boolean
}

export interface Token {
  access_token: string
  token_type: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  name: string
  email?: string
  password: string
}

export interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
} 