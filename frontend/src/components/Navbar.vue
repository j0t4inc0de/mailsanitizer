<template>
  <nav
    class="fixed top-0 left-0 right-0 z-50 transition-all duration-300"
    :class="scrolled ? 'bg-brand-darker/80 backdrop-blur-xl border-b border-brand-border shadow-glass' : 'bg-transparent'"
  >
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 items-center justify-between">
        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-1 group">
          <span class="font-outfit text-xl font-bold text-brand-text group-hover:text-brand-primary transition-colors">
            CleanMail
          </span>
          <span class="text-sm text-brand-muted font-inter">by Samod</span>
        </router-link>

        <!-- Desktop nav -->
        <div class="hidden md:flex items-center gap-2">
          <router-link to="/" class="btn-ghost text-sm">Inicio</router-link>
          <router-link to="/pricing" class="btn-ghost text-sm">Precios</router-link>

          <template v-if="auth.isAuthenticated">
            <router-link to="/dashboard" class="btn-ghost text-sm">Dashboard</router-link>
            <CreditBalance :credits="auth.credits" />
            <button @click="handleLogout" class="btn-ghost text-sm text-red-400 hover:text-red-300">
              Salir
            </button>
          </template>

          <template v-else>
            <button @click="showAuthModal = true" class="btn-primary text-sm py-2 px-5">
              Comenzar gratis
            </button>
          </template>
        </div>

        <!-- Mobile hamburger -->
        <button
          @click="mobileOpen = !mobileOpen"
          class="md:hidden p-2 text-brand-muted hover:text-brand-text transition-colors"
          aria-label="Menú"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              v-if="!mobileOpen"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            />
            <path
              v-else
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile menu -->
    <transition name="fade">
      <div v-if="mobileOpen" class="md:hidden border-t border-brand-border bg-brand-darker/95 backdrop-blur-xl">
        <div class="px-4 py-4 space-y-2">
          <router-link to="/" class="block btn-ghost text-sm w-full text-left" @click="mobileOpen = false">
            Inicio
          </router-link>
          <router-link to="/pricing" class="block btn-ghost text-sm w-full text-left" @click="mobileOpen = false">
            Precios
          </router-link>

          <template v-if="auth.isAuthenticated">
            <router-link to="/dashboard" class="block btn-ghost text-sm w-full text-left" @click="mobileOpen = false">
              Dashboard
            </router-link>
            <div class="px-4 py-2">
              <CreditBalance :credits="auth.credits" />
            </div>
            <button @click="handleLogout" class="block btn-ghost text-sm w-full text-left text-red-400">
              Salir
            </button>
          </template>

          <template v-else>
            <button
              @click="showAuthModal = true; mobileOpen = false"
              class="btn-primary text-sm w-full mt-2"
            >
              Comenzar gratis
            </button>
          </template>
        </div>
      </div>
    </transition>

    <!-- Auth modal -->
    <transition name="fade">
      <div
        v-if="showAuthModal"
        class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm px-4"
        @click.self="showAuthModal = false"
      >
        <div class="glass-panel-solid p-8 w-full max-w-md animate-scale-in">
          <h2 class="font-outfit text-2xl font-bold text-brand-text mb-2">
            Accede a tu cuenta
          </h2>
          <p class="text-brand-muted text-sm mb-6">
            Ingresa tu correo y te enviaremos un enlace mágico para iniciar sesión.
          </p>

          <div v-if="!linkSent">
            <input
              v-model="authEmail"
              type="email"
              placeholder="tu@correo.com"
              class="glass-input mb-4"
              @keyup.enter="sendMagicLink"
            />
            <button
              @click="sendMagicLink"
              :disabled="auth.isLoading || !authEmail"
              class="btn-primary w-full"
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
            <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-brand-secondary/20 flex items-center justify-center">
              <svg class="w-8 h-8 text-brand-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <p class="text-brand-text font-medium mb-1">¡Revisa tu correo!</p>
            <p class="text-brand-muted text-sm">
              Enviamos un enlace mágico a <strong class="text-brand-text">{{ authEmail }}</strong>
            </p>
          </div>

          <p v-if="auth.error" class="mt-3 text-red-400 text-sm text-center">{{ auth.error }}</p>

          <button
            @click="showAuthModal = false"
            class="mt-4 text-brand-muted hover:text-brand-text text-sm transition-colors w-full text-center"
          >
            Cerrar
          </button>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import CreditBalance from './CreditBalance.vue'

const auth = useAuthStore()
const router = useRouter()

const scrolled = ref(false)
const mobileOpen = ref(false)
const showAuthModal = ref(false)
const authEmail = ref('')
const linkSent = ref(false)

function onScroll() {
  scrolled.value = window.scrollY > 20
}

onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

async function sendMagicLink() {
  if (!authEmail.value) return
  try {
    await auth.requestMagicLink(authEmail.value)
    linkSent.value = true
  } catch {
    // error is set in store
  }
}

function handleLogout() {
  auth.logout()
  mobileOpen.value = false
  router.push('/')
}
</script>
