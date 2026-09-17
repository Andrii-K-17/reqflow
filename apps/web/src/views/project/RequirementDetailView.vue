<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useRequirementsStore } from '@/stores/requirements'
import { useTraceLinksStore } from '@/stores/traceLinks'
import RequirementBadges from '@/components/RequirementBadges.vue'
import LinkEntityModal from '@/components/LinkEntityModal.vue'
import type { Requirement, RequirementStatus } from '@/types/requirement'
import {
  ArrowLeft,
  AlertTriangle,
  FileText,
  Lightbulb,
  Quote,
  GitBranch,
  Plus,
  Link2,
  Trash2,
  Loader2,
  CheckCircle2,
  XCircle,
  ArrowRight,
  Minus,
} from '@lucide/vue'

const route = useRoute()
const router = useRouter()
const projectId = route.params.projectId as string
const requirementId = route.params.requirementId as string

const requirements = useRequirementsStore()
const traceLinks = useTraceLinksStore()
const requirement = ref<Requirement | null>(null)
const isLoading = ref(true)
const isLinkModalOpen = ref(false)

const statusOptions: RequirementStatus[] = ['DRAFT', 'REVIEWED', 'APPROVED', 'REJECTED']

async function load() {
  isLoading.value = true
  try {
    requirement.value = await requirements.fetchOne(projectId, requirementId)
    if (traceLinks.items.length === 0) await traceLinks.fetch(projectId)
  } finally {
    isLoading.value = false
  }
}

onMounted(load)

async function changeStatus(status: RequirementStatus) {
  if (!requirement.value) return
  requirement.value = await requirements.update(projectId, requirementId, { status })
}

async function toggleVerifiable() {
  if (!requirement.value) return
  requirement.value = await requirements.update(projectId, requirementId, {
    verifiable: !requirement.value.verifiable,
  })
}

async function removeRequirement() {
  if (!confirm('Delete this requirement?')) return
  await requirements.remove(projectId, requirementId)
  router.push({ name: 'project-requirements', params: { projectId } })
}

async function removeLink(linkId: string) {
  if (!confirm('Delete this link?')) return
  await traceLinks.remove(projectId, linkId)
}
</script>

<template>
  <section
    v-if="isLoading"
    class="flex items-center gap-2 text-base text-slate-600 dark:text-slate-400"
  >
    <Loader2 class="h-4 w-4 animate-spin" />
    Loading…
  </section>

  <section v-else-if="requirement" class="max-w-6xl">
    <router-link
      :to="{ name: 'project-requirements', params: { projectId } }"
      class="mb-3 flex items-center gap-1.5 text-sm text-slate-600 transition-colors hover:text-blue-500 dark:text-slate-400 dark:hover:text-blue-400"
    >
      <ArrowLeft class="h-3.5 w-3.5" />
      All requirements
    </router-link>

    <div class="mb-4 flex items-start justify-between gap-4">
      <div>
        <span class="font-mono text-sm text-slate-400 dark:text-slate-500">
          {{ requirement.code }}
        </span>
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">
          {{ requirement.title }}
        </h2>
      </div>
      <div class="flex shrink-0 gap-2">
        <RequirementBadges
          :type="requirement.type"
          :status="requirement.status"
          :priority="requirement.priority"
        />
      </div>
    </div>

    <p
      v-if="!requirement.verifiable"
      class="mb-4 flex items-start gap-1.5 rounded-xl bg-amber-50 px-3 py-2 text-sm text-amber-700 dark:bg-amber-500/10 dark:text-amber-400"
    >
      <AlertTriangle class="h-4 w-4 shrink-0 mt-0.5" />
      This requirement is marked as non-verifiable. Consider rephrasing it with measurable criteria.
    </p>

    <div
      class="space-y-5 rounded-xl border border-blue-400/30 bg-white/70 p-6 backdrop-blur-sm dark:border-slate-700 dark:bg-slate-900/60"
    >
      <div v-if="requirement.description">
        <h3
          class="mb-1.5 flex items-center gap-1.5 text-sm font-medium uppercase tracking-wider text-slate-400 dark:text-slate-500"
        >
          <FileText class="h-3.5 w-3.5" />
          Description
        </h3>
        <p class="text-sm text-slate-700 dark:text-slate-300">{{ requirement.description }}</p>
      </div>

      <div v-if="requirement.rationale">
        <h3
          class="mb-1.5 flex items-center gap-1.5 text-sm font-medium uppercase tracking-wider text-slate-400 dark:text-slate-500"
        >
          <Lightbulb class="h-3.5 w-3.5" />
          Rationale
        </h3>
        <p class="text-sm text-slate-700 dark:text-slate-300">{{ requirement.rationale }}</p>
      </div>

      <div v-if="requirement.source">
        <h3
          class="mb-1.5 flex items-center gap-1.5 text-sm font-medium uppercase tracking-wider text-slate-400 dark:text-slate-500"
        >
          <Quote class="h-3.5 w-3.5" />
          Source
        </h3>
        <p class="text-sm text-slate-700 dark:text-slate-300">{{ requirement.source }}</p>
      </div>

      <div>
        <div class="mb-2 flex flex-col items-start">
          <h3
            class="flex items-center gap-1.5 text-sm font-medium uppercase tracking-wider text-slate-400 dark:text-slate-500"
          >
            <GitBranch class="h-3.5 w-3.5" />
            Traceability
          </h3>

          <p
            v-if="traceLinks.linksFor('REQUIREMENT', requirement.id).length === 0"
            class="text-sm text-slate-400 dark:text-slate-500"
          >
            No links yet.
          </p>
          <ul v-else class="space-y-1.5">
            <li
              v-for="link in traceLinks.linksFor('REQUIREMENT', requirement.id)"
              :key="link.id"
              class="flex items-center justify-between gap-2 rounded-xl bg-blue-50/60 px-3 py-2 text-sm text-slate-600 dark:bg-slate-800/60 dark:text-slate-400"
            >
              <span class="flex items-center gap-1.5">
                <Link2 class="h-3.5 w-3.5 shrink-0 text-slate-400 dark:text-slate-500" />

                <span class="font-medium text-slate-800 dark:text-slate-200">
                  {{ link.from_type }}
                </span>

                <Minus class="h-3 w-3 shrink-0 text-slate-400 dark:text-slate-500" />

                <span class="text-xs text-slate-500 dark:text-slate-400">
                  {{ link.relation }}
                </span>

                <ArrowRight class="h-3.5 w-3.5 shrink-0 text-slate-400 dark:text-slate-500" />

                <span class="font-medium text-slate-800 dark:text-slate-200">
                  {{ link.to_type }}
                </span>
              </span>
              <button
                class="flex items-center gap-1 text-red-500 transition-colors hover:text-red-600 dark:text-red-400 dark:hover:text-red-300 hover:cursor-pointer"
                @click="removeLink(link.id)"
              >
                <Trash2 class="h-3.5 w-3.5" />
                Remove
              </button>
            </li>
          </ul>
        </div>
        <button
          class="flex items-center px-3 gap-1 text-sm text-slate-500 transition-colors hover:text-blue-500 dark:text-slate-400 dark:hover:text-blue-400 hover:cursor-pointer"
          @click="isLinkModalOpen = true"
        >
          <Plus class="h-3.5 w-3.5" />
          Add link
        </button>
      </div>
    </div>

    <div class="mt-5 flex flex-wrap items-center gap-2">
      <span class="text-sm text-slate-500 dark:text-slate-400">Change status:</span>
      <button
        v-for="s in statusOptions"
        :key="s"
        class="rounded-xl border border-blue-400/50 px-2.5 py-1 text-sm text-slate-700 transition-colors hover:bg-blue-50/70 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800/70 hover:cursor-pointer"
        :class="{
          '!border-sky-500 !bg-sky-500 !text-white hover:!bg-sky-500 dark:!border-sky-600 dark:!bg-sky-600 dark:hover:!bg-sky-600':
            requirement.status === s,
        }"
        @click="changeStatus(s)"
      >
        {{ s }}
      </button>

      <span class="mx-2 h-4 w-px bg-blue-400/30 dark:bg-slate-700"></span>

      <button
        class="flex items-center gap-1.5 rounded-xl border border-blue-400/50 px-2.5 py-1 text-sm text-slate-700 transition-colors hover:bg-blue-50/70 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800/70 hover:cursor-pointer"
        @click="toggleVerifiable"
      >
        <XCircle v-if="requirement.verifiable" class="h-3.5 w-3.5" />
        <CheckCircle2 v-else class="h-3.5 w-3.5" />
        {{ requirement.verifiable ? 'Mark as non-verifiable' : 'Mark as verifiable' }}
      </button>

      <button
        class="ml-auto flex items-center gap-1 text-sm text-red-500 transition-colors hover:text-red-600 dark:text-red-400 dark:hover:text-red-300 hover:cursor-pointer"
        @click="removeRequirement"
      >
        <Trash2 class="h-3.5 w-3.5" />
        Delete requirement
      </button>
    </div>

    <LinkEntityModal
      v-if="isLinkModalOpen"
      source-type="REQUIREMENT"
      :source-id="requirement.id"
      @close="isLinkModalOpen = false"
    />
  </section>
</template>
