<template>
  <div
    class="relative rounded-2xl border-2 border-dashed transition-all duration-300 cursor-pointer"
    :class="[
      isDragging
        ? 'border-brand-primary bg-brand-primary/10 shadow-neon-primary'
        : 'border-brand-border hover:border-brand-borderHover hover:bg-white/[0.02]',
      selectedFile ? 'p-6' : 'p-10 sm:p-16'
    ]"
    @dragover.prevent="isDragging = true"
    @dragleave.prevent="isDragging = false"
    @drop.prevent="onDrop"
    @click="openPicker"
  >
    <input
      ref="fileInput"
      type="file"
      accept=".csv,.txt"
      class="hidden"
      @change="onFileSelected"
    />

    <!-- Empty state -->
    <div v-if="!selectedFile" class="text-center">
      <div class="mx-auto w-16 h-16 rounded-2xl bg-brand-primary/10 border border-brand-primary/20 flex items-center justify-center mb-4">
        <svg class="w-8 h-8 text-brand-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
          />
        </svg>
      </div>
      <p class="font-outfit text-lg font-semibold text-brand-text mb-1">
        Arrastra tu archivo CSV aquí
      </p>
      <p class="text-brand-muted text-sm">
        o <span class="text-brand-primary font-medium">haz clic para seleccionar</span>
      </p>
      <p class="text-brand-muted/60 text-xs mt-3">
        Formatos aceptados: .csv, .txt — Máximo 10MB
      </p>
    </div>

    <!-- File selected -->
    <div v-else class="flex items-center gap-4">
      <div class="w-12 h-12 rounded-xl bg-brand-secondary/15 border border-brand-secondary/25 flex items-center justify-center flex-shrink-0">
        <svg class="w-6 h-6 text-brand-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
      </div>
      <div class="flex-1 min-w-0">
        <p class="font-outfit font-semibold text-brand-text truncate">{{ selectedFile.name }}</p>
        <p class="text-brand-muted text-sm">{{ formatSize(selectedFile.size) }}</p>
      </div>
      <button
        @click.stop="clearFile"
        class="p-2 text-brand-muted hover:text-red-400 transition-colors rounded-lg hover:bg-red-500/10"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['file-selected', 'file-cleared'])

const fileInput = ref(null)
const selectedFile = ref(null)
const isDragging = ref(false)

const MAX_SIZE = 10 * 1024 * 1024 // 10MB

function openPicker() {
  if (!selectedFile.value) {
    fileInput.value?.click()
  }
}

function onFileSelected(e) {
  const file = e.target.files?.[0]
  if (file) handleFile(file)
}

function onDrop(e) {
  isDragging.value = false
  const file = e.dataTransfer.files?.[0]
  if (file) handleFile(file)
}

function handleFile(file) {
  if (file.size > MAX_SIZE) {
    alert('El archivo excede el límite de 10MB.')
    return
  }
  const ext = file.name.split('.').pop()?.toLowerCase()
  if (!['csv', 'txt'].includes(ext)) {
    alert('Solo se aceptan archivos .csv o .txt')
    return
  }
  selectedFile.value = file
  emit('file-selected', file)
}

function clearFile() {
  selectedFile.value = null
  if (fileInput.value) fileInput.value.value = ''
  emit('file-cleared')
}

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1048576).toFixed(2) + ' MB'
}
</script>
