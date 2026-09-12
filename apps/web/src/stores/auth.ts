import { defineStore } from 'pinia'
import router from '@/router'
import api from '@/lib/api'
import type { TokenPair, User } from '@/types/auth'

interface AuthState {
  accessToken: string | null
  refreshToken: string | null
  user: User | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    accessToken: localStorage.getItem('reqflow_access_token'),
    refreshToken: localStorage.getItem('reqflow_refresh_token'),
    user: null,
  }),

  getters: {
    isAuthenticated: state => Boolean(state.accessToken),
  },

  actions: {
    setTokens(tokens: TokenPair) {
      this.accessToken = tokens.access_token
      this.refreshToken = tokens.refresh_token
      localStorage.setItem('reqflow_access_token', tokens.access_token)
      localStorage.setItem('reqflow_refresh_token', tokens.refresh_token)
    },

    async register(payload: { email: string; password: string; full_name: string }) {
      const { data } = await api.post<TokenPair>('/auth/register', payload)
      this.setTokens(data)
      await this.fetchCurrentUser()
    },

    async login(payload: { email: string; password: string }) {
      const { data } = await api.post<TokenPair>('/auth/login', payload)
      this.setTokens(data)
      await this.fetchCurrentUser()
    },

    async refreshTokens() {
      if (!this.refreshToken) throw new Error('No refresh token available')
      const { data } = await api.post<TokenPair>('/auth/refresh', {
        refresh_token: this.refreshToken,
      })
      this.setTokens(data)
    },

    async fetchCurrentUser() {
      const { data } = await api.get<User>('/auth/me')
      this.user = data
    },

    logout() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null
      localStorage.removeItem('reqflow_access_token')
      localStorage.removeItem('reqflow_refresh_token')
      router.push({ name: 'login' })
    },
  },
})
