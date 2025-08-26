import { defineStore, acceptHMRUpdate } from "pinia";
import api from 'src/services/api'

interface User {
  id: number
  name: string
  email?: string
  is_active?: boolean
}

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token'),
        user: null as User | null,
    }),
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
        },
        logout() {
            this.token = null
            this.user = null
            localStorage.removeItem('token')
            delete api.defaults.headers.common['Authorization']
        }, 
    }
});
if (import.meta.hot) { //  функция из модуля Pinia, которая включает замену горячих модулей (HMR) для хранилищ
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot));
}