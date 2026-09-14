import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/lib/api'
import type { Stakeholder, StakeholderCategory } from '@/types/stakeholder'

interface CreatePayload {
  name: string
  category: StakeholderCategory
  interest_description?: string
}

export const useStakeholdersStore = defineStore('stakeholders', () => {
  const items = ref<Stakeholder[]>([])
  const isLoading = ref(false)

  async function fetch(projectId: string) {
    isLoading.value = true
    try {
      const { data } = await api.get<Stakeholder[]>(`/projects/${projectId}/stakeholders`)
      items.value = data
    } finally {
      isLoading.value = false
    }
  }

  async function create(projectId: string, payload: CreatePayload) {
    const { data } = await api.post<Stakeholder>(`/projects/${projectId}/stakeholders`, payload)
    items.value.push(data)
    return data
  }

  async function remove(projectId: string, stakeholderId: string) {
    await api.delete(`/projects/${projectId}/stakeholders/${stakeholderId}`)
    items.value = items.value.filter(s => s.id !== stakeholderId)
  }

  return {
    items,
    isLoading,
    fetch,
    create,
    remove,
  }
})
