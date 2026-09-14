import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/lib/api'
import type {
  Requirement,
  RequirementCreatePayload,
  RequirementFilters,
  RequirementPage,
  RequirementUpdatePayload,
} from '@/types/requirement'

export const useRequirementsStore = defineStore('requirements', () => {
  const items = ref<Requirement[]>([])
  const total = ref(0)
  const page = ref(1)
  const pageSize = ref(20)
  const isLoading = ref(false)

  async function fetch(projectId: string, filters: RequirementFilters = {}) {
    isLoading.value = true
    try {
      const { data } = await api.get<RequirementPage>(`/projects/${projectId}/requirements`, {
        params: filters,
      })
      items.value = data.items
      total.value = data.total
      page.value = data.page
      pageSize.value = data.page_size
    } finally {
      isLoading.value = false
    }
  }

  async function create(projectId: string, payload: RequirementCreatePayload) {
    const { data } = await api.post<Requirement>(`/projects/${projectId}/requirements`, payload)
    items.value.unshift(data)
    total.value += 1
    return data
  }

  async function update(
    projectId: string,
    requirementId: string,
    payload: RequirementUpdatePayload,
  ) {
    const { data } = await api.patch<Requirement>(
      `/projects/${projectId}/requirements/${requirementId}`,
      payload,
    )
    const index = items.value.findIndex(r => r.id === requirementId)
    if (index !== -1) {
      items.value[index] = data
    }
    return data
  }

  async function remove(projectId: string, requirementId: string) {
    await api.delete(`/projects/${projectId}/requirements/${requirementId}`)
    items.value = items.value.filter(r => r.id !== requirementId)
    total.value -= 1
  }

  async function fetchOne(projectId: string, requirementId: string) {
    const { data } = await api.get<Requirement>(
      `/projects/${projectId}/requirements/${requirementId}`,
    )
    return data
  }

  return {
    items,
    total,
    page,
    pageSize,
    isLoading,
    fetch,
    create,
    update,
    remove,
    fetchOne,
  }
})
