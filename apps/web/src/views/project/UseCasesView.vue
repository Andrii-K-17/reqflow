<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useUseCasesStore } from '@/stores/useCases'
import UseCaseForm from '@/components/UseCaseForm.vue'
import {
  Workflow,
  Plus,
  Loader2,
  Trash2,
  ChevronDown,
  Users,
  ListOrdered,
  GitFork,
} from '@lucide/vue'

const route = useRoute()
const projectId = route.params.projectId as string
const useCases = useUseCasesStore()
const isEditorOpen = ref(false)
const expandedId = ref<string | null>(null)

onMounted(() => useCases.fetch(projectId))

function toggle(id: string) {
  expandedId.value = expandedId.value === id ? null : id
}

async function remove(id: string) {
  if (confirm('Delete this use case?')) {
    await useCases.remove(projectId, id)
  }
}
</script>

<template>
  <section class="flex flex-1 flex-col min-h-0 h-full">
    <div class="mb-6 flex flex-shrink-0 items-center justify-between">
      <div class="flex items-center gap-2.5">
        <div class="rounded-lg bg-sky-100 p-1.5 text-sky-500 dark:bg-sky-500/10 dark:text-sky-400">
          <Workflow class="h-4 w-4" />
        </div>
        <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Use Cases</h2>
      </div>
      <button
        class="flex items-center gap-2 rounded-xl bg-sky-500 px-4 py-2.5 text-base font-medium text-white transition-all hover:bg-blue-500 hover:shadow-md active:scale-[0.98] cursor-pointer dark:bg-sky-600 dark:hover:bg-blue-600"
        @click="isEditorOpen = true"
      >
        <Plus class="h-4 w-4" />
        New use case
      </button>
    </div>

    <div
      v-if="useCases.isLoading"
      class="flex flex-1 items-center justify-center gap-2 text-base text-slate-600 dark:text-slate-400"
    >
      <Loader2 class="h-4 w-4 animate-spin" />
      Loading…
    </div>

    <div
      v-else-if="useCases.items.length === 0"
      class="rounded-xl border border-blue-400/30 bg-blue-50/40 px-5 py-6 text-center text-base text-slate-600 dark:border-slate-700 dark:bg-slate-900/60 dark:text-slate-400"
    >
      No use cases created yet.
    </div>

    <div v-else class="flex-1 min-h-0 overflow-y-auto pr-1 scrollbar-thin">
      <ul class="space-y-3">
        <li
          v-for="uc in useCases.items"
          :key="uc.id"
          class="overflow-hidden rounded-xl border border-blue-400/30 bg-white/70 backdrop-blur-sm transition-colors dark:border-slate-700 dark:bg-slate-900/60"
        >
          <div
            class="flex cursor-pointer items-center justify-between gap-4 p-4 hover:bg-blue-50/40 dark:hover:bg-slate-800/40"
            @click="toggle(uc.id)"
          >
            <div class="flex min-w-0 items-start gap-3">
              <ChevronDown
                class="mt-1 h-4 w-4 shrink-0 text-slate-500 transition-transform dark:text-slate-400"
                :class="{ '-rotate-90': expandedId !== uc.id }"
              />
              <div class="min-w-0">
                <span class="font-mono text-sm text-slate-400 dark:text-slate-500">{{
                  uc.code
                }}</span>
                <p class="font-medium text-slate-900 dark:text-white">{{ uc.title }}</p>
                <p class="flex items-center gap-1 text-sm text-slate-500 dark:text-slate-400">
                  <Users class="h-3 w-3 shrink-0" />
                  Actors: {{ uc.actors.join(', ') || '—' }}
                </p>
              </div>
            </div>
            <button
              class="inline-flex shrink-0 items-center gap-1 text-sm text-red-500 transition-colors hover:text-red-600 dark:text-red-400 dark:hover:text-red-300 hover:cursor-pointer"
              @click.stop="remove(uc.id)"
            >
              <Trash2 class="h-3.5 w-3.5" />
              Remove
            </button>
          </div>

          <div
            v-if="expandedId === uc.id"
            class="border-t border-blue-400/20 p-4 text-sm dark:border-slate-800"
          >
            <div v-if="uc.preconditions" class="mb-3">
              <span
                class="text-sm font-medium uppercase tracking-wider text-slate-400 dark:text-slate-500"
              >
                Preconditions
              </span>
              <p class="mt-0.5 text-slate-700 dark:text-slate-300">{{ uc.preconditions }}</p>
            </div>

            <div v-if="uc.postconditions" class="mb-4">
              <span
                class="text-sm font-medium uppercase tracking-wider text-slate-400 dark:text-slate-500"
              >
                Postconditions
              </span>
              <p class="mt-0.5 text-slate-700 dark:text-slate-300">{{ uc.postconditions }}</p>
            </div>

            <div class="mb-4">
              <span
                class="mb-1 flex items-center gap-1.5 text-sm font-medium uppercase tracking-wider text-slate-400 dark:text-slate-500"
              >
                <ListOrdered class="h-3.5 w-3.5" />
                Main flow
              </span>
              <ol class="ml-4 list-decimal space-y-0.5 text-slate-700 dark:text-slate-300">
                <li v-for="(step, i) in uc.main_flow" :key="i">{{ step }}</li>
              </ol>
            </div>

            <div
              v-for="flow in uc.alternative_flows"
              :key="flow.name"
              class="mb-2 rounded-xl bg-blue-50/60 p-3 dark:bg-slate-800/60"
            >
              <p
                class="mb-1 flex items-center gap-1.5 text-sm font-medium text-slate-700 dark:text-slate-300"
              >
                <GitFork class="h-3.5 w-3.5 shrink-0" />
                {{ flow.name }} — {{ flow.condition }}
              </p>
              <ol class="ml-4 list-decimal space-y-0.5 text-slate-600 dark:text-slate-400">
                <li v-for="(step, i) in flow.steps" :key="i">{{ step }}</li>
              </ol>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <UseCaseForm v-if="isEditorOpen" @close="isEditorOpen = false" />
  </section>
</template>
