<template>
  <div class="glass-panel p-6 sm:p-8">
    <h3 class="font-outfit text-xl font-bold text-brand-text mb-4 text-center">
      Valida un correo gratis
    </h3>

    <div class="flex flex-col sm:flex-row gap-3">
      <input
        v-model="email"
        type="email"
        placeholder="ejemplo@correo.com"
        class="glass-input-lg flex-1"
        @keyup.enter="validate"
        :disabled="isLoading"
      />
      <button
        @click="validate"
        :disabled="isLoading || !email"
        class="btn-primary py-4 px-8 text-lg whitespace-nowrap"
      >
        <svg v-if="isLoading" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
        <span>{{ isLoading ? 'Validando...' : 'Validar' }}</span>
      </button>
    </div>

    <!-- Result -->
    <transition name="fade">
      <div v-if="result" class="mt-6 animate-scale-in">
        <div
          class="rounded-xl border p-5 flex items-start gap-4 transition-all duration-500"
          :class="resultClasses"
        >
          <div class="text-3xl flex-shrink-0 mt-0.5">{{ resultIcon }}</div>
          <div>
            <p class="font-outfit font-bold text-lg" :class="resultTextColor">
              {{ resultTitle }}
            </p>
            <p class="text-brand-muted text-sm mt-1" v-if="resultDetail">
              {{ resultDetail }}
            </p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import api from '../api/client'

const email = ref('')
const isLoading = ref(false)
const result = ref(null)

async function validate() {
  if (!email.value) return
  isLoading.value = true
  result.value = null

  try {
    const { data } = await api.post('/validate/single/', { email: email.value })
    result.value = data
  } catch (err) {
    result.value = {
      is_valid: false,
      reason: err.response?.data?.detail || 'Error de conexión. Intenta de nuevo.',
    }
  } finally {
    isLoading.value = false
  }
}

const resultIcon = computed(() => {
  if (!result.value) return ''
  if (result.value.is_disposable) return '⚠️'
  if (result.value.is_valid) return '✅'
  return '❌'
})

const resultTitle = computed(() => {
  if (!result.value) return ''
  if (result.value.is_disposable) return 'Dominio desechable detectado'
  if (result.value.is_valid) return 'Correo válido'
  return 'Correo inválido'
})

const resultDetail = computed(() => {
  if (!result.value) return ''
  if (result.value.is_disposable) {
    return 'Este correo utiliza un dominio temporal. No es recomendable enviar a esta dirección.'
  }
  if (result.value.is_valid) {
    return `El correo ${email.value} tiene un formato válido, el dominio existe y el buzón es alcanzable.`
  }
  return result.value.reason || 'El correo no pudo ser verificado. Revisa la dirección e intenta de nuevo.'
})

const resultClasses = computed(() => {
  if (!result.value) return ''
  if (result.value.is_disposable) {
    return 'bg-amber-500/10 border-amber-500/25 shadow-neon-amber'
  }
  if (result.value.is_valid) {
    return 'bg-emerald-500/10 border-emerald-500/25 shadow-neon-secondary'
  }
  return 'bg-red-500/10 border-red-500/25 shadow-neon-red'
})

const resultTextColor = computed(() => {
  if (!result.value) return ''
  if (result.value.is_disposable) return 'text-amber-400'
  if (result.value.is_valid) return 'text-emerald-400'
  return 'text-red-400'
})
</script>
