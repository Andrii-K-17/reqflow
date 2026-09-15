<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useProjectsStore } from '@/stores/projects'
import { useAuthStore } from '@/stores/auth'
import CreateProjectModal from '@/components/CreateProjectModal.vue'
import { FolderKanban, Plus, LogOut, Loader2, MoonIcon, SunIcon } from '@lucide/vue'
import { useDark, useToggle } from '@vueuse/core'

const isDark = useDark()
const toggleDark = useToggle(isDark)

const projects = useProjectsStore()
const auth = useAuthStore()
const router = useRouter()
const isModalOpen = ref(false)

onMounted(() => {
  projects.fetchProjects()
  if (!auth.user) auth.fetchCurrentUser()
})

function openProject(projectId: string) {
  router.push({ name: 'project-vision', params: { projectId } })
}
</script>

<template>
  <main
    class="min-h-screen bg-gradient-to-tr from-indigo-300/50 to-blue-200/50 dark:from-slate-950 dark:to-slate-900"
  >
    <header
      class="flex items-center justify-between border-b border-blue-400/30 bg-white/70 px-8 py-4 backdrop-blur-sm dark:border-slate-800 dark:bg-slate-900/70"
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

    <div class="mx-auto max-w-6xl px-8 py-10">
      <div class="mb-6 flex items-center justify-between">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">My Projects</h2>
        <button
          class="flex items-center gap-2 rounded-xl bg-sky-500 px-4 py-2.5 text-base font-medium text-white transition-all hover:bg-blue-500 hover:shadow-md active:scale-[0.98] cursor-pointer dark:bg-sky-600 dark:hover:bg-blue-600"
          @click="isModalOpen = true"
        >
          <Plus class="h-4 w-4" />
          New Project
        </button>
      </div>

      <div
        v-if="projects.isLoading"
        class="flex items-center gap-2 text-base text-slate-600 dark:text-slate-400"
      >
        <Loader2 class="h-4 w-4 animate-spin" />
        Loading…
      </div>

      <div
        v-else-if="projects.projects.length === 0"
        class="rounded-xl border border-blue-400/30 bg-blue-50/40 px-5 py-6 text-center text-base text-slate-600 dark:border-slate-700 dark:bg-slate-900/60 dark:text-slate-400"
      >
        No projects yet. Create your first one.
      </div>

      <ul v-else class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <li
          v-for="project in projects.projects"
          :key="project.id"
          class="group cursor-pointer rounded-xl border border-blue-400/30 bg-blue-50/40 p-5 backdrop-blur-sm transition-all hover:border-blue-400 hover:bg-blue-50/70 hover:shadow-md dark:border-slate-700 dark:bg-slate-900/60 dark:hover:border-slate-500 dark:hover:bg-slate-900/90"
          @click="openProject(project.id)"
        >
          <div class="flex items-start gap-3">
            <div
              class="mt-0.5 rounded-lg bg-sky-100 p-2 text-sky-500 dark:bg-sky-500/10 dark:text-sky-400"
            >
              <FolderKanban class="h-4 w-4" />
            </div>
            <div class="min-w-0 flex-1">
              <h3 class="font-medium text-slate-900 dark:text-white">{{ project.name }}</h3>
              <p class="mt-1 line-clamp-2 text-base text-slate-600 dark:text-slate-400">
                {{ project.description || 'No description' }}
              </p>
              <span
                class="mt-3 inline-block rounded-full bg-sky-100 px-2 py-0.5 text-sm text-sky-600 dark:bg-sky-500/10 dark:text-sky-400"
              >
                {{ project.my_role }}
              </span>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <CreateProjectModal
      v-if="isModalOpen"
      @close="isModalOpen = false"
      @created="projects.fetchProjects"
    />
  </main>
</template>
