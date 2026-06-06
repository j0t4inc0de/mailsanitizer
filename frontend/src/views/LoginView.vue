<template>
  <div class="min-h-screen flex items-center justify-center px-4 pt-20">
    <!-- Background glow -->
    <div class="glow-orb-primary w-72 h-72 top-20 left-1/4 fixed animate-float" />
    <div class="glow-orb-accent w-64 h-64 bottom-20 right-1/4 fixed animate-float-delayed" />

    <div class="glass-panel-solid p-8 sm:p-12 max-w-md w-full text-center animate-scale-in">
      <h2 class="font-outfit text-3xl font-bold text-brand-text mb-2">
        Acceder a tu cuenta
      </h2>
      <p class="text-brand-muted text-sm mb-6">
        Ingresa tu correo y te enviaremos un enlace mágico para iniciar sesión.
      </p>

      <div v-if="!linkSent">
        <input
          v-model="email"
          type="email"
          placeholder="tu@correo.com"
          class="glass-input mb-4"
          @keyup.enter="handleSendMagicLink"
        />
        <button
          @click="handleSendMagicLink"
          :disabled="auth.isLoading || !email"
          class="btn-primary w-full flex items-center justify-center gap-2"
        >
          <svg v-if="auth.isLoading" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <span v-if="!auth.isLoading">Enviar enlace mágico</span>
          <span v-else>Enviando...</span>
        </button>
      </div>

      <div v-else class="text-center py-4">
        <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-brand-secondary/20 flex items-center justify-center shadow-neon-secondary">
          <svg class="w-8 h-8 text-brand-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>
        <p class="text-brand-text font-medium mb-1">¡Revisa tu correo!</p>
        <p class="text-brand-muted text-sm mb-6">
          Enviamos un enlace mágico a <strong class="text-brand-text">{{ email }}</strong>
        </p>
        <button @click="linkSent = false" class="btn-secondary w-full">
          Volver a intentar
        </button>
      </div>

      <p v-if="auth.error" class="mt-3 text-red-400 text-sm text-center">{{ auth.error }}</p>

      <router-link
        to="/"
        class="block mt-6 text-brand-muted hover:text-brand-text text-sm transition-colors text-center"
      >
        Volver al inicio
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { toast } from 'vue-sonner'

const auth = useAuthStore()
const email = ref('')
const linkSent = ref(false)

const handleSendMagicLink = async () => {
  if (!email.value) return
  try {
    await auth.requestMagicLink(email.value)
    linkSent.value = true
    toast.success('¡Enlace enviado! Revisa tu bandeja de entrada.')
  } catch (err) {
    toast.error(auth.error || 'Error al enviar el enlace mágico.')
  }
}
</script>
