<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
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
  MenuIcon,
  X,
  BookOpen,
} from '@lucide/vue'
import { useDark, useToggle } from '@vueuse/core'

const isDark = useDark()
const toggleDark = useToggle(isDark)

const route = useRoute()
const projectId = computed(() => route.params.projectId as string)
const projects = useProjectsStore()
const auth = useAuthStore()

const isSidebarOpen = ref(false)

const navItems = [
  { name: 'project-vision', label: 'Vision / Concept', icon: Lightbulb },
  { name: 'project-requirements', label: 'Requirements', icon: ListChecks },
  { name: 'project-use-cases', label: 'Use Cases', icon: Users },
  { name: 'project-user-stories', label: 'User Stories', icon: BookOpen },
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
      class="flex flex-shrink-0 items-center px-8 py-4 justify-between border-b border-blue-400/30 bg-white/70 backdrop-blur-sm dark:border-slate-800 dark:bg-slate-900/70"
    >
      <div
        class="flex items-center gap-2.5 lg:min-w-16 lg:border-r-0 border-r border-blue-400/30 dark:border-slate-800"
      >
        <button
          class="lg:hidden cursor-pointer text-slate-600 transition-colors hover:text-blue-500 dark:text-slate-400 dark:hover:text-blue-400"
          aria-label="Toggle navigation"
          @click="isSidebarOpen = !isSidebarOpen"
        >
          <X v-if="isSidebarOpen" class="h-5 w-5" />
          <MenuIcon v-else class="h-5 w-5" />
        </button>

        <router-link class="flex flex-row gap-2.5 items-center" :to="{ name: 'projects' }">
          <img src="/icon.svg" alt="ReqFlow logo" class="size-7 hidden lg:block" />
          <h1
            class="hidden lg:block text-2xl select-none font tracking-tight text-sky-500 dark:text-sky-400"
          >
            ReqFlow
          </h1>
        </router-link>
      </div>

      <div class="flex lg:hidden truncate items-center gap-2 px-5">
        <div class="rounded-lg bg-sky-100 px-1.5 text-sky-500 dark:bg-sky-900/30">
          <FolderKanban class="h-4 w-4" />
        </div>

        <h2 class="truncate text-slate-900 dark:text-white">
          {{ project?.name || 'Project' }}
        </h2>
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

        <span class="text-base text-slate-700 dark:text-slate-300">
          {{ auth.user?.full_name }}
        </span>

        <button
          class="flex items-center gap-1.5 text-base text-slate-600 transition-colors hover:text-blue-500 dark:text-slate-400 dark:hover:text-blue-400 hover:cursor-pointer"
          @click="auth.logout"
        >
          <LogOut class="h-4 w-4" />
          <span class="hidden lg:block">Log out</span>
        </button>
      </div>
    </header>

    <div class="relative flex flex-1 min-h-0">
      <div
        v-if="isSidebarOpen"
        class="absolute inset-0 z-30 bg-slate-900/40 lg:hidden"
        @click="isSidebarOpen = false"
      ></div>

      <aside
        class="absolute inset-y-0 left-0 z-40 flex w-64 flex-col overflow-hidden border-r border-blue-400/30 bg-white/95 backdrop-blur-sm transition-transform duration-300 dark:border-slate-800 dark:bg-slate-900/95 lg:relative lg:z-0 lg:translate-x-0 lg:bg-white/70 lg:dark:bg-slate-900/70"
        :class="isSidebarOpen ? 'translate-x-0' : '-translate-x-full'"
      >
        <div class="hidden border-b border-blue-400/30 px-4 py-4 dark:border-slate-800 lg:block">
          <div class="flex items-center gap-2">
            <div class="rounded-lg bg-sky-100 p-1.5 text-sky-500 dark:bg-sky-900/30">
              <FolderKanban class="h-4 w-4" />
            </div>

            <h2 class="truncate text-slate-900 dark:text-white">
              {{ project?.name || 'Project' }}
            </h2>
          </div>
        </div>

        <nav class="flex flex-1 min-h-0 flex-col gap-1 overflow-y-auto scrollbar-thin p-2">
          <router-link
            v-for="item in navItems"
            :key="item.name"
            :to="{ name: item.name, params: { projectId } }"
            class="flex items-center transition-all gap-2.5 rounded-xl px-3 py-2.5 text-base text-slate-700 hover:bg-blue-50/70 dark:text-slate-300 dark:hover:bg-slate-800/70"
            active-class="!bg-sky-500 !text-white"
            @click="isSidebarOpen = false"
          >
            <component :is="item.icon" class="h-4 w-4 shrink-0" />
            <span>{{ item.label }}</span>
          </router-link>
        </nav>

        <div class="flex border-t border-blue-400/30 px-4 py-4 dark:border-slate-800">
          <router-link
            :to="{ name: 'projects' }"
            class="flex items-center gap-1.5 text-base text-slate-600 transition-colors hover:text-blue-500 dark:text-slate-400 dark:hover:text-blue-400"
            @click="isSidebarOpen = false"
          >
            <ArrowLeft class="h-4 w-4 shrink-0" />
            All projects
          </router-link>
        </div>
      </aside>

      <section class="flex flex-1 flex-col p-8 overflow-auto">
        <router-view />
      </section>
    </div>
  </div>
</template>
