import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/client'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('cleanmail_token') || '')
  const isLoading = ref(false)
  const error = ref('')

  const isAuthenticated = computed(() => !!token.value)
  const credits = computed(() => user.value?.credits ?? 0)

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('cleanmail_token', newToken)
  }

  function clearAuth() {
    token.value = ''
    user.value = null
    localStorage.removeItem('cleanmail_token')
  }

  async function requestMagicLink(email) {
    isLoading.value = true
    error.value = ''
    try {
      const { data } = await api.post('/auth/magic-link/', { email })
      return data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al enviar el enlace mágico'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function verifyToken(magicToken) {
    isLoading.value = true
    error.value = ''
    try {
      const { data } = await api.post('/auth/verify/', { token: magicToken })
      setToken(data.token)
      user.value = data.usuario || null
      return data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Token inválido o expirado'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchUser() {
    if (!token.value) return
    isLoading.value = true
    try {
      const { data } = await api.get('/auth/me/')
      user.value = data
    } catch (err) {
      if (err.response?.status === 401) {
        clearAuth()
      }
    } finally {
      isLoading.value = false
    }
  }

  function logout() {
    clearAuth()
  }

  return {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
    credits,
    setToken,
    clearAuth,
    requestMagicLink,
    verifyToken,
    fetchUser,
    logout,
  }
})
