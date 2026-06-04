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
    <footer class="relative z-10 border-t border-brand-border py-6">
      <div class="mx-auto max-w-7xl px-4 text-center">
        <p class="text-sm text-brand-muted">
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
