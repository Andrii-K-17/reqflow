<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useUseCasesStore } from '@/stores/useCases'
import type { AlternativeFlow } from '@/types/use-case'
import {
  Workflow,
  Users,
  AlignLeft,
  ListOrdered,
  GitFork,
  Plus,
  X,
  Trash2,
  Loader2,
  AlertCircle,
} from '@lucide/vue'

const emit = defineEmits<{ close: [] }>()

const route = useRoute()
const projectId = route.params.projectId as string
const useCases = useUseCasesStore()

const form = ref({
  title: '',
  actorsText: '',
  preconditions: '',
  postconditions: '',
  mainFlow: [''],
  altFlows: [] as AlternativeFlow[],
})

const isSubmitting = ref(false)
const titleError = ref<string | null>(null)

const hasUnsavedChanges = computed(() => {
  return (
    form.value.title.trim() !== '' ||
    form.value.actorsText.trim() !== '' ||
    form.value.preconditions.trim() !== '' ||
    form.value.postconditions.trim() !== '' ||
    form.value.mainFlow.some(step => step.trim() !== '') ||
    form.value.altFlows.length > 0
  )
})

function requestClose() {
  if (hasUnsavedChanges.value && !confirm('You have unsaved changes. Discard this use case?')) {
    return
  }
  emit('close')
}

function addMainStep() {
  form.value.mainFlow.push('')
}

function removeMainStep(index: number) {
  form.value.mainFlow.splice(index, 1)
}

function addAltFlow() {
  form.value.altFlows.push({ name: '', condition: '', steps: [''] })
}

function removeAltFlow(index: number) {
  form.value.altFlows.splice(index, 1)
}

function addAltStep(flowIndex: number) {
  form.value.altFlows[flowIndex].steps.push('')
}

function removeAltStep(flowIndex: number, stepIndex: number) {
  form.value.altFlows[flowIndex].steps.splice(stepIndex, 1)
}

async function submit() {
  if (!form.value.title.trim()) {
    titleError.value = 'Please enter a use case name'
    return
  }
  titleError.value = null
  isSubmitting.value = true
  try {
    await useCases.create(projectId, {
      title: form.value.title,
      actors: form.value.actorsText
        .split(',')
        .map(a => a.trim())
        .filter(Boolean),
      preconditions: form.value.preconditions || undefined,
      postconditions: form.value.postconditions || undefined,
      main_flow: form.value.mainFlow.filter(step => step.trim() !== ''),
      alternative_flows: form.value.altFlows
        .filter(flow => flow.name.trim() !== '')
        .map(flow => ({ ...flow, steps: flow.steps.filter(s => s.trim() !== '') })),
    })
    emit('close')
  } finally {
    isSubmitting.value = false
  }
}

const handleBeforeUnload = (event: BeforeUnloadEvent) => {
  if (hasUnsavedChanges.value) {
    event.preventDefault()
  }
}

onMounted(() => {
  window.addEventListener('beforeunload', handleBeforeUnload)
})

onUnmounted(() => {
  window.removeEventListener('beforeunload', handleBeforeUnload)
})
</script>

<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm px-4 py-8"
    @click.self="requestClose"
  >
    <div
      class="flex max-h-[90vh] w-full max-w-4xl flex-col rounded-xl border border-blue-400/30 bg-white shadow-lg dark:border-slate-700 dark:bg-slate-900"
    >
      <div
        class="flex shrink-0 items-center justify-between border-b border-blue-400/20 px-8 py-6 dark:border-slate-800"
      >
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">New use case</h2>
        <button
          type="button"
          class="p-1.5 rounded-lg text-slate-400 hover:text-sky-500 dark:text-slate-500 dark:hover:text-sky-400 hover:cursor-pointer transform transition-transform active:scale-110"
          aria-label="Close"
          @click="requestClose"
        >
          <X class="h-5 w-5" />
        </button>
      </div>

      <div class="flex-1 min-h-0 overflow-y-auto px-8 py-6 scrollbar-thin">
        <div class="space-y-5">
          <div>
            <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
              Title
            </label>
            <div class="relative">
              <Workflow
                class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600 dark:text-slate-400"
              />
              <input
                v-model="form.title"
                type="text"
                spellcheck="false"
                placeholder="Book an appointment"
                class="w-full rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-md text-slate-800 placeholder:text-slate-500/80 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
              />
            </div>
            <p
              v-if="titleError"
              class="mt-1.5 flex items-center gap-1 text-sm text-red-500 dark:text-red-400"
            >
              <AlertCircle class="h-3.5 w-3.5 shrink-0" />
              {{ titleError }}
            </p>
          </div>

          <div>
            <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
              Actors (comma-separated)
            </label>
            <div class="relative">
              <Users
                class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600 dark:text-slate-400"
              />
              <input
                v-model="form.actorsText"
                type="text"
                spellcheck="false"
                placeholder="Patient, Administrator"
                class="w-full rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-md text-slate-800 placeholder:text-slate-500/80 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
                Preconditions
              </label>
              <div class="relative">
                <AlignLeft
                  class="pointer-events-none absolute left-3.5 top-3.5 h-4 w-4 text-slate-600 dark:text-slate-400"
                />
                <textarea
                  v-model="form.preconditions"
                  rows="2"
                  class="w-full rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-sm text-slate-800 outline-none transition-all resize-none focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
                />
              </div>
            </div>
            <div>
              <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
                Postconditions
              </label>
              <div class="relative">
                <AlignLeft
                  class="pointer-events-none absolute left-3.5 top-3.5 h-4 w-4 text-slate-600 dark:text-slate-400"
                />
                <textarea
                  v-model="form.postconditions"
                  rows="2"
                  class="w-full rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-sm text-slate-800 outline-none transition-all resize-none focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
                />
              </div>
            </div>
          </div>

          <div>
            <div class="mb-2 flex items-center justify-between">
              <span
                class="flex items-center gap-1.5 text-md tracking-wider text-slate-700 dark:text-slate-300"
              >
                <ListOrdered class="h-4 w-4" />
                Main flow
              </span>
              <button
                type="button"
                class="flex items-center gap-1 text-sm text-slate-500 transition-colors hover:text-blue-500 dark:text-slate-400 dark:hover:text-blue-400 hover:cursor-pointer"
                @click="addMainStep"
              >
                <Plus class="h-3.5 w-3.5" />
                Step
              </button>
            </div>
            <div v-for="(_, i) in form.mainFlow" :key="i" class="mb-1.5 flex items-center gap-2">
              <span class="w-5 shrink-0 text-sm text-slate-400 dark:text-slate-500">
                {{ i + 1 }}.
              </span>
              <input
                v-model="form.mainFlow[i]"
                type="text"
                spellcheck="false"
                class="flex-1 rounded-xl border border-blue-400/50 bg-blue-50/40 px-3 py-2 text-sm text-slate-800 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
              />
              <button
                type="button"
                class="shrink-0 p-1 text-slate-400 transition-colors hover:text-red-500 dark:text-slate-500 dark:hover:text-red-400 hover:cursor-pointer"
                @click="removeMainStep(i)"
              >
                <X class="h-3.5 w-3.5" />
              </button>
            </div>
          </div>

          <div>
            <div class="mb-2 flex items-center justify-between">
              <span
                class="flex items-center gap-1.5 text-md tracking-wider text-slate-700 dark:text-slate-300"
              >
                <GitFork class="h-4 w-4" />
                Alternative flows
              </span>
              <button
                type="button"
                class="flex items-center gap-1 text-sm text-slate-500 transition-colors hover:text-blue-500 dark:text-slate-400 dark:hover:text-blue-400 hover:cursor-pointer"
                @click="addAltFlow"
              >
                <Plus class="h-3.5 w-3.5" />
                Alternative flow
              </button>
            </div>

            <div
              v-for="(flow, fi) in form.altFlows"
              :key="fi"
              class="mb-3 rounded-xl border border-blue-400/30 bg-blue-50/40 p-3 dark:border-slate-700 dark:bg-slate-900/60"
            >
              <div class="mb-2 flex items-center gap-2">
                <input
                  v-model="flow.name"
                  type="text"
                  spellcheck="false"
                  placeholder="Name (e.g. No available slots)"
                  class="flex-1 rounded-xl border border-blue-400/50 bg-white px-3 py-2 text-sm text-slate-800 outline-none transition-all focus:border-blue-400 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900 dark:text-white dark:focus:border-blue-900/80 dark:focus:ring-blue-950/50"
                />
                <button
                  type="button"
                  class="flex shrink-0 items-center gap-1 text-sm text-red-500 transition-colors hover:text-red-600 dark:text-red-400 dark:hover:text-red-300 hover:cursor-pointer"
                  @click="removeAltFlow(fi)"
                >
                  <Trash2 class="h-3.5 w-3.5" />
                  Remove flow
                </button>
              </div>
              <input
                v-model="flow.condition"
                type="text"
                spellcheck="false"
                placeholder="Condition"
                class="mb-2 w-full rounded-xl border border-blue-400/50 bg-white px-3 py-2 text-sm text-slate-800 outline-none transition-all focus:border-blue-400 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900 dark:text-white dark:focus:border-blue-900/80 dark:focus:ring-blue-950/50"
              />

              <div v-for="(_, si) in flow.steps" :key="si" class="mb-1.5 flex items-center gap-2">
                <span class="w-5 shrink-0 text-sm text-slate-400 dark:text-slate-500">
                  {{ si + 1 }}.
                </span>
                <input
                  v-model="flow.steps[si]"
                  type="text"
                  spellcheck="false"
                  class="flex-1 rounded-xl border border-blue-400/50 bg-white px-3 py-2 text-sm text-slate-800 outline-none transition-all focus:border-blue-400 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900 dark:text-white dark:focus:border-blue-900/80 dark:focus:ring-blue-950/50"
                />
                <button
                  type="button"
                  class="shrink-0 p-1 text-slate-400 transition-colors hover:text-red-500 dark:text-slate-500 dark:hover:text-red-400 hover:cursor-pointer"
                  @click="removeAltStep(fi, si)"
                >
                  <X class="h-3.5 w-3.5" />
                </button>
              </div>
              <button
                type="button"
                class="mt-1 flex items-center gap-1 text-sm text-slate-500 transition-colors hover:text-blue-500 dark:text-slate-400 dark:hover:text-blue-400 hover:cursor-pointer"
                @click="addAltStep(fi)"
              >
                <Plus class="h-3.5 w-3.5" />
                Step
              </button>
            </div>
          </div>
        </div>
      </div>

      <div
        class="flex shrink-0 justify-end gap-3 border-t border-blue-400/20 px-8 py-3 dark:border-slate-800"
      >
        <button
          type="button"
          class="rounded-xl px-4 py-2.5 text-sm font-medium text-slate-600 transition-colors hover:text-blue-500 dark:text-slate-400 dark:hover:text-blue-400 hover:cursor-pointer"
          @click="requestClose"
        >
          Cancel
        </button>
        <button
          type="button"
          :disabled="isSubmitting"
          class="flex items-center justify-center gap-2 rounded-xl bg-sky-500 px-5 py-2.5 text-sm cursor-pointer font-medium text-white transition-all hover:bg-blue-500 hover:shadow-md active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60 dark:bg-sky-600 dark:hover:bg-blue-600"
          @click="submit"
        >
          <Loader2 v-if="isSubmitting" class="h-4 w-4 animate-spin" />
          {{ isSubmitting ? 'Creating...' : 'Create' }}
        </button>
      </div>
    </div>
  </div>
</template>
