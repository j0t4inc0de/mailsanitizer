<template>
  <div class="relative min-h-screen pt-24 pb-16 px-4">
    <!-- Background glow orbs -->
    <div class="glow-orb-primary w-80 h-80 -top-40 -right-40 fixed animate-float" />
    <div class="glow-orb-accent w-72 h-72 bottom-10 -left-36 fixed animate-float-delayed" />

    <div class="mx-auto max-w-6xl">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 class="font-outfit text-3xl sm:text-4xl font-bold text-brand-text">Dashboard</h1>
          <p class="text-brand-muted mt-1">
            Bienvenido, <span class="text-brand-text">{{ auth.user?.email || 'usuario' }}</span>
          </p>
        </div>
        <router-link to="/upload" class="btn-primary text-base py-3 px-6 whitespace-nowrap">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nueva validación
        </router-link>
      </div>

      <!-- Credit balance card -->
      <div class="glass-panel p-6 sm:p-8 mb-8">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <p class="text-brand-muted text-sm mb-1">Tu balance de créditos</p>
            <div class="flex items-baseline gap-2">
              <span
                class="font-outfit text-5xl font-extrabold"
                :class="auth.credits > 0 ? 'text-brand-secondary' : 'text-red-400'"
                :style="auth.credits > 0 ? 'text-shadow: 0 0 30px rgba(16,185,129,0.4)' : 'text-shadow: 0 0 30px rgba(239,68,68,0.4)'"
              >
                {{ auth.credits.toLocaleString('es-CL') }}
              </span>
              <span class="text-brand-muted text-lg">créditos</span>
            </div>
          </div>
          <router-link to="/pricing" class="btn-secondary whitespace-nowrap">
            Comprar créditos
          </router-link>
        </div>
      </div>

      <!-- Task history -->
      <div class="glass-panel overflow-hidden">
        <div class="px-6 py-5 border-b border-brand-border">
          <h2 class="font-outfit text-xl font-bold text-brand-text">Historial de validaciones</h2>
        </div>

        <!-- Loading -->
        <div v-if="tasksStore.isLoading" class="p-12 text-center">
          <svg class="w-8 h-8 mx-auto text-brand-primary animate-spin mb-3" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <p class="text-brand-muted text-sm">Cargando tareas...</p>
        </div>

        <!-- Empty state -->
        <div v-else-if="tasksStore.tasks.length === 0" class="p-12 sm:p-16 text-center">
          <div class="w-20 h-20 mx-auto mb-6 rounded-2xl bg-brand-primary/10 border border-brand-primary/20 flex items-center justify-center">
            <svg class="w-10 h-10 text-brand-primary/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 class="font-outfit text-xl font-bold text-brand-text mb-2">Sin validaciones aún</h3>
          <p class="text-brand-muted text-sm mb-6">Sube tu primer archivo CSV para comenzar a validar correos.</p>
          <router-link to="/upload" class="btn-primary">
            Subir mi primer archivo
          </router-link>
        </div>

        <!-- Tasks table -->
        <div v-else class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="text-left text-brand-muted text-xs uppercase tracking-wider border-b border-brand-border">
                <th class="px-6 py-3 font-medium">Archivo</th>
                <th class="px-6 py-3 font-medium hidden sm:table-cell">Fecha</th>
                <th class="px-6 py-3 font-medium">Correos</th>
                <th class="px-6 py-3 font-medium">Estado</th>
                <th class="px-6 py-3 font-medium text-right">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-brand-border">
              <tr
                v-for="task in tasksStore.tasks"
                :key="task.id"
                class="hover:bg-white/[0.02] transition-colors"
              >
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-brand-primary/10 flex items-center justify-center flex-shrink-0">
                      <svg class="w-4 h-4 text-brand-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                    <span class="text-brand-text text-sm font-medium truncate max-w-[180px]">
                      {{ task.original_filename || 'archivo.csv' }}
                    </span>
                  </div>
                </td>
                <td class="px-6 py-4 hidden sm:table-cell">
                  <span class="text-brand-muted text-sm">{{ formatDate(task.created_at) }}</span>
                </td>
                <td class="px-6 py-4">
                  <span class="text-brand-text text-sm font-medium">
                    {{ (task.total_emails || 0).toLocaleString('es-CL') }}
                  </span>
                </td>
                <td class="px-6 py-4">
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
                </td>
                <td class="px-6 py-4 text-right">
                  <router-link
                    :to="`/tasks/${task.id}`"
                    class="text-brand-primary hover:text-brand-primary/80 text-sm font-medium transition-colors"
                  >
                    Ver resultados →
                  </router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useTasksStore } from '../stores/tasks'

const auth = useAuthStore()
const tasksStore = useTasksStore()

onMounted(() => {
  tasksStore.fetchTasks()
  auth.fetchUser()
})

function formatDate(dateStr) {
  if (!dateStr) return '—'
  const d = new Date(dateStr)
  return d.toLocaleDateString('es-CL', { day: '2-digit', month: 'short', year: 'numeric' })
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
