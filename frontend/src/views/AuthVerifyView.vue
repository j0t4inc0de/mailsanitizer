<template>
  <div class="min-h-screen flex items-center justify-center px-4 pt-20">
    <!-- Background glow -->
    <div class="glow-orb-primary w-72 h-72 top-20 left-1/4 fixed animate-float" />
    <div class="glow-orb-accent w-64 h-64 bottom-20 right-1/4 fixed animate-float-delayed" />

    <div class="glass-panel-solid p-8 sm:p-12 max-w-md w-full text-center animate-scale-in">
      <!-- Loading state -->
      <template v-if="isVerifying">
        <div class="w-16 h-16 mx-auto mb-6 rounded-full bg-brand-primary/20 flex items-center justify-center">
          <svg class="w-8 h-8 text-brand-primary animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        </div>
        <h2 class="font-outfit text-2xl font-bold text-brand-text mb-2">Verificando tu enlace...</h2>
        <p class="text-brand-muted text-sm">Un momento, estamos validando tu acceso.</p>
      </template>

      <!-- Success -->
      <template v-else-if="success">
        <div class="w-16 h-16 mx-auto mb-6 rounded-full bg-brand-secondary/20 flex items-center justify-center shadow-neon-secondary">
          <svg class="w-8 h-8 text-brand-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h2 class="font-outfit text-2xl font-bold text-brand-text mb-2">¡Bienvenido!</h2>
        <p class="text-brand-muted text-sm mb-6">Tu sesión ha sido verificada correctamente.</p>
        <router-link to="/dashboard" class="btn-primary w-full">
          Ir al Dashboard
        </router-link>
      </template>

      <!-- Error -->
      <template v-else>
        <div class="w-16 h-16 mx-auto mb-6 rounded-full bg-red-500/20 flex items-center justify-center shadow-neon-red">
          <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        <h2 class="font-outfit text-2xl font-bold text-brand-text mb-2">Enlace inválido</h2>
        <p class="text-brand-muted text-sm mb-6">
          {{ errorMessage || 'Este enlace ha expirado o ya fue utilizado. Solicita uno nuevo.' }}
        </p>
        <router-link to="/" class="btn-primary w-full">
          Volver al inicio
        </router-link>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const isVerifying = ref(true)
const success = ref(false)
const errorMessage = ref('')

onMounted(async () => {
  const token = route.query.token
  if (!token) {
    isVerifying.value = false
    errorMessage.value = 'No se encontró un token de verificación en el enlace.'
    return
  }

  try {
    await auth.verifyToken(token)
    success.value = true
    // Auto-redirect after 2 seconds
    setTimeout(() => router.push('/dashboard'), 2000)
  } catch (err) {
    errorMessage.value = auth.error || 'Token inválido o expirado.'
  } finally {
    isVerifying.value = false
  }
})
</script>
