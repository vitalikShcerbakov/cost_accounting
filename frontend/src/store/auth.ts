import { defineStore } from "pinia";
import api from 'src/services/api'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token'),
        user: null,
    }),
    actions: {
        async login(username:string, password:string){
            const res = await api.post(`/auth/token`, new URLSearchParams({username, password}))
            this.token = res.data.access_token
            localStorage.setItem('token', this.token ? this.token : '')
            api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
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
})