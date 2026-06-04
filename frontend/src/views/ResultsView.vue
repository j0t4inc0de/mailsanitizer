<template>
  <div class="relative min-h-screen pt-24 pb-16 px-4">
    <!-- Background glow orbs -->
    <div class="glow-orb-primary w-80 h-80 -top-40 -right-40 fixed animate-float" />
    <div class="glow-orb-accent w-64 h-64 bottom-10 -left-32 fixed animate-float-delayed" />

    <div class="mx-auto max-w-4xl">
      <!-- Back link -->
      <router-link to="/dashboard" class="inline-flex items-center gap-2 text-brand-muted hover:text-brand-text text-sm transition-colors mb-6">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Volver al dashboard
      </router-link>

      <!-- Loading state -->
      <div v-if="isLoading && !task" class="text-center py-20">
        <svg class="w-10 h-10 mx-auto text-brand-primary animate-spin mb-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
        <p class="text-brand-muted">Cargando resultados...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="tasksStore.error && !task" class="glass-panel p-12 text-center">
        <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-red-500/20 flex items-center justify-center">
          <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        </div>
        <h2 class="font-outfit text-xl font-bold text-brand-text mb-2">Error al cargar</h2>
        <p class="text-brand-muted text-sm">{{ tasksStore.error }}</p>
      </div>

      <template v-else-if="task">
        <!-- Header -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 class="font-outfit text-2xl sm:text-3xl font-bold text-brand-text">
              {{ task.original_filename || 'Resultados' }}
            </h1>
            <p class="text-brand-muted text-sm mt-1">
              Tarea #{{ task.id }} — {{ formatDate(task.created_at) }}
            </p>
          </div>
          <span :class="statusBadge(task.status)">
            <span
              v-if="task.status === 'pending' || task.status === 'processing'"
              class="relative flex h-2 w-2"
            >
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75" :class="task.status === 'pending' ? 'bg-amber-400' : 'bg-blue-400'"></span>
              <span class="relative inline-flex rounded-full h-2 w-2" :class="task.status === 'pending' ? 'bg-amber-400' : 'bg-blue-400'"></span>
            </span>
            {{ statusLabel(task.status) }}
          </span>
        </div>

        <!-- Processing: Progress tracker -->
        <div v-if="task.status === 'pending' || task.status === 'processing'" class="mb-8">
          <ProgressTracker
            :processed="task.processed_emails || 0"
            :total="task.total_emails || 1"
          />
        </div>

        <!-- Error status -->
        <div v-else-if="task.status === 'error'" class="glass-panel p-8 text-center">
          <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-red-500/20 flex items-center justify-center shadow-neon-red">
            <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h3 class="font-outfit text-xl font-bold text-brand-text mb-2">Error en el procesamiento</h3>
          <p class="text-brand-muted text-sm">{{ task.error_message || 'Ocurrió un error inesperado. Intenta subir el archivo nuevamente.' }}</p>
        </div>

        <!-- Completed: Full results -->
        <template v-else-if="task.status === 'completed'">
          <!-- Diagnostic chart -->
          <div class="glass-panel p-8 mb-8">
            <h2 class="font-outfit text-xl font-bold text-brand-text mb-6 text-center">Diagnóstico de tu lista</h2>
            <DiagnosticChart
              :valid="diagnostic?.valid_count || 0"
              :invalid="diagnostic?.invalid_count || 0"
              :disposable="diagnostic?.disposable_count || 0"
            />
          </div>

          <!-- Summary insight -->
          <div v-if="problemPercentage > 0" class="glass-panel p-6 mb-8 border-amber-500/20">
            <div class="flex items-start gap-4">
              <div class="w-10 h-10 rounded-xl bg-amber-500/15 flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <div>
                <p class="text-brand-text font-semibold mb-1">
                  {{ problemPercentage }}% de tus correos son problemáticos
                </p>
                <p class="text-brand-muted text-sm">
                  Enviar a estas direcciones dañará tu reputación de envío y aumentará tu tasa de rebote.
                  Descarga el reporte limpio para mejorar tus métricas.
                </p>
              </div>
            </div>
          </div>

          <!-- Preview table -->
          <div v-if="diagnostic?.preview && diagnostic.preview.length > 0" class="glass-panel overflow-hidden mb-8">
            <div class="px-6 py-4 border-b border-brand-border">
              <h3 class="font-outfit text-lg font-bold text-brand-text">
                Vista previa <span class="text-brand-muted font-normal text-sm">(primeros {{ diagnostic.preview.length }} resultados)</span>
              </h3>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead>
                  <tr class="text-left text-brand-muted text-xs uppercase tracking-wider border-b border-brand-border">
                    <th class="px-6 py-3 font-medium">Correo</th>
                    <th class="px-6 py-3 font-medium">Estado</th>
                    <th class="px-6 py-3 font-medium hidden sm:table-cell">Motivo</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-brand-border">
                  <tr v-for="(row, idx) in diagnostic.preview" :key="idx" class="hover:bg-white/[0.02] transition-colors">
                    <td class="px-6 py-3 text-sm text-brand-text font-mono">{{ row.email }}</td>
                    <td class="px-6 py-3">
                      <span
                        class="badge"
                        :class="{
                          'badge-completed': row.status === 'valid',
                          'badge-error': row.status === 'invalid',
                          'badge-pending': row.status === 'disposable'
                        }"
                      >
                        {{ row.status === 'valid' ? 'Válido' : row.status === 'invalid' ? 'Inválido' : 'Desechable' }}
                      </span>
                    </td>
                    <td class="px-6 py-3 text-sm text-brand-muted hidden sm:table-cell">{{ row.reason || '—' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Download section -->
          <div class="glass-panel p-6 sm:p-8">
            <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
              <div>
                <h3 class="font-outfit text-xl font-bold text-brand-text mb-1">Descargar reporte limpio</h3>
                <p class="text-brand-muted text-sm">CSV con solo los correos válidos, listo para tu campaña.</p>
              </div>
              <button
                @click="handleDownload"
                :disabled="isDownloading"
                class="btn-emerald whitespace-nowrap py-3 px-8"
              >
                <svg v-if="isDownloading" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span>{{ isDownloading ? 'Descargando...' : 'Descargar CSV' }}</span>
              </button>
            </div>
          </div>
        </template>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useTasksStore } from '../stores/tasks'
import ProgressTracker from '../components/ProgressTracker.vue'
import DiagnosticChart from '../components/DiagnosticChart.vue'

const route = useRoute()
const tasksStore = useTasksStore()

const isLoading = ref(true)
const isDownloading = ref(false)
let pollInterval = null

const task = computed(() => tasksStore.currentTask)

const diagnostic = computed(() => tasksStore.diagnostic)

const problemPercentage = computed(() => {
  if (!diagnostic.value) return 0
  const total = (diagnostic.value.valid_count || 0) + (diagnostic.value.invalid_count || 0) + (diagnostic.value.disposable_count || 0)
  if (!total) return 0
  const problems = (diagnostic.value.invalid_count || 0) + (diagnostic.value.disposable_count || 0)
  return Math.round((problems / total) * 100)
})

onMounted(async () => {
  try {
    await tasksStore.fetchTask(route.params.id)
    if (task.value?.status === 'completed') {
      await tasksStore.fetchDiagnostic(route.params.id)
    } else if (task.value?.status === 'pending' || task.value?.status === 'processing') {
      startPolling()
    }
  } catch {
    // error handled in store
  } finally {
    isLoading.value = false
  }
})

onUnmounted(() => {
  stopPolling()
})

function startPolling() {
  pollInterval = setInterval(async () => {
    try {
      await tasksStore.fetchTask(route.params.id)
      if (task.value?.status === 'completed') {
        stopPolling()
        await tasksStore.fetchDiagnostic(route.params.id)
      } else if (task.value?.status === 'error') {
        stopPolling()
      }
    } catch {
      stopPolling()
    }
  }, 3000)
}

function stopPolling() {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
}

async function handleDownload() {
  isDownloading.value = true
  try {
    await tasksStore.downloadResults(route.params.id)
  } catch {
    // error in store
  } finally {
    isDownloading.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  const d = new Date(dateStr)
  return d.toLocaleDateString('es-CL', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function statusBadge(status) {
  const map = {
    pending: 'badge-pending',
    processing: 'badge-processing',
    completed: 'badge-completed',
    error: 'badge-error',
  }
  return map[status] || 'badge-pending'
}

function statusLabel(status) {
  const map = {
    pending: 'Pendiente',
    processing: 'Procesando',
    completed: 'Completado',
    error: 'Error',
  }
  return map[status] || status
}
</script>
