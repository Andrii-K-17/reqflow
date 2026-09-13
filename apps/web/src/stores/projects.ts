import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/lib/api'
import type { Project } from '@/types/project'

export const useProjectsStore = defineStore('projects', () => {
  const projects = ref<Project[]>([])
  const isLoading = ref(false)

  async function fetchProjects() {
    isLoading.value = true
    try {
      const { data } = await api.get<Project[]>('/projects')
      projects.value = data
    } finally {
      isLoading.value = false
    }
  }

  async function createProject(payload: { name: string; description?: string }) {
    const { data } = await api.post<Project>('/projects', payload)
    projects.value.unshift(data)
    return data
  }

  return {
    projects,
    isLoading,
    fetchProjects,
    createProject,
  }
})
