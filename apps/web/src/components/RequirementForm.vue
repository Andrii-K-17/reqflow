<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { z } from 'zod'
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useRequirementsStore } from '@/stores/requirements'
import {
  Layers,
  AlignLeft,
  Flag,
  CheckCircle2,
  FileText,
  Quote,
  AlertTriangle,
  Loader2,
  ChevronDown,
  X,
} from '@lucide/vue'

const emit = defineEmits<{ close: [] }>()

const route = useRoute()
const router = useRouter()
const projectId = route.params.projectId as string
const requirements = useRequirementsStore()

const schema = toTypedSchema(
  z.object({
    type: z.enum(['BUSINESS', 'USER', 'FUNCTIONAL', 'NONFUNCTIONAL', 'SYSTEM']),
    title: z.string().min(1, 'Please enter a requirement statement'),
    description: z.string().optional(),
    priority: z.enum(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']),
    verifiable: z.boolean(),
    rationale: z.string().optional(),
    source: z.string().optional(),
  }),
)

const { handleSubmit, defineField, errors } = useForm({
  validationSchema: schema,
  initialValues: { type: 'FUNCTIONAL', priority: 'MEDIUM', verifiable: true },
})

const [type, typeAttrs] = defineField('type')
const [title, titleAttrs] = defineField('title')
const [description, descriptionAttrs] = defineField('description')
const [priority, priorityAttrs] = defineField('priority')
const [verifiable] = defineField('verifiable')
const [rationale, rationaleAttrs] = defineField('rationale')
const [source, sourceAttrs] = defineField('source')

const isSubmitting = ref(false)

const verifiabilityHint = computed(() =>
  verifiable.value
    ? null
    : 'Non-verifiable requirements (e.g. "the system should be fast") should be rephrased with measurable criteria.',
)

const onSubmit = handleSubmit(async values => {
  isSubmitting.value = true
  try {
    const created = await requirements.create(projectId, values)
    emit('close')
    router.push({ name: 'requirement-detail', params: { projectId, requirementId: created.id } })
  } finally {
    isSubmitting.value = false
  }
})
</script>

<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm px-4"
    @click.self="emit('close')"
  >
    <form
      class="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-xl border border-blue-400/30 bg-white p-8 shadow-lg scrollbar-thin dark:border-slate-700 dark:bg-slate-900"
      @submit="onSubmit"
    >
      <div class="mb-6 flex items-center justify-between">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">New requirement</h2>
        <button
          type="button"
          class="p-1.5 rounded-lg text-slate-400 hover:text-sky-500 dark:text-slate-500 dark:hover:text-sky-400 hover:cursor-pointer transform transition-transform active:scale-110"
          aria-label="Close"
          @click="emit('close')"
        >
          <X class="h-5 w-5" />
        </button>
      </div>

      <div class="space-y-5">
        <div>
          <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
            Type
          </label>
          <div class="relative">
            <Layers
              class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600 dark:text-slate-400"
            />
            <select
              v-model="type"
              v-bind="typeAttrs"
              class="w-full appearance-none rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-9 text-md text-slate-800 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
            >
              <option value="BUSINESS">Business requirement</option>
              <option value="USER">User requirement</option>
              <option value="FUNCTIONAL">Functional requirement</option>
              <option value="NONFUNCTIONAL">Non-functional requirement</option>
              <option value="SYSTEM">System requirement</option>
            </select>
            <ChevronDown
              class="pointer-events-none absolute right-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600 dark:text-slate-400"
            />
          </div>
        </div>

        <div>
          <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
            Statement
          </label>
          <div class="relative">
            <AlignLeft
              class="pointer-events-none absolute left-3.5 top-3.5 h-4 w-4 text-slate-600 dark:text-slate-400"
            />
            <textarea
              v-model="title"
              v-bind="titleAttrs"
              rows="2"
              placeholder="The user shall be able to book an appointment with a doctor"
              class="w-full rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-md text-slate-800 placeholder:text-slate-500/80 outline-none transition-all resize-none focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
            />
          </div>
          <p
            v-if="errors.title"
            class="mt-1.5 flex items-center gap-1 text-xs text-red-500 dark:text-red-400"
          >
            <AlertTriangle class="h-3.5 w-3.5 shrink-0" />
            {{ errors.title }}
          </p>
        </div>

        <div>
          <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
            Description (optional)
          </label>
          <div class="relative">
            <FileText
              class="pointer-events-none absolute left-3.5 top-3.5 h-4 w-4 text-slate-600 dark:text-slate-400"
            />
            <textarea
              v-model="description"
              v-bind="descriptionAttrs"
              rows="3"
              placeholder="Add more context about this requirement"
              class="w-full rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-md text-slate-800 placeholder:text-slate-500/80 outline-none transition-all resize-none focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
            />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
              Priority
            </label>
            <div class="relative">
              <Flag
                class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600 dark:text-slate-400"
              />
              <select
                v-model="priority"
                v-bind="priorityAttrs"
                class="w-full appearance-none rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-9 text-md text-slate-800 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
              >
                <option value="LOW">Low</option>
                <option value="MEDIUM">Medium</option>
                <option value="HIGH">High</option>
                <option value="CRITICAL">Critical</option>
              </select>
              <ChevronDown
                class="pointer-events-none absolute right-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600 dark:text-slate-400"
              />
            </div>
          </div>

          <div class="flex items-end pb-3">
            <label
              class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300 hover:cursor-pointer"
            >
              <input
                v-model="verifiable"
                type="checkbox"
                class="h-4 w-4 rounded border-blue-400/50 text-sky-500 outline-none focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:focus:ring-blue-950/50"
              />
              <CheckCircle2 class="h-4 w-4 text-slate-500 dark:text-slate-400" />
              Requirement is verifiable
            </label>
          </div>
        </div>

        <p
          v-if="verifiabilityHint"
          class="flex items-start gap-1.5 rounded-xl bg-amber-50 px-3 py-2 text-xs text-amber-700 dark:bg-amber-500/10 dark:text-amber-400"
        >
          <AlertTriangle class="h-3.5 w-3.5 shrink-0 mt-0.5" />
          {{ verifiabilityHint }}
        </p>

        <div>
          <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
            Rationale (optional)
          </label>
          <div class="relative">
            <FileText
              class="pointer-events-none absolute left-3.5 top-3.5 h-4 w-4 text-slate-600 dark:text-slate-400"
            />
            <textarea
              v-model="rationale"
              v-bind="rationaleAttrs"
              rows="2"
              placeholder="Why is this requirement needed?"
              class="w-full rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-md text-slate-800 placeholder:text-slate-500/80 outline-none transition-all resize-none focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
            />
          </div>
        </div>

        <div>
          <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
            Source (optional)
          </label>
          <div class="relative">
            <Quote
              class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600 dark:text-slate-400"
            />
            <input
              v-model="source"
              v-bind="sourceAttrs"
              type="text"
              spellcheck="false"
              placeholder="Stakeholder interview, document..."
              class="w-full rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-md text-slate-800 placeholder:text-slate-500/80 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
            />
          </div>
        </div>
      </div>

      <div class="mt-6 flex justify-end gap-3">
        <button
          type="button"
          class="rounded-xl px-4 py-2.5 text-sm font-medium text-slate-600 transition-colors hover:text-blue-500 dark:text-slate-400 dark:hover:text-blue-400 hover:cursor-pointer"
          @click="emit('close')"
        >
          Cancel
        </button>
        <button
          type="submit"
          :disabled="isSubmitting"
          class="flex items-center justify-center gap-2 rounded-xl bg-sky-500 px-5 py-2.5 text-sm cursor-pointer font-medium text-white transition-all hover:bg-blue-500 hover:shadow-md active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60 dark:bg-sky-600 dark:hover:bg-blue-600"
        >
          <Loader2 v-if="isSubmitting" class="h-4 w-4 animate-spin" />
          {{ isSubmitting ? 'Creating...' : 'Create' }}
        </button>
      </div>
    </form>
  </div>
</template>
