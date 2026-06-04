import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/client'

export const useTasksStore = defineStore('tasks', () => {
  const tasks = ref([])
  const currentTask = ref(null)
  const diagnostic = ref(null)
  const isLoading = ref(false)
  const error = ref('')

  async function fetchTasks() {
    isLoading.value = true
    error.value = ''
    try {
      const { data } = await api.get('/tasks/')
      tasks.value = data.results || data
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
      currentTask.value = data
      return data
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
      currentTask.value = data
      return data
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
