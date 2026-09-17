<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useRequirementsStore } from '@/stores/requirements'
import { useBusinessGoalsStore } from '@/stores/businessGoals'
import { useUseCasesStore } from '@/stores/useCases'
import { useUserStoriesStore } from '@/stores/userStories'
import { useTraceLinksStore } from '@/stores/traceLinks'
import type { TraceEntityType, TraceRelation } from '@/types/trace-link'
import AppSelect from '@/components/ui/AppSelect.vue'
import type { SelectOption } from '@/components/ui/AppSelect.vue'
import {
  GitBranch,
  ArrowLeftRight,
  Layers,
  Link2,
  X,
  AlertCircle,
  Loader2,
  Plus,
} from '@lucide/vue'

const props = defineProps<{
  sourceType: TraceEntityType
  sourceId: string
}>()
const emit = defineEmits<{ close: [] }>()

const route = useRoute()
const projectId = route.params.projectId as string

const requirements = useRequirementsStore()
const goals = useBusinessGoalsStore()
const useCases = useUseCasesStore()
const userStories = useUserStoriesStore()
const traceLinks = useTraceLinksStore()

const form = ref({
  targetType: 'BUSINESS_GOAL' as TraceEntityType,
  targetId: '',
  relation: 'DERIVES_FROM' as TraceRelation,
  direction: 'outgoing' as 'outgoing' | 'incoming',
})

const errorMessage = ref<string | null>(null)
const isSubmitting = ref(false)
const isLoadingCandidates = ref(true)

const directionOptions: SelectOption[] = [
  { value: 'outgoing', label: 'This entity → other entity' },
  { value: 'incoming', label: 'Other entity → this entity' },
]

const targetTypeOptions: SelectOption[] = [
  { value: 'BUSINESS_GOAL', label: 'Business Goal' },
  { value: 'REQUIREMENT', label: 'Requirement' },
  { value: 'USE_CASE', label: 'Use Case' },
  { value: 'USER_STORY', label: 'User Story' },
]

const relationOptions: SelectOption[] = [
  { value: 'DERIVES_FROM', label: 'Derives from' },
  { value: 'SATISFIES', label: 'Satisfies' },
  { value: 'CONFLICTS_WITH', label: 'Conflicts with' },
]

const hasUnsavedChanges = computed(() => form.value.targetId !== '')

function requestClose() {
  if (hasUnsavedChanges.value && !confirm('You have unsaved changes. Discard this link?')) {
    return
  }
  emit('close')
}

onMounted(async () => {
  isLoadingCandidates.value = true
  try {
    await Promise.all([
      requirements.items.length ? Promise.resolve() : requirements.fetch(projectId),
      goals.items.length ? Promise.resolve() : goals.fetch(projectId),
      useCases.items.length ? Promise.resolve() : useCases.fetch(projectId),
      userStories.items.length ? Promise.resolve() : userStories.fetch(projectId),
    ])
  } finally {
    isLoadingCandidates.value = false
  }
})

const candidateOptions = computed<SelectOption[]>(() => {
  const raw = (() => {
    switch (form.value.targetType) {
      case 'BUSINESS_GOAL':
        return goals.items.map(g => ({ id: g.id, label: g.title }))
      case 'REQUIREMENT':
        return requirements.items
          .filter(r => !(props.sourceType === 'REQUIREMENT' && r.id === props.sourceId))
          .map(r => ({ id: r.id, label: `${r.code} — ${r.title}` }))
      case 'USE_CASE':
        return useCases.items.map(uc => ({ id: uc.id, label: `${uc.code} — ${uc.title}` }))
      case 'USER_STORY':
        return userStories.items.map(s => ({ id: s.id, label: `${s.code} — ${s.role}: ${s.goal}` }))
      default:
        return []
    }
  })()
  return raw.map(c => ({ value: c.id, label: c.label }))
})

async function submit() {
  if (!form.value.targetId) {
    errorMessage.value = 'Please select an entity to link'
    return
  }
  errorMessage.value = null

  const linkPayload =
    form.value.direction === 'outgoing'
      ? {
          from_type: props.sourceType,
          from_id: props.sourceId,
          to_type: form.value.targetType,
          to_id: form.value.targetId,
          relation: form.value.relation,
        }
      : {
          from_type: form.value.targetType,
          from_id: form.value.targetId,
          to_type: props.sourceType,
          to_id: props.sourceId,
          relation: form.value.relation,
        }

  isSubmitting.value = true
  try {
    await traceLinks.create(projectId, linkPayload)
    emit('close')
  } catch (err: any) {
    errorMessage.value = err?.response?.data?.detail || 'Failed to create the link'
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
      class="flex max-h-[90vh] w-full max-w-lg flex-col rounded-xl border border-blue-400/30 bg-white shadow-lg dark:border-slate-700 dark:bg-slate-900"
    >
      <div
        class="flex shrink-0 items-center justify-between border-b border-blue-400/20 px-8 py-6 dark:border-slate-800"
      >
        <h2 class="flex items-center gap-2.5 text-xl font-semibold text-slate-900 dark:text-white">
          <GitBranch class="h-5 w-5 text-sky-500 dark:text-sky-400" />
          Add traceability link
        </h2>
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
              Direction
            </label>
            <AppSelect
              v-model="form.direction"
              :options="directionOptions"
              :icon="ArrowLeftRight"
            />
          </div>

          <div>
            <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
              Target entity type
            </label>
            <AppSelect v-model="form.targetType" :options="targetTypeOptions" :icon="Layers" />
          </div>

          <div>
            <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
              Entity
            </label>
            <div
              v-if="isLoadingCandidates"
              class="flex items-center gap-2 rounded-xl border border-blue-400/50 bg-blue-50/40 px-4 py-3 text-sm text-slate-500 dark:border-slate-700 dark:bg-slate-900/90 dark:text-slate-400"
            >
              <Loader2 class="h-4 w-4 animate-spin" />
              Loading options…
            </div>
            <AppSelect
              v-else
              v-model="form.targetId"
              :options="candidateOptions"
              :icon="Link2"
              placeholder="Select…"
            />
            <p
              v-if="!isLoadingCandidates && candidateOptions.length === 0"
              class="mt-1.5 text-sm text-slate-400 dark:text-slate-500"
            >
              No entities of this type available.
            </p>
          </div>

          <div>
            <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
              Relation type
            </label>
            <AppSelect v-model="form.relation" :options="relationOptions" :icon="GitBranch" />
          </div>
        </div>

        <p
          v-if="errorMessage"
          class="mt-4 flex items-center gap-1 text-sm text-red-500 dark:text-red-400"
        >
          <AlertCircle class="h-3.5 w-3.5 shrink-0" />
          {{ errorMessage }}
        </p>
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
          <Plus v-else class="h-4 w-4" />
          {{ isSubmitting ? 'Adding...' : 'Add link' }}
        </button>
      </div>
    </div>
  </div>
</template>
