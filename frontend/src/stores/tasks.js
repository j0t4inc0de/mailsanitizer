import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/client'

export const useTasksStore = defineStore('tasks', () => {
  const tasks = ref([])
  const currentTask = ref(null)
  const diagnostic = ref(null)
  const isLoading = ref(false)
  const error = ref('')

  function mapTask(t) {
    if (!t) return null
    const statusMap = {
      'pendiente': 'pending',
      'procesando': 'processing',
      'completado': 'completed',
      'error': 'error'
    }
    return {
      id: t.id,
      original_filename: t.nombre_archivo,
      total_emails: t.total_correos,
      processed_emails: t.procesados,
      valid: t.validos,
      invalid: t.invalidos,
      throwaway: t.desechables,
      status: statusMap[t.estado] || t.estado,
      is_free: t.es_gratuita,
      progress: t.progreso,
      created_at: t.created_at,
      completed_at: t.completed_at
    }
  }

  async function fetchTasks() {
    isLoading.value = true
    error.value = ''
    try {
      const { data } = await api.get('/tasks/')
      const rawTasks = data.results || data
      tasks.value = rawTasks.map(mapTask)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al cargar tareas'
    } finally {
      isLoading.value = false
    }
  }

  async function fetchTask(id) {
    isLoading.value = true
    error.value = ''
    try {
      const { data } = await api.get(`/tasks/${id}/`)
      const task = mapTask(data)
      currentTask.value = task
      return task
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al cargar la tarea'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function uploadCSV(file) {
    isLoading.value = true
    error.value = ''
    try {
      const formData = new FormData()
      formData.append('file', file)
      const { data } = await api.post('/validate/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      const task = mapTask(data.tarea)
      currentTask.value = task
      return task
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al subir el archivo'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchDiagnostic(id) {
    try {
      const { data } = await api.get(`/tasks/${id}/diagnostic/`)
      diagnostic.value = data
      return data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al cargar el diagnóstico'
      throw err
    }
  }

  async function downloadResults(id) {
    try {
      const { data } = await api.get(`/tasks/${id}/download/`, {
        responseType: 'blob',
      })
      const url = window.URL.createObjectURL(new Blob([data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `cleanmail-results-${id}.csv`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al descargar resultados'
      throw err
    }
  }

  return {
    tasks,
    currentTask,
    diagnostic,
    isLoading,
    error,
    fetchTasks,
    fetchTask,
    uploadCSV,
    fetchDiagnostic,
    downloadResults,
  }
})
