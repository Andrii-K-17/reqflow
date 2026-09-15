import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/lib/api'
import type { UserStory, UserStoryCreatePayload } from '@/types/user-story'

export const useUserStoriesStore = defineStore('userStories', () => {
  const items = ref<UserStory[]>([])
  const isLoading = ref(false)

  async function fetch(projectId: string) {
    isLoading.value = true
    try {
      const { data } = await api.get<UserStory[]>(`/projects/${projectId}/user-stories`)
      items.value = data
    } finally {
      isLoading.value = false
    }
  }

  async function create(projectId: string, payload: UserStoryCreatePayload) {
    const { data } = await api.post<UserStory>(`/projects/${projectId}/user-stories`, payload)
    items.value.push(data)
    return data
  }

  async function update(
    projectId: string,
    storyId: string,
    payload: Partial<UserStoryCreatePayload>,
  ) {
    const { data } = await api.patch<UserStory>(
      `/projects/${projectId}/user-stories/${storyId}`,
      payload,
    )
    const index = items.value.findIndex(s => s.id === storyId)
    if (index !== -1) {
      items.value[index] = data
    }
    return data
  }

  async function remove(projectId: string, storyId: string) {
    await api.delete(`/projects/${projectId}/user-stories/${storyId}`)
    items.value = items.value.filter(s => s.id !== storyId)
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
