import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/lib/api'
import type { UseCase, UseCaseCreatePayload } from '@/types/use-case'

export const useUseCasesStore = defineStore('useCases', () => {
  const items = ref<UseCase[]>([])
  const isLoading = ref(false)

  async function fetch(projectId: string) {
    isLoading.value = true
    try {
      const { data } = await api.get<UseCase[]>(`/projects/${projectId}/use-cases`)
      items.value = data
    } finally {
      isLoading.value = false
    }
  }

  async function create(projectId: string, payload: UseCaseCreatePayload) {
    const { data } = await api.post<UseCase>(`/projects/${projectId}/use-cases`, payload)
    items.value.push(data)
    return data
  }

  async function update(
    projectId: string,
    useCaseId: string,
    payload: Partial<UseCaseCreatePayload>,
  ) {
    const { data } = await api.patch<UseCase>(
      `/projects/${projectId}/use-cases/${useCaseId}`,
      payload,
    )
    const index = items.value.findIndex(uc => uc.id === useCaseId)
    if (index !== -1) {
      items.value[index] = data
    }
    return data
  }

  async function remove(projectId: string, useCaseId: string) {
    await api.delete(`/projects/${projectId}/use-cases/${useCaseId}`)
    items.value = items.value.filter(uc => uc.id !== useCaseId)
  }

  return {
    items,
    isLoading,
    fetch,
    create,
    update,
    remove,
  }
})
