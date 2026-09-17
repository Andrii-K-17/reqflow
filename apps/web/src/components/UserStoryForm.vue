<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStoriesStore } from '@/stores/userStories'
import {
  BookOpen,
  UserRound,
  Target,
  Gift,
  ListChecks,
  Plus,
  X,
  Loader2,
  AlertCircle,
} from '@lucide/vue'

const emit = defineEmits<{ close: [] }>()

const route = useRoute()
const projectId = route.params.projectId as string
const userStories = useUserStoriesStore()

const form = ref({
  role: '',
  goal: '',
  benefit: '',
  criteria: [''],
})

const isSubmitting = ref(false)
const error = ref<string | null>(null)

const hasUnsavedChanges = computed(() => {
  return (
    form.value.role.trim() !== '' ||
    form.value.goal.trim() !== '' ||
    form.value.benefit.trim() !== '' ||
    form.value.criteria.some(c => c.trim() !== '')
  )
})

function requestClose() {
  if (hasUnsavedChanges.value && !confirm('You have unsaved changes. Discard this user story?')) {
    return
  }
  emit('close')
}

function addCriterion() {
  form.value.criteria.push('')
}

function removeCriterion(index: number) {
  form.value.criteria.splice(index, 1)
}

async function submit() {
  if (!form.value.role.trim() || !form.value.goal.trim() || !form.value.benefit.trim()) {
    error.value = 'Please fill in role, goal and benefit'
    return
  }
  error.value = null
  isSubmitting.value = true
  try {
    await userStories.create(projectId, {
      role: form.value.role,
      goal: form.value.goal,
      benefit: form.value.benefit,
      acceptance_criteria: form.value.criteria.filter(c => c.trim() !== ''),
    })
    emit('close')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm px-4 py-8"
    @click.self="requestClose"
  >
    <div
      class="flex max-h-[90vh] w-full max-w-2xl flex-col rounded-xl border border-blue-400/30 bg-white shadow-lg dark:border-slate-700 dark:bg-slate-900"
    >
      <div
        class="flex shrink-0 items-center justify-between border-b border-blue-400/20 px-8 py-6 dark:border-slate-800"
      >
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">New user story</h2>
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
        <div
          class="mb-5 flex items-start gap-2.5 rounded-xl border border-blue-400/30 bg-blue-50/40 p-4 dark:border-slate-700 dark:bg-slate-900/60"
        >
          <BookOpen class="mt-0.5 h-4 w-4 shrink-0 text-sky-500 dark:text-sky-400" />
          <p class="text-sm text-slate-700 dark:text-slate-300">
            As a
            <strong class="text-slate-900 dark:text-white"> {{ form.role || '…' }} </strong>
            , I want to
            <strong class="text-slate-900 dark:text-white"> {{ form.goal || '…' }} </strong>
            , so that
            <strong class="text-slate-900 dark:text-white"> {{ form.benefit || '…' }} </strong>
          </p>
        </div>

        <div class="space-y-5">
          <div>
            <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
              Role (As a...)
            </label>
            <div class="relative">
              <UserRound
                class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600 dark:text-slate-400"
              />
              <input
                v-model="form.role"
                type="text"
                spellcheck="false"
                placeholder="Patient"
                class="w-full rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-md text-slate-800 placeholder:text-slate-500/80 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
              />
            </div>
          </div>

          <div>
            <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
              Goal (I want to...)
            </label>
            <div class="relative">
              <Target
                class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600 dark:text-slate-400"
              />
              <input
                v-model="form.goal"
                type="text"
                spellcheck="false"
                placeholder="book an appointment online"
                class="w-full rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-md text-slate-800 placeholder:text-slate-500/80 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
              />
            </div>
          </div>

          <div>
            <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
              Benefit (so that...)
            </label>
            <div class="relative">
              <Gift
                class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600 dark:text-slate-400"
              />
              <input
                v-model="form.benefit"
                type="text"
                spellcheck="false"
                placeholder="I don't have to call the clinic"
                class="w-full rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-md text-slate-800 placeholder:text-slate-500/80 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
              />
            </div>
          </div>

          <div>
            <div class="mb-2 flex items-center justify-between">
              <span
                class="flex items-center gap-1.5 text-md tracking-wider text-slate-700 dark:text-slate-300"
              >
                <ListChecks class="h-4 w-4" />
                Acceptance criteria
              </span>
              <button
                type="button"
                class="flex items-center gap-1 text-sm text-slate-500 transition-colors hover:text-blue-500 dark:text-slate-400 dark:hover:text-blue-400 hover:cursor-pointer"
                @click="addCriterion"
              >
                <Plus class="h-3.5 w-3.5" />
                Criterion
              </button>
            </div>
            <div v-for="(_, i) in form.criteria" :key="i" class="mb-1.5 flex items-center gap-2">
              <input
                v-model="form.criteria[i]"
                type="text"
                spellcheck="false"
                class="flex-1 rounded-xl border border-blue-400/50 bg-blue-50/40 px-3 py-2 text-sm text-slate-800 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
              />
              <button
                type="button"
                class="shrink-0 p-1 text-slate-400 transition-colors hover:text-red-500 dark:text-slate-500 dark:hover:text-red-400 hover:cursor-pointer"
                @click="removeCriterion(i)"
              >
                <X class="h-3.5 w-3.5" />
              </button>
            </div>
          </div>
        </div>

        <p v-if="error" class="mt-4 flex items-center gap-1 text-sm text-red-500 dark:text-red-400">
          <AlertCircle class="h-3.5 w-3.5 shrink-0" />
          {{ error }}
        </p>
      </div>

      <div
        class="flex shrink-0 justify-end gap-3 border-t border-blue-400/20 px-8 py-6 dark:border-slate-800"
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
