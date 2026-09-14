<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useStakeholdersStore } from '@/stores/stakeholders'
import { useBusinessGoalsStore } from '@/stores/businessGoals'
import StakeholderForm from '@/components/StakeholderForm.vue'
import BusinessGoalForm from '@/components/BusinessGoalForm.vue'
import { Users, Target, Plus, Loader2, Trash2, ChevronDown } from '@lucide/vue'

const route = useRoute()
const projectId = route.params.projectId as string
const stakeholders = useStakeholdersStore()
const goals = useBusinessGoalsStore()
const isFormOpen = ref(false)
const isGoalFormOpen = ref(false)

const isStakeholdersOpen = ref(true)
const isGoalsOpen = ref(true)

const categoryLabel: Record<string, string> = {
  PRIMARY: 'Primary',
  SECONDARY: 'Secondary',
  EXTERNAL: 'External',
}

const priorityStyle: Record<string, string> = {
  LOW: 'bg-slate-100 text-slate-600 dark:bg-slate-500/10 dark:text-slate-400',
  MEDIUM: 'bg-blue-100 text-blue-700 dark:bg-blue-500/10 dark:text-blue-400',
  HIGH: 'bg-amber-100 text-amber-700 dark:bg-amber-500/10 dark:text-amber-400',
  CRITICAL: 'bg-red-100 text-red-700 dark:bg-red-500/10 dark:text-red-400',
}

onMounted(() => {
  stakeholders.fetch(projectId)
  goals.fetch(projectId)
})

async function removeStakeholder(id: string) {
  if (confirm('Remove this stakeholder?')) {
    await stakeholders.remove(projectId, id)
  }
}

async function removeGoal(id: string) {
  if (confirm('Remove this business goal?')) {
    await goals.remove(projectId, id)
  }
}
</script>

<template>
  <section class="space-y-10">
    <div>
      <div class="mb-6 flex items-center justify-between">
        <button
          class="flex items-center gap-2.5 hover:cursor-pointer"
          @click="isStakeholdersOpen = !isStakeholdersOpen"
        >
          <div
            class="rounded-lg bg-sky-100 p-1.5 text-sky-500 dark:bg-sky-500/10 dark:text-sky-400"
          >
            <Users class="h-4 w-4" />
          </div>
          <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Stakeholders</h2>
          <ChevronDown
            class="h-4 w-4 text-slate-500 transition-transform dark:text-slate-400"
            :class="{ '-rotate-90': !isStakeholdersOpen }"
          />
        </button>
        <button
          class="flex items-center gap-2 rounded-xl bg-sky-500 px-4 py-2.5 text-base font-medium text-white transition-all hover:bg-blue-500 hover:shadow-md active:scale-[0.98] cursor-pointer dark:bg-sky-600 dark:hover:bg-blue-600"
          @click="isFormOpen = true"
        >
          <Plus class="h-4 w-4" />
          Add
        </button>
      </div>

      <div v-show="isStakeholdersOpen">
        <div
          v-if="stakeholders.isLoading"
          class="flex items-center justify-center gap-2 py-6 text-base text-slate-600 dark:text-slate-400"
        >
          <Loader2 class="h-4 w-4 animate-spin" />
          Loading…
        </div>

        <div
          v-else-if="stakeholders.items.length === 0"
          class="rounded-xl border border-blue-400/30 bg-blue-50/40 px-5 py-6 text-center text-base text-slate-600 dark:border-slate-700 dark:bg-slate-900/60 dark:text-slate-400"
        >
          No stakeholders defined yet.
        </div>

        <div
          v-else
          class="max-h-96 overflow-y-auto rounded-xl border border-blue-400/30 bg-white/70 backdrop-blur-sm scrollbar-thin dark:border-slate-700 dark:bg-slate-900/60"
        >
          <table class="w-full text-base table-auto border-collapse">
            <thead
              class="bg-blue-50/60 text-left shadow-sm text-xs uppercase tracking-wider text-slate-500 dark:bg-slate-900/80 dark:text-slate-400"
            >
              <tr>
                <th
                  class="sticky top-0 z-10 border-b border-blue-200/60 bg-blue-50/70 backdrop-blur-sm px-4 py-3 dark:border-slate-800 dark:bg-slate-900"
                >
                  Name
                </th>
                <th
                  class="sticky top-0 z-10 border-b border-blue-200/60 bg-blue-50/70 backdrop-blur-sm px-4 py-3 dark:border-slate-800 dark:bg-slate-900"
                >
                  Category
                </th>
                <th
                  class="sticky top-0 z-10 border-b border-blue-200/60 bg-blue-50/70 backdrop-blur-sm px-4 py-3 dark:border-slate-800 dark:bg-slate-900"
                >
                  Interest
                </th>
                <th
                  class="sticky top-0 z-10 border-b border-blue-200/60 bg-blue-50/70 backdrop-blur-sm px-4 py-3 dark:border-slate-800 dark:bg-slate-900"
                ></th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="s in stakeholders.items"
                :key="s.id"
                class="border-t border-blue-400/20 transition-colors hover:bg-blue-100/50 dark:border-slate-800 dark:hover:bg-slate-800/40"
              >
                <td class="px-4 py-3 font-medium text-slate-900 dark:text-white">{{ s.name }}</td>
                <td class="px-4 py-3">
                  <span
                    class="rounded-full bg-sky-100 px-2 py-0.5 text-xs text-sky-600 dark:bg-sky-500/10 dark:text-sky-400"
                  >
                    {{ categoryLabel[s.category] }}
                  </span>
                </td>
                <td class="px-4 py-3 text-slate-600 dark:text-slate-400">
                  {{ s.interest_description || '-' }}
                </td>
                <td class="px-4 py-3 text-right">
                  <button
                    class="inline-flex items-center gap-1 text-xs text-red-500 transition-colors hover:text-red-600 dark:text-red-400 dark:hover:text-red-300 hover:cursor-pointer"
                    @click="removeStakeholder(s.id)"
                  >
                    <Trash2 class="h-3.5 w-3.5" />
                    Remove
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div>
      <div class="mb-6 flex flex-shrink-0 items-center justify-between">
        <div class="flex items-center gap-2.5 cursor-pointer" @click="isGoalsOpen = !isGoalsOpen">
          <div
            class="rounded-lg bg-sky-100 p-1.5 text-sky-500 dark:bg-sky-500/10 dark:text-sky-400"
          >
            <Target class="h-4 w-4" />
          </div>
          <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Business Goals</h2>
          <ChevronDown
            class="h-4 w-4 text-slate-500 transition-transform dark:text-slate-400"
            :class="{ '-rotate-90': !isGoalsOpen }"
          />
        </div>
        <button
          class="flex items-center gap-2 rounded-xl bg-sky-500 px-4 py-2.5 text-base font-medium text-white transition-all hover:bg-blue-500 hover:shadow-md active:scale-[0.98] cursor-pointer dark:bg-sky-600 dark:hover:bg-blue-600"
          @click="isGoalFormOpen = true"
        >
          <Plus class="h-4 w-4" />
          Add
        </button>
      </div>

      <div v-show="isGoalsOpen">
        <div
          v-if="goals.isLoading"
          class="flex items-center justify-center gap-2 py-6 text-base text-slate-600 dark:text-slate-400"
        >
          <Loader2 class="h-4 w-4 animate-spin" />
          Loading…
        </div>

        <div
          v-else-if="goals.items.length === 0"
          class="rounded-xl border border-blue-400/30 bg-blue-50/40 px-5 py-6 text-center text-base text-slate-600 dark:border-slate-700 dark:bg-slate-900/60 dark:text-slate-400"
        >
          No business goals defined yet.
        </div>

        <div v-else class="max-h-96 space-y-3 overflow-y-auto pr-1 scrollbar-thin">
          <ul class="space-y-3">
            <li
              v-for="g in goals.items"
              :key="g.id"
              class="flex items-start justify-between rounded-xl border border-blue-400/30 bg-white/70 p-4 backdrop-blur-sm transition-colors hover:bg-blue-50/40 dark:border-slate-700 dark:bg-slate-900/60 dark:hover:bg-slate-800/40"
            >
              <div>
                <p class="font-medium text-slate-900 dark:text-white">{{ g.title }}</p>
                <p v-if="g.description" class="mt-1 text-base text-slate-600 dark:text-slate-400">
                  {{ g.description }}
                </p>
              </div>
              <div class="flex items-center gap-3">
                <span
                  class="rounded-full px-2 py-0.5 text-xs font-medium"
                  :class="priorityStyle[g.priority]"
                >
                  {{ g.priority }}
                </span>
                <button
                  class="inline-flex items-center gap-1 text-xs text-red-500 transition-colors hover:text-red-600 dark:text-red-400 dark:hover:text-red-300 hover:cursor-pointer"
                  @click="removeGoal(g.id)"
                >
                  <Trash2 class="h-3.5 w-3.5" />
                  Remove
                </button>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <StakeholderForm v-if="isFormOpen" @close="isFormOpen = false" />
    <BusinessGoalForm v-if="isGoalFormOpen" @close="isGoalFormOpen = false" />
  </section>
</template>
