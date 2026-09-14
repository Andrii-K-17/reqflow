<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { z } from 'zod'
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useBusinessGoalsStore } from '@/stores/businessGoals'
import { Target, AlignLeft, Flag, Loader2, AlertCircle, X } from '@lucide/vue'

const emit = defineEmits<{ close: [] }>()

const schema = toTypedSchema(
  z.object({
    title: z.string().min(1, 'Please enter a goal statement'),
    description: z.string().optional(),
    priority: z.enum(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']),
  }),
)

const { handleSubmit, defineField, errors } = useForm({
  validationSchema: schema,
  initialValues: { priority: 'MEDIUM' },
})
const [title, titleAttrs] = defineField('title')
const [description, descriptionAttrs] = defineField('description')
const [priority, priorityAttrs] = defineField('priority')

const route = useRoute()
const goals = useBusinessGoalsStore()
const isSubmitting = ref(false)

const onSubmit = handleSubmit(async values => {
  isSubmitting.value = true
  try {
    await goals.create(route.params.projectId as string, values)
    emit('close')
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
      class="w-full max-w-md rounded-xl border border-blue-400/30 bg-white p-8 shadow-lg dark:border-slate-700 dark:bg-slate-900"
      @submit="onSubmit"
    >
      <div class="mb-6 flex items-center justify-between">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">New business goal</h2>
        <button
          type="button"
          class="p-1.5 rounded-lg text-slate-400 hover:text-sky-500 dark:text-slate-500 dark:hover:text-sky-400 hover:cursor-pointer transform transition-transform active:scale-110"
          aria-label="Close"
          @click="emit('close')"
        >
          <X class="h-5 w-5" />
        </button>
      </div>

      <div class="mb-5">
        <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
          Goal statement
        </label>
        <div class="relative">
          <Target
            class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600 dark:text-slate-400"
          />
          <input
            v-model="title"
            v-bind="titleAttrs"
            type="text"
            spellcheck="false"
            placeholder="Goal"
            class="w-full rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-md text-slate-800 placeholder:text-slate-500/80 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
          />
        </div>
        <p
          v-if="errors.title"
          class="mt-1.5 flex items-center gap-1 text-xs text-red-500 dark:text-red-400"
        >
          <AlertCircle class="h-3.5 w-3.5 shrink-0" />
          {{ errors.title }}
        </p>
      </div>

      <div class="mb-5">
        <label class="mb-1.5 block text-md tracking-wider text-slate-700 dark:text-slate-300">
          Description (optional)
        </label>
        <div class="relative">
          <AlignLeft
            class="pointer-events-none absolute left-3.5 top-3.5 h-4 w-4 text-slate-600 dark:text-slate-400"
          />
          <textarea
            v-model="description"
            v-bind="descriptionAttrs"
            rows="3"
            placeholder="Add more context about this goal"
            class="w-full rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-md text-slate-800 placeholder:text-slate-500/80 outline-none transition-all resize-none focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
          />
        </div>
      </div>

      <div class="mb-6">
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
            class="w-full appearance-none rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-md text-slate-800 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
          >
            <option value="LOW">Low</option>
            <option value="MEDIUM">Medium</option>
            <option value="HIGH">High</option>
            <option value="CRITICAL">Critical</option>
          </select>
        </div>
      </div>

      <div class="flex justify-end gap-3">
        <button
          type="button"
          class="rounded-xl px-4 py-2.5 text-base font-medium text-slate-600 transition-colors hover:text-blue-500 dark:text-slate-400 dark:hover:text-blue-400 hover:cursor-pointer"
          @click="emit('close')"
        >
          Cancel
        </button>
        <button
          type="submit"
          :disabled="isSubmitting"
          class="flex items-center justify-center gap-2 rounded-xl bg-sky-500 px-5 py-2.5 text-base cursor-pointer font-medium text-white transition-all hover:bg-blue-500 hover:shadow-md active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60 dark:bg-sky-600 dark:hover:bg-blue-600"
        >
          <Loader2 v-if="isSubmitting" class="h-4 w-4 animate-spin" />
          {{ isSubmitting ? 'Adding...' : 'Add' }}
        </button>
      </div>
    </form>
  </div>
</template>
