import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import router from '@/router'
import api from '@/lib/api'
import type { TokenPair, User } from '@/types/auth'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(localStorage.getItem('reqflow_access_token'))
  const refreshToken = ref<string | null>(localStorage.getItem('reqflow_refresh_token'))
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => Boolean(accessToken.value))

  function setTokens(tokens: TokenPair) {
    accessToken.value = tokens.access_token
    refreshToken.value = tokens.refresh_token
    localStorage.setItem('reqflow_access_token', tokens.access_token)
    localStorage.setItem('reqflow_refresh_token', tokens.refresh_token)
  }

  async function register(payload: { email: string; password: string; full_name: string }) {
    const { data } = await api.post<TokenPair>('/auth/register', payload)
    setTokens(data)
    await fetchCurrentUser()
  }

  async function login(payload: { email: string; password: string }) {
    const { data } = await api.post<TokenPair>('/auth/login', payload)
    setTokens(data)
    await fetchCurrentUser()
  }

  async function refreshTokens() {
    if (!refreshToken.value) throw new Error('No refresh token available')
    const { data } = await api.post<TokenPair>('/auth/refresh', {
      refresh_token: refreshToken.value,
    })
    setTokens(data)
  }

  async function fetchCurrentUser() {
    const { data } = await api.get<User>('/auth/me')
    user.value = data
  }

  function logout() {
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    localStorage.removeItem('reqflow_access_token')
    localStorage.removeItem('reqflow_refresh_token')
    router.push({ name: 'login' })
  }

  return {
    accessToken,
    refreshToken,
    user,
    isAuthenticated,
    setTokens,
    register,
    login,
    refreshTokens,
    fetchCurrentUser,
    logout,
  }
})
