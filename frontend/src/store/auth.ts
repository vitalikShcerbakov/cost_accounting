import { defineStore, acceptHMRUpdate } from "pinia";
import api from 'src/services/api'

interface User {
  id: number
  name: string
  email?: string
  is_active?: boolean
}

export const useAuthStore = defineStore('auth', {
    state: () => {
        const token = localStorage.getItem('token')
        const userStr = localStorage.getItem('user')
        const user = userStr ? JSON.parse(userStr) as User : null
        
        return {
            token,
            user,
        }
    },
    actions: {
        async login(username:string, password:string){
            try {
            console.log('username:', username, 'username:', password)
            const params = new URLSearchParams({ username, password })
            const res = await api.post(`/auth/token`, params, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' }})
            this.token = res.data.access_token
            localStorage.setItem('token', this.token ? this.token : '')
            api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
            } catch(err) {
                console.log('error: ', err)
            }
        },
        async fetchUser() {
            const res = await api.get(`/auth/me`, {
                headers: {
                    Authorization: `Bearer ${this.token}`
                }
            })
            api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
            this.user = res.data.user
            // Сохраняем пользователя в localStorage
            localStorage.setItem('user', JSON.stringify(this.user))
        },
            async initAuth() {
      // Восстанавливаем состояние аутентификации при загрузке приложения
      console.log('Инициализация аутентификации, token:', this.token)
      if (this.token) {
        try {
          api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
          await this.fetchUser()
          console.log('Пользователь восстановлен:', this.user)
        } catch (error) {
          console.log('Ошибка восстановления аутентификации:', error)
          this.logout()
        }
      } else {
        console.log('Токен не найден')
      }
    },
        logout() {
            this.token = null
            this.user = null
            localStorage.removeItem('token')
            localStorage.removeItem('user')
            delete api.defaults.headers.common['Authorization']
        }, 
    }
});
if (import.meta.hot) { //  функция из модуля Pinia, которая включает замену горячих модулей (HMR) для хранилищ
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot));
}