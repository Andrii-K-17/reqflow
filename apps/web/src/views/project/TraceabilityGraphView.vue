<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useTraceLinksStore } from '@/stores/traceLinks'
import MermaidRenderer from '@/components/MermaidRenderer.vue'
import { Loader2, GitBranch } from '@lucide/vue'

const route = useRoute()
const projectId = route.params.projectId as string
const traceLinks = useTraceLinksStore()
const isLoading = ref(true)

onMounted(async () => {
  isLoading.value = true
  try {
    await traceLinks.fetchGraph(projectId)
  } finally {
    isLoading.value = false
  }
})

function sanitizeId(id: string): string {
  return `n_${id.replace(/-/g, '')}`
}

function escapeLabel(text: string): string {
  return text.replace(/"/g, "'")
}

const relationArrow: Record<string, string> = {
  DERIVES_FROM: '-->',
  SATISFIES: '-->',
  CONFLICTS_WITH: '-.->',
}

const mermaidCode = computed(() => {
  const graph = traceLinks.graph
  if (!graph || graph.nodes.length === 0) return ''

  const lines = ['graph LR']

  for (const node of graph.nodes) {
    const shape =
      node.type === 'BUSINESS_GOAL'
        ? `(("${escapeLabel(node.code)}: ${escapeLabel(node.label)}"))`
        : `["${escapeLabel(node.code)}: ${escapeLabel(node.label)}"]`
    lines.push(`  ${sanitizeId(node.id)}${shape}`)
  }

  for (const edge of graph.edges) {
    const arrow = relationArrow[edge.relation] ?? '-->'
    lines.push(`  ${sanitizeId(edge.from_id)} ${arrow}|${edge.relation}| ${sanitizeId(edge.to_id)}`)
  }

  return lines.join('\n')
})
</script>

<template>
  <section class="flex flex-1 flex-col min-h-0 h-full">
    <div
      v-if="isLoading"
      class="flex flex-1 items-center justify-center gap-2 text-base text-slate-600 dark:text-slate-400"
    >
      <Loader2 class="h-4 w-4 animate-spin" />
      Loading…
    </div>

    <div
      v-else-if="!traceLinks.graph || traceLinks.graph.nodes.length === 0"
      class="flex flex-1 items-center justify-center"
    >
      <div
        class="rounded-xl border border-blue-400/30 bg-blue-50/40 px-6 py-8 text-center dark:border-slate-700 dark:bg-slate-900/60"
      >
        <GitBranch class="mx-auto mb-2 h-6 w-6 text-slate-400 dark:text-slate-500" />
        <p class="text-sm text-slate-600 dark:text-slate-400">
          The graph is empty — add traceability links from the requirement, use case or goal pages.
        </p>
      </div>
    </div>

    <div
      v-else
      class="rounded-xl border border-blue-400/30 bg-white/70 p-1 backdrop-blur-sm scrollbar-thin dark:border-slate-700 dark:bg-slate-900/60"
    >
      <MermaidRenderer :code="mermaidCode" />
    </div>

    <p
      class="mt-3 flex flex-shrink-0 items-center gap-5 text-sm text-slate-500 dark:text-slate-400"
    >
      <div>Solid line: DERIVES_FROM / SATISFIES</div>
      <div>Dashed line: CONFLICTS_WITH</div>
    </p>
  </section>
</template>
