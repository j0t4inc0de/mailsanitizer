<template>
  <div class="glass-panel p-6">
    <!-- Progress bar -->
    <div class="relative h-4 rounded-full bg-white/5 overflow-hidden mb-4">
      <div
        class="absolute inset-y-0 left-0 rounded-full transition-all duration-700 ease-out animate-progress-pulse"
        :style="{ width: percentage + '%' }"
        style="background: linear-gradient(90deg, #8B5CF6, #3B82F6, #10B981);"
      ></div>
    </div>

    <!-- Stats -->
    <div class="flex items-center justify-between">
      <p class="text-brand-muted text-sm">
        <span v-if="processed < total">
          Procesando <strong class="text-brand-text">{{ processed.toLocaleString('es-CL') }}</strong>
          de <strong class="text-brand-text">{{ total.toLocaleString('es-CL') }}</strong> correos...
        </span>
        <span v-else class="text-brand-secondary font-medium">
          ¡Procesamiento completo!
        </span>
      </p>
      <span class="font-outfit text-xl font-bold text-brand-text">
        {{ percentage }}%
      </span>
    </div>

    <!-- Pulse indicator -->
    <div v-if="processed < total" class="flex items-center gap-2 mt-3">
      <span class="relative flex h-2.5 w-2.5">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-accent opacity-75"></span>
        <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-brand-accent"></span>
      </span>
      <span class="text-brand-muted text-xs">Validación en progreso</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  processed: { type: Number, default: 0 },
  total: { type: Number, default: 1 },
})

const percentage = computed(() => {
  if (!props.total) return 0
  return Math.min(100, Math.round((props.processed / props.total) * 100))
})
</script>
