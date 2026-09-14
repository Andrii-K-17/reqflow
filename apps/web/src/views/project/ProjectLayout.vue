<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useProjectsStore } from '@/stores/projects'
import { useAuthStore } from '@/stores/auth'
import {
  ArrowLeft,
  Lightbulb,
  ListChecks,
  Users,
  Workflow,
  GitBranch,
  FileText,
  Sparkles,
  FolderKanban,
  LogOut,
  MoonIcon,
  SunIcon,
} from '@lucide/vue'
import { useDark, useToggle } from '@vueuse/core'

const isDark = useDark()
const toggleDark = useToggle(isDark)

const route = useRoute()
const projectId = computed(() => route.params.projectId as string)
const projects = useProjectsStore()
const auth = useAuthStore()

const navItems = [
  { name: 'project-vision', label: 'Vision / Concept', icon: Lightbulb },
  { name: 'project-requirements', label: 'Requirements', icon: ListChecks },
  { name: 'project-use-cases', label: 'Use Cases', icon: Users },
  { name: 'project-diagrams', label: 'Diagrams', icon: Workflow },
  { name: 'project-traceability', label: 'Traceability', icon: GitBranch },
  { name: 'project-documents', label: 'Documents', icon: FileText },
  { name: 'project-ai', label: 'AI Assistant', icon: Sparkles },
]

const project = computed(() => projects.projects.find(p => p.id === projectId.value))

onMounted(() => {
  if (projects.projects.length === 0) projects.fetchProjects()
  if (!auth.user) auth.fetchCurrentUser()
})
</script>

<template>
  <div
    class="h-screen flex flex-col overflow-hidden bg-gradient-to-tr from-indigo-300/50 to-blue-200/50 dark:from-slate-950 dark:to-slate-900"
  >
    <header
      class="flex flex-shrink-0 items-center justify-between border-b border-blue-400/30 bg-white/70 px-8 py-4 backdrop-blur-sm dark:border-slate-800 dark:bg-slate-900/70"
    >
      <div class="flex items-center gap-2.5">
        <img src="/icon.svg" alt="ReqFlow logo" class="size-7" />
        <h1 class="text-2xl select-none font tracking-tight text-sky-500 dark:text-sky-400">
          ReqFlow
        </h1>
      </div>

      <div class="flex items-center gap-4">
        <button
          @click="toggleDark()"
          class="p-2 rounded-xl text-slate-900 hover:text-sky-500 dark:text-slate-300 dark:hover:text-sky-400 hover:cursor-pointer transform transition-transform active:scale-110"
          aria-label="Toggle dark mode"
        >
          <SunIcon v-if="isDark" class="w-5 h-5" />
          <MoonIcon v-else class="w-5 h-5" />
        </button>

        <span class="text-base text-slate-700 dark:text-slate-300">{{ auth.user?.full_name }}</span>

        <button
          class="flex items-center gap-1.5 text-base text-slate-600 transition-colors hover:text-blue-500 dark:text-slate-400 dark:hover:text-blue-400 hover:cursor-pointer"
          @click="auth.logout"
        >
          <LogOut class="h-4 w-4" />
          Log out
        </button>
      </div>
    </header>

    <div class="flex flex-1 min-h-0">
      <aside
        class="w-64 shrink-0 flex flex-col h-full border-r border-blue-400/30 bg-white/70 backdrop-blur-sm dark:border-slate-800 dark:bg-slate-900/70"
      >
        <div class="border-b border-blue-400/30 px-5 py-4 dark:border-slate-800 shrink-0">
          <router-link
            :to="{ name: 'projects' }"
            class="flex items-center gap-1.5 text-base text-slate-600 transition-colors hover:text-blue-500 dark:text-slate-400 dark:hover:text-blue-400"
          >
            <ArrowLeft class="h-3.5 w-3.5" />
            All projects
          </router-link>
          <div class="mt-2 flex items-center gap-2">
            <div
              class="rounded-lg bg-sky-100 p-1.5 text-sky-500 dark:bg-sky-500/10 dark:text-sky-400"
            >
              <FolderKanban class="h-4 w-4" />
            </div>
            <h2 class="truncate font-semibold text-slate-900 dark:text-white">
              {{ project?.name || 'Project' }}
            </h2>
          </div>
        </div>

        <nav class="flex flex-col gap-1 p-3 flex-1 min-h-0 overflow-y-auto scrollbar-thin">
          <router-link
            v-for="item in navItems"
            :key="item.name"
            :to="{ name: item.name, params: { projectId } }"
            class="flex items-center gap-2.5 rounded-xl px-3 py-2.5 text-base text-slate-700 transition-all hover:bg-blue-50/70 dark:text-slate-300 dark:hover:bg-slate-800/70"
            active-class="!bg-sky-500 !text-white dark:!bg-sky-600 hover:!bg-sky-500 dark:hover:!bg-sky-600"
          >
            <component :is="item.icon" class="h-4 w-4 shrink-0" />
            {{ item.label }}
          </router-link>
        </nav>
      </aside>

      <section class="flex flex-1 flex-col p-8 overflow-hidden">
        <router-view />
      </section>
    </div>
  </div>
</template>
