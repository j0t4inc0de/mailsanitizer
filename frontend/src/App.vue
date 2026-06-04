<template>
  <div class="relative min-h-screen flex flex-col">
    <Navbar />
    <main class="flex-1">
      <router-view v-slot="{ Component }">
        <transition name="view" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <footer class="relative z-10 border-t border-brand-border py-8 bg-black/20 backdrop-blur-sm">
      <div class="mx-auto max-w-7xl px-4 flex flex-col md:flex-row items-center justify-between gap-4">
        <p class="text-sm text-brand-muted order-2 md:order-1">
          © 2026 CleanMail by Samod — Un producto de
          <a
            href="https://wearesamod.com"
            target="_blank"
            rel="noopener noreferrer"
            class="text-brand-primary hover:text-brand-primary/80 transition-colors"
          >
            We Are Samod
          </a>
        </p>
        
        <!-- Enlaces legales -->
        <div class="flex flex-wrap justify-center gap-x-6 gap-y-2 text-sm text-brand-muted order-1 md:order-2">
          <router-link to="/terms" class="hover:text-brand-text transition-colors">Términos de Servicio</router-link>
          <router-link to="/privacy" class="hover:text-brand-text transition-colors">Política de Privacidad</router-link>
          <router-link to="/refunds" class="hover:text-brand-text transition-colors">Política de Reembolso</router-link>
          <a href="mailto:contacto@wearesamod.com" class="hover:text-brand-text transition-colors">Soporte</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'
import Navbar from './components/Navbar.vue'

const auth = useAuthStore()

onMounted(() => {
  if (auth.isAuthenticated) {
    auth.fetchUser()
  }
})
</script>
