<template>
  <div class="flex flex-col items-center">
    <!-- SVG Donut Chart -->
    <div class="relative w-56 h-56 sm:w-64 sm:h-64">
      <svg class="w-full h-full -rotate-90" viewBox="0 0 200 200">
        <!-- Background circle -->
        <circle
          cx="100" cy="100" r="80"
          fill="none"
          stroke="rgba(255,255,255,0.05)"
          stroke-width="24"
        />
        <!-- Valid segment -->
        <circle
          cx="100" cy="100" r="80"
          fill="none"
          stroke="#10B981"
          stroke-width="24"
          stroke-linecap="round"
          :stroke-dasharray="validDash"
          stroke-dashoffset="0"
          class="transition-all duration-1000 ease-out"
          :style="{ strokeDasharray: animatedValid }"
        />
        <!-- Invalid segment -->
        <circle
          cx="100" cy="100" r="80"
          fill="none"
          stroke="#EF4444"
          stroke-width="24"
          stroke-linecap="round"
          :stroke-dasharray="invalidDash"
          :stroke-dashoffset="'-' + validLength"
          class="transition-all duration-1000 ease-out delay-200"
          :style="{ strokeDasharray: animatedInvalid }"
        />
        <!-- Disposable segment -->
        <circle
          cx="100" cy="100" r="80"
          fill="none"
          stroke="#F59E0B"
          stroke-width="24"
          stroke-linecap="round"
          :stroke-dasharray="disposableDash"
          :stroke-dashoffset="'-' + (validLength + invalidLength)"
          class="transition-all duration-1000 ease-out delay-500"
          :style="{ strokeDasharray: animatedDisposable }"
        />
      </svg>

      <!-- Center text -->
      <div class="absolute inset-0 flex flex-col items-center justify-center">
        <span class="font-outfit text-3xl font-bold text-brand-text">
          {{ total.toLocaleString('es-CL') }}
        </span>
        <span class="text-brand-muted text-sm">correos</span>
      </div>
    </div>

    <!-- Legend -->
    <div class="flex flex-wrap justify-center gap-4 sm:gap-6 mt-6">
      <div class="flex items-center gap-2">
        <span class="w-3 h-3 rounded-full bg-emerald-500"></span>
        <span class="text-sm text-brand-muted">Válidos</span>
        <span class="text-sm font-semibold text-emerald-400">{{ valid }}</span>
        <span class="text-xs text-brand-muted">({{ validPct }}%)</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-3 h-3 rounded-full bg-red-500"></span>
        <span class="text-sm text-brand-muted">Inválidos</span>
        <span class="text-sm font-semibold text-red-400">{{ invalid }}</span>
        <span class="text-xs text-brand-muted">({{ invalidPct }}%)</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-3 h-3 rounded-full bg-amber-500"></span>
        <span class="text-sm text-brand-muted">Desechables</span>
        <span class="text-sm font-semibold text-amber-400">{{ disposable }}</span>
        <span class="text-xs text-brand-muted">({{ disposablePct }}%)</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'

const props = defineProps({
  valid: { type: Number, default: 0 },
  invalid: { type: Number, default: 0 },
  disposable: { type: Number, default: 0 },
})

const circumference = 2 * Math.PI * 80 // ≈ 502.65
const animated = ref(false)

const total = computed(() => props.valid + props.invalid + props.disposable)

const validPct = computed(() => total.value ? Math.round((props.valid / total.value) * 100) : 0)
const invalidPct = computed(() => total.value ? Math.round((props.invalid / total.value) * 100) : 0)
const disposablePct = computed(() => total.value ? Math.round((props.disposable / total.value) * 100) : 0)

const validLength = computed(() => total.value ? (props.valid / total.value) * circumference : 0)
const invalidLength = computed(() => total.value ? (props.invalid / total.value) * circumference : 0)
const disposableLength = computed(() => total.value ? (props.disposable / total.value) * circumference : 0)

const validDash = computed(() => `${validLength.value} ${circumference}`)
const invalidDash = computed(() => `${invalidLength.value} ${circumference}`)
const disposableDash = computed(() => `${disposableLength.value} ${circumference}`)

const animatedValid = computed(() => animated.value ? validDash.value : `0 ${circumference}`)
const animatedInvalid = computed(() => animated.value ? invalidDash.value : `0 ${circumference}`)
const animatedDisposable = computed(() => animated.value ? disposableDash.value : `0 ${circumference}`)

onMounted(() => {
  requestAnimationFrame(() => {
    animated.value = true
  })
})
</script>
