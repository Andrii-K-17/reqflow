import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/lib/api'
import type { BusinessGoal, Priority } from '@/types/business-goal'

interface CreatePayload {
  title: string
  description?: string
  priority: Priority
}

export const useBusinessGoalsStore = defineStore('businessGoals', () => {
  const items = ref<BusinessGoal[]>([])
  const isLoading = ref(false)

  async function fetch(projectId: string) {
    isLoading.value = true
    try {
      const { data } = await api.get<BusinessGoal[]>(`/projects/${projectId}/business-goals`)
      items.value = data
    } finally {
      isLoading.value = false
    }
  }

  async function create(projectId: string, payload: CreatePayload) {
    const { data } = await api.post<BusinessGoal>(`/projects/${projectId}/business-goals`, payload)
    items.value.push(data)
    return data
  }

  async function remove(projectId: string, goalId: string) {
    await api.delete(`/projects/${projectId}/business-goals/${goalId}`)
    items.value = items.value.filter(g => g.id !== goalId)
  }

  return {
    items,
    isLoading,
    fetch,
    create,
    remove,
  }
})
