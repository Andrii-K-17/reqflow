<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useRequirementsStore } from '@/stores/requirements'
import RequirementBadges from '@/components/RequirementBadges.vue'
import type { RequirementFilters } from '@/types/requirement'
import RequirementForm from '@/components/RequirementForm.vue'
import {
  ListChecks,
  Plus,
  SlidersHorizontal,
  Loader2,
  AlertTriangle,
  ChevronRight,
  ChevronDown,
} from '@lucide/vue'

const route = useRoute()
const router = useRouter()
const projectId = route.params.projectId as string
const requirements = useRequirementsStore()

const isFormOpen = ref(false)

const filters = ref<RequirementFilters>({
  type: undefined,
  status: undefined,
  priority: undefined,
  page: 1,
  page_size: 20,
})

function load() {
  requirements.fetch(projectId, filters.value)
}

onMounted(load)
watch(filters, load)

function openRequirement(id: string) {
  router.push({ name: 'requirement-detail', params: { projectId, requirementId: id } })
}
</script>

<template>
  <section class="flex flex-1 flex-col min-h-0 h-full">
    <div class="mb-6 flex flex-shrink-0 items-center justify-between">
      <div class="flex items-center gap-2.5">
        <div class="rounded-lg bg-sky-100 p-1.5 text-sky-500 dark:bg-sky-500/10 dark:text-sky-400">
          <ListChecks class="h-4 w-4" />
        </div>
        <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Requirements</h2>
      </div>
      <button
        class="flex items-center gap-2 rounded-xl bg-sky-500 px-4 py-2.5 text-base font-medium text-white transition-all hover:bg-blue-500 hover:shadow-md active:scale-[0.98] cursor-pointer dark:bg-sky-600 dark:hover:bg-blue-600"
        @click="isFormOpen = true"
      >
        <Plus class="h-4 w-4" />
        New requirement
      </button>
    </div>

    <div class="mb-4 flex flex-shrink-0 flex-wrap items-center gap-3">
      <div class="flex items-center gap-1.5 text-sm text-slate-500 dark:text-slate-400">
        <SlidersHorizontal class="h-3.5 w-3.5" />
        Filters:
      </div>

      <div class="relative">
        <select
          v-model="filters.type"
          class="peer w-full appearance-none rounded-xl border border-blue-400/50 bg-blue-50/40 pl-3 pr-9 py-2 text-sm text-slate-800 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
        >
          <option :value="undefined">All types</option>
          <option value="BUSINESS">Business</option>
          <option value="USER">User</option>
          <option value="FUNCTIONAL">Functional</option>
          <option value="NONFUNCTIONAL">Non-functional</option>
          <option value="SYSTEM">System</option>
        </select>
        <ChevronDown
          class="pointer-events-none peer-focus:rotate-180 absolute transition-transform right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500 dark:text-slate-400"
        />
      </div>

      <div class="relative">
        <select
          v-model="filters.status"
          class="peer w-full appearance-none rounded-xl border border-blue-400/50 bg-blue-50/40 pl-3 pr-9 py-2 text-sm text-slate-800 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
        >
          <option :value="undefined">All statuses</option>
          <option value="DRAFT">Draft</option>
          <option value="REVIEWED">Reviewed</option>
          <option value="APPROVED">Approved</option>
          <option value="REJECTED">Rejected</option>
        </select>
        <ChevronDown
          class="pointer-events-none peer-focus:rotate-180 absolute transition-transform right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500 dark:text-slate-400"
        />
      </div>

      <div class="relative">
        <select
          v-model="filters.priority"
          class="peer w-full appearance-none rounded-xl border border-blue-400/50 bg-blue-50/40 pl-3 pr-9 py-2 text-sm text-slate-800 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
        >
          <option :value="undefined">All priorities</option>
          <option value="LOW">Low</option>
          <option value="MEDIUM">Medium</option>
          <option value="HIGH">High</option>
          <option value="CRITICAL">Critical</option>
        </select>
        <ChevronDown
          class="pointer-events-none peer-focus:rotate-180 absolute transition-transform right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500 dark:text-slate-400"
        />
      </div>
    </div>

    <div
      v-if="requirements.isLoading"
      class="flex flex-1 items-center justify-center gap-2 text-base text-slate-600 dark:text-slate-400"
    >
      <Loader2 class="h-4 w-4 animate-spin" />
      Loading…
    </div>

    <div
      v-else-if="requirements.items.length === 0"
      class="rounded-xl border border-blue-400/30 bg-blue-50/40 px-5 py-6 text-center text-base text-slate-600 dark:border-slate-700 dark:bg-slate-900/60 dark:text-slate-400"
    >
      No requirements found for these filters.
    </div>

    <div v-else class="flex-1 min-h-0 overflow-y-auto pr-1 scrollbar-thin">
      <ul class="space-y-2">
        <li
          v-for="r in requirements.items"
          :key="r.id"
          class="group flex cursor-pointer items-start justify-between gap-4 rounded-xl border border-blue-400/30 bg-white/70 p-4 backdrop-blur-sm transition-all hover:border-blue-400 hover:bg-blue-50/70 hover:shadow-md dark:border-slate-700 dark:bg-slate-900/60 dark:hover:border-slate-500 dark:hover:bg-slate-900/90"
          @click="openRequirement(r.id)"
        >
          <div class="min-w-0 flex-1">
            <span class="font-mono text-sm text-slate-400 dark:text-slate-500">{{ r.code }}</span>
            <p class="font-medium text-slate-900 dark:text-white">{{ r.title }}</p>
            <p
              v-if="!r.verifiable"
              class="mt-1 flex items-center gap-1 text-sm text-amber-600 dark:text-amber-400"
            >
              <AlertTriangle class="h-3.5 w-3.5 shrink-0" />
              Requirement is not verifiable
            </p>
          </div>
          <div class="flex shrink-0 items-center gap-2">
            <RequirementBadges :type="r.type" :status="r.status" :priority="r.priority" />
            <ChevronRight
              class="h-4 w-4 text-slate-400 transition-transform group-hover:translate-x-0.5 dark:text-slate-500"
            />
          </div>
        </li>
      </ul>
    </div>

    <p class="mt-4 flex-shrink-0 text-sm text-slate-500 dark:text-slate-400">
      Total: {{ requirements.total }}
    </p>

    <RequirementForm v-if="isFormOpen" @close="isFormOpen = false" />
  </section>
</template>
