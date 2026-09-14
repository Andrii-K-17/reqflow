<script setup lang="ts">
import type { Priority, RequirementStatus, RequirementType } from '@/types/requirement'

defineProps<{
  type?: RequirementType
  status?: RequirementStatus
  priority?: Priority
}>()

const typeStyle: Record<RequirementType, string> = {
  BUSINESS: 'bg-purple-100 text-purple-700 dark:bg-purple-500/10 dark:text-purple-400',
  USER: 'bg-cyan-100 text-cyan-700 dark:bg-cyan-500/10 dark:text-cyan-400',
  FUNCTIONAL: 'bg-blue-100 text-blue-700 dark:bg-blue-500/10 dark:text-blue-400',
  NONFUNCTIONAL: 'bg-teal-100 text-teal-700 dark:bg-teal-500/10 dark:text-teal-400',
  SYSTEM: 'bg-indigo-100 text-indigo-700 dark:bg-indigo-500/10 dark:text-indigo-400',
}

const statusStyle: Record<RequirementStatus, string> = {
  DRAFT: 'bg-slate-100 text-slate-600 dark:bg-slate-500/10 dark:text-slate-400',
  REVIEWED: 'bg-amber-100 text-amber-700 dark:bg-amber-500/10 dark:text-amber-400',
  APPROVED: 'bg-green-100 text-green-700 dark:bg-green-500/10 dark:text-green-400',
  REJECTED: 'bg-red-100 text-red-700 dark:bg-red-500/10 dark:text-red-400',
}

const priorityStyle: Record<Priority, string> = {
  LOW: 'bg-slate-100 text-slate-600 dark:bg-slate-500/10 dark:text-slate-400',
  MEDIUM: 'bg-blue-100 text-blue-700 dark:bg-blue-500/10 dark:text-blue-400',
  HIGH: 'bg-amber-100 text-amber-700 dark:bg-amber-500/10 dark:text-amber-400',
  CRITICAL: 'bg-red-100 text-red-700 dark:bg-red-500/10 dark:text-red-400',
}
</script>

<template>
  <span v-if="type" class="rounded-full px-2 py-0.5 text-sm font-medium" :class="typeStyle[type]">
    {{ type }}
  </span>
  <span
    v-if="status"
    class="rounded-full px-2 py-0.5 text-sm font-medium"
    :class="statusStyle[status]"
  >
    {{ status }}
  </span>
  <span
    v-if="priority"
    class="rounded-full px-2 py-0.5 text-sm font-medium"
    :class="priorityStyle[priority]"
  >
    {{ priority }}
  </span>
</template>
