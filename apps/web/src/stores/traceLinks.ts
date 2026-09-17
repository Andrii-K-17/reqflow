import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/lib/api'
import type { TraceEntityType, TraceGraph, TraceLink, TraceRelation } from '@/types/trace-link'

export const useTraceLinksStore = defineStore('traceLinks', () => {
  const items = ref<TraceLink[]>([])
  const graph = ref<TraceGraph | null>(null)
  const isLoading = ref(false)

  async function fetch(projectId: string) {
    isLoading.value = true
    try {
      const { data } = await api.get<TraceLink[]>(`/projects/${projectId}/trace-links`)
      items.value = data
    } finally {
      isLoading.value = false
    }
  }

  async function fetchGraph(projectId: string) {
    const { data } = await api.get<TraceGraph>(`/projects/${projectId}/trace-links/graph`)
    graph.value = data
    return data
  }

  async function create(
    projectId: string,
    payload: {
      from_type: TraceEntityType
      from_id: string
      to_type: TraceEntityType
      to_id: string
      relation: TraceRelation
    },
  ) {
    const { data } = await api.post<TraceLink>(`/projects/${projectId}/trace-links`, payload)
    items.value.push(data)
    return data
  }

  async function remove(projectId: string, linkId: string) {
    await api.delete(`/projects/${projectId}/trace-links/${linkId}`)
    items.value = items.value.filter(l => l.id !== linkId)
  }

  function linksFor(entityType: TraceEntityType, entityId: string): TraceLink[] {
    return items.value.filter(
      l =>
        (l.from_type === entityType && l.from_id === entityId) ||
        (l.to_type === entityType && l.to_id === entityId),
    )
  }

  return {
    items,
    graph,
    isLoading,
    fetch,
    fetchGraph,
    create,
    remove,
    linksFor,
  }
})
