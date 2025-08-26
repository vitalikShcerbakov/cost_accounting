import axios from 'axios'
import type { LoginRequest, RegisterRequest, Token, User } from '../types/auth'

const API_BASE_URL = process.env.DEV 
    ? 'http://localhost:8000' // для разработки
    : ''                 // для production

const authApi = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Добавляем перехватчик для добавления токена к запросам
authApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(new Error(error.message || 'Request error'))
  }
)

// Добавляем перехватчик для обработки ошибок авторизации
authApi.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Токен истек или недействителен
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(new Error(error.message || 'Network error'))
  }
)

export const authService = {
  // Авторизация
  login: async (credentials: LoginRequest): Promise<Token> => {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)
    
    const response = await authApi.post<Token>('/auth/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    return response.data
  },

  // Регистрация
  register: async (userData: RegisterRequest): Promise<User> => {
    const response = await authApi.post<User>('/auth/register', userData)
    return response.data
  },

  // Получение информации о текущем пользователе
  getCurrentUser: async (): Promise<User> => {
    const response = await authApi.get<{ user: User }>('/auth/me')
    return response.data.user
  },

  // Выход
  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },

  // Сохранение токена и пользователя
  saveAuthData: (token: string, user: User) => {
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(user))
  },

  // Получение сохраненного токена
  getToken: (): string | null => {
    return localStorage.getItem('token')
  },

  // Получение сохраненного пользователя
  getStoredUser: (): User | null => {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  },

  // Проверка аутентификации
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('token')
  }
}

export default authApi 