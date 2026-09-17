<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useRequirementsStore } from '@/stores/requirements'
import { useBusinessGoalsStore } from '@/stores/businessGoals'
import { useUseCasesStore } from '@/stores/useCases'
import { useTraceLinksStore } from '@/stores/traceLinks'
import { GitBranch, Loader2, Target, Workflow, ArrowRight, LayoutGrid, Share2 } from '@lucide/vue'
import TraceabilityGraphView from './TraceabilityGraphView.vue'

const route = useRoute()
const projectId = route.params.projectId as string

const requirements = useRequirementsStore()
const goals = useBusinessGoalsStore()
const useCases = useUseCasesStore()
const traceLinks = useTraceLinksStore()

const activeTab = ref<'matrix' | 'graph'>('matrix')
const isLoading = ref(true)

const tabs = [
  { key: 'matrix' as const, label: 'Matrix', icon: LayoutGrid },
  { key: 'graph' as const, label: 'Graph', icon: Share2 },
]

onMounted(async () => {
  isLoading.value = true
  try {
    await Promise.all([
      requirements.fetch(projectId, { page_size: 100 }),
      goals.fetch(projectId),
      useCases.fetch(projectId),
      traceLinks.fetch(projectId),
    ])
  } finally {
    isLoading.value = false
  }
})

interface MatrixRow {
  requirementId: string
  code: string
  title: string
  goalTitles: string[]
  useCaseCodes: string[]
}

const rows = computed<MatrixRow[]>(() => {
  return requirements.items.map(req => {
    const goalTitles = traceLinks.items
      .filter(
        l =>
          l.from_type === 'REQUIREMENT' &&
          l.from_id === req.id &&
          l.to_type === 'BUSINESS_GOAL' &&
          l.relation === 'DERIVES_FROM',
      )
      .map(l => goals.items.find(g => g.id === l.to_id)?.title)
      .filter((t): t is string => Boolean(t))

    const useCaseCodes = traceLinks.items
      .filter(
        l =>
          l.to_type === 'REQUIREMENT' &&
          l.to_id === req.id &&
          l.from_type === 'USE_CASE' &&
          l.relation === 'SATISFIES',
      )
      .map(l => useCases.items.find(uc => uc.id === l.from_id)?.code)
      .filter((c): c is string => Boolean(c))

    return {
      requirementId: req.id,
      code: req.code,
      title: req.title,
      goalTitles,
      useCaseCodes,
    }
  })
})

const coveragePercent = computed(() => {
  if (rows.value.length === 0) return 0
  const covered = rows.value.filter(
    r => r.goalTitles.length > 0 || r.useCaseCodes.length > 0,
  ).length
  return Math.round((covered / rows.value.length) * 100)
})
</script>

<template>
  <section class="flex flex-1 flex-col min-h-0 h-full">
    <div class="mb-4 flex flex-shrink-0 items-center justify-between">
      <div class="flex items-center gap-2.5">
        <div class="rounded-lg bg-sky-100 p-1.5 text-sky-500 dark:bg-sky-500/10 dark:text-sky-400">
          <GitBranch class="h-4 w-4" />
        </div>
        <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Traceability</h2>
      </div>
      <span
        v-if="activeTab === 'matrix'"
        class="rounded-full bg-sky-100 px-3 py-1 text-sm font-medium text-sky-600 dark:bg-sky-500/10 dark:text-sky-400"
      >
        Coverage: {{ coveragePercent }}%
      </span>
    </div>

    <div
      class="mb-4 flex flex-shrink-0 gap-1.5 rounded-xl border border-blue-400/30 bg-blue-50/40 p-1.5 w-fit dark:border-slate-700 dark:bg-slate-900/60"
    >
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-medium transition-all hover:cursor-pointer"
        :class="
          activeTab === tab.key
            ? 'bg-sky-500 text-white shadow-sm dark:bg-sky-600'
            : 'text-slate-600 hover:bg-blue-50/70 dark:text-slate-400 dark:hover:bg-slate-800/70'
        "
        @click="activeTab = tab.key"
      >
        <component :is="tab.icon" class="h-3.5 w-3.5" />
        {{ tab.label }}
      </button>
    </div>

    <template v-if="activeTab === 'matrix'">
      <p
        class="flex flex-shrink-0 flex-wrap items-center justify-between gap-2 mb-4 text-sm text-slate-600 dark:text-slate-400"
      >
        <span
          class="inline-flex items-center gap-1.5 font-medium text-slate-700 dark:text-slate-300"
        >
          Business Goal
          <ArrowRight class="h-3.5 w-3.5 shrink-0 text-slate-500 dark:text-slate-400" />
          Requirement
          <ArrowRight class="h-3.5 w-3.5 shrink-0 text-slate-500 dark:text-slate-400" />
          Use Case
        </span>
        <span>
          Empty cells mean there's no link yet — add one from the corresponding requirement's page.
        </span>
      </p>

      <div
        v-if="isLoading"
        class="flex flex-1 items-center justify-center gap-2 text-base text-slate-600 dark:text-slate-400"
      >
        <Loader2 class="h-4 w-4 animate-spin" />
        Loading…
      </div>

      <div
        v-else
        class="flex overflow-hidden rounded-xl border border-blue-400/30 bg-white/70 backdrop-blur-sm dark:border-slate-700 dark:bg-slate-900/60"
      >
        <div class="flex-1 h-auto overflow-y-auto scrollbar-thin">
          <table class="w-full text-sm table-auto border-collapse">
            <thead
              class="bg-blue-50/60 shadow text-left text-sm uppercase tracking-wider text-slate-500 dark:bg-slate-900/80 dark:text-slate-400"
            >
              <tr>
                <th
                  class="sticky top-0 z-10 border-b border-blue-200/60 bg-blue-50/70 backdrop-blur-sm px-4 py-3 dark:border-slate-800 dark:bg-slate-900"
                >
                  Requirement
                </th>
                <th
                  class="sticky top-0 z-10 border-b border-blue-200/60 bg-blue-50/70 backdrop-blur-sm px-4 py-3 dark:border-slate-800 dark:bg-slate-900"
                >
                  Business Goals
                </th>
                <th
                  class="sticky top-0 z-10 border-b border-blue-200/60 bg-blue-50/70 backdrop-blur-sm px-4 py-3 dark:border-slate-800 dark:bg-slate-900"
                >
                  Use Cases
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="row in rows"
                :key="row.requirementId"
                class="border-t border-blue-400/20 transition-colors hover:bg-blue-100/50 dark:border-slate-800 dark:hover:bg-slate-800/40"
              >
                <td class="px-4 py-3">
                  <router-link
                    :to="{
                      name: 'requirement-detail',
                      params: { projectId, requirementId: row.requirementId },
                    }"
                    class="font-medium text-slate-900 transition-colors hover:text-sky-500 dark:text-white dark:hover:text-sky-400"
                  >
                    {{ row.code }}
                  </router-link>
                  <p class="text-sm text-slate-500 dark:text-slate-400">{{ row.title }}</p>
                </td>
                <td class="px-4 py-3">
                  <span
                    v-if="row.goalTitles.length === 0"
                    class="text-sm text-slate-300 dark:text-slate-600"
                    >—</span
                  >
                  <ul v-else class="space-y-1">
                    <li
                      v-for="g in row.goalTitles"
                      :key="g"
                      class="flex items-start gap-1 text-sm text-slate-600 dark:text-slate-400"
                    >
                      <Target class="mt-0.5 h-3 w-3 shrink-0 text-slate-400 dark:text-slate-500" />
                      {{ g }}
                    </li>
                  </ul>
                </td>
                <td class="px-4 py-3">
                  <span
                    v-if="row.useCaseCodes.length === 0"
                    class="text-sm text-slate-300 dark:text-slate-600"
                    >—</span
                  >
                  <span v-else class="flex flex-wrap gap-1">
                    <span
                      v-for="c in row.useCaseCodes"
                      :key="c"
                      class="flex items-center gap-1 rounded-full bg-sky-100 px-2 py-0.5 text-sm text-sky-600 dark:bg-sky-500/10 dark:text-sky-400"
                    >
                      <Workflow class="h-3 w-3" />
                      {{ c }}
                    </span>
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <div v-else class="flex flex-1 min-h-0">
      <TraceabilityGraphView />
    </div>
  </section>
</template>
