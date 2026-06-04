<template>
  <div
    class="inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold border transition-all duration-300"
    :class="colorClasses"
  >
    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"
      />
    </svg>
    <span>{{ formatted }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  credits: {
    type: Number,
    default: 0,
  },
})

const formatted = computed(() => {
  return new Intl.NumberFormat('es-CL').format(props.credits)
})

const colorClasses = computed(() => {
  if (props.credits > 500) {
    return 'bg-emerald-500/15 text-emerald-400 border-emerald-500/25 shadow-neon-secondary'
  }
  if (props.credits >= 100) {
    return 'bg-amber-500/15 text-amber-400 border-amber-500/25 shadow-neon-amber'
  }
  return 'bg-red-500/15 text-red-400 border-red-500/25 shadow-neon-red'
})
</script>
