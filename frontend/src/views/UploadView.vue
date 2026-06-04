<template>
  <div class="relative min-h-screen pt-24 pb-16 px-4">
    <!-- Background glow orbs -->
    <div class="glow-orb-primary w-80 h-80 -top-40 left-10 fixed animate-float" />
    <div class="glow-orb-accent w-64 h-64 bottom-20 -right-32 fixed animate-float-delayed" />

    <div class="mx-auto max-w-2xl">
      <!-- Header -->
      <div class="text-center mb-10">
        <h1 class="font-outfit text-3xl sm:text-4xl font-bold text-brand-text mb-2">
          Sube tu lista de correos
        </h1>
        <p class="text-brand-muted text-lg">
          Arrastra tu archivo CSV y valida todos los correos en segundos.
        </p>
      </div>

      <!-- File uploader -->
      <div class="mb-8">
        <FileUploader @file-selected="onFileSelected" @file-cleared="onFileCleared" />
      </div>

      <!-- File info + credit cost -->
      <transition name="fade">
        <div v-if="selectedFile" class="space-y-4 animate-slide-up">
          <!-- File stats -->
          <div class="glass-panel p-6">
            <div class="grid grid-cols-2 gap-4 text-center">
              <div>
                <p class="text-brand-muted text-sm">Tamaño del archivo</p>
                <p class="font-outfit text-xl font-bold text-brand-text">{{ formatSize(selectedFile.size) }}</p>
              </div>
              <div>
                <p class="text-brand-muted text-sm">Correos estimados</p>
                <p class="font-outfit text-xl font-bold text-brand-text">~{{ estimatedEmails.toLocaleString('es-CL') }}</p>
              </div>
            </div>
          </div>

          <!-- Credit cost -->
          <div class="glass-panel p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-brand-muted text-sm">Costo de esta validación</p>
                <p class="font-outfit text-2xl font-bold text-brand-text">
                  {{ estimatedEmails.toLocaleString('es-CL') }} créditos
                </p>
              </div>
              <div class="text-right">
                <p class="text-brand-muted text-sm">Tu balance</p>
                <p class="font-outfit text-2xl font-bold" :class="auth.credits >= estimatedEmails ? 'text-brand-secondary' : 'text-red-400'">
                  {{ auth.credits.toLocaleString('es-CL') }}
                </p>
              </div>
            </div>

            <!-- Free first task -->
            <div
              v-if="isFirstTaskFree"
              class="mt-4 rounded-xl bg-brand-secondary/10 border border-brand-secondary/20 p-4 flex items-center gap-3"
            >
              <span class="text-2xl">📊</span>
              <div>
                <p class="text-brand-secondary font-semibold text-sm">Tus validaciones usarán créditos</p>
                <p class="text-brand-muted text-xs">Se descontará 1 crédito por cada correo en tu archivo.</p>
              </div>
            </div>

            <!-- Insufficient credits warning -->
            <div
              v-else-if="auth.credits < estimatedEmails"
              class="mt-4 rounded-xl bg-red-500/10 border border-red-500/20 p-4"
            >
              <p class="text-red-400 text-sm font-medium mb-1">Créditos insuficientes</p>
              <p class="text-brand-muted text-xs mb-3">
                Necesitas {{ (estimatedEmails - auth.credits).toLocaleString('es-CL') }} créditos adicionales.
              </p>
              <router-link to="/pricing" class="text-brand-primary text-sm font-medium hover:underline">
                Comprar créditos →
              </router-link>
            </div>
          </div>

          <!-- Submit button -->
          <button
            @click="startValidation"
            :disabled="isUploading || (!isFirstTaskFree && auth.credits < estimatedEmails)"
            class="btn-primary w-full py-4 text-lg"
          >
            <svg v-if="isUploading" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            <span>{{ isUploading ? 'Subiendo archivo...' : 'Iniciar validación' }}</span>
          </button>

          <!-- Error -->
          <p v-if="tasksStore.error" class="text-red-400 text-sm text-center">
            {{ tasksStore.error }}
          </p>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useTasksStore } from '../stores/tasks'
import FileUploader from '../components/FileUploader.vue'

const router = useRouter()
const auth = useAuthStore()
const tasksStore = useTasksStore()

const selectedFile = ref(null)
const isUploading = ref(false)

// Rough estimate: ~40 bytes per email line in a CSV
const estimatedEmails = computed(() => {
  if (!selectedFile.value) return 0
  return Math.max(1, Math.round(selectedFile.value.size / 40))
})

const isFirstTaskFree = computed(() => {
  return false
})

function onFileSelected(file) {
  selectedFile.value = file
}

function onFileCleared() {
  selectedFile.value = null
}

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1048576).toFixed(2) + ' MB'
}

async function startValidation() {
  if (!selectedFile.value) return
  isUploading.value = true
  try {
    const task = await tasksStore.uploadCSV(selectedFile.value)
    router.push(`/tasks/${task.id}`)
  } catch {
    // error is set in store
  } finally {
    isUploading.value = false
  }
}
</script>
