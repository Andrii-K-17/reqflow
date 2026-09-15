<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStoriesStore } from '@/stores/userStories'
import UserStoryForm from '@/components/UserStoryForm.vue'
import { BookOpen, Plus, Loader2, Trash2, ListChecks, CheckSquare } from '@lucide/vue'

const route = useRoute()
const projectId = route.params.projectId as string
const userStories = useUserStoriesStore()
const isFormOpen = ref(false)

onMounted(() => userStories.fetch(projectId))

async function remove(id: string) {
  if (confirm('Delete this user story?')) {
    await userStories.remove(projectId, id)
  }
}
</script>

<template>
  <section class="flex flex-1 flex-col min-h-0 h-full">
    <div class="mb-6 flex flex-shrink-0 items-center justify-between">
      <div class="flex items-center gap-2.5">
        <div class="rounded-lg bg-sky-100 p-1.5 text-sky-500 dark:bg-sky-500/10 dark:text-sky-400">
          <BookOpen class="h-4 w-4" />
        </div>
        <h2 class="text-lg font-semibold text-slate-900 dark:text-white">User Stories</h2>
      </div>
      <button
        class="flex items-center gap-2 rounded-xl bg-sky-500 px-4 py-2.5 text-base font-medium text-white transition-all hover:bg-blue-500 hover:shadow-md active:scale-[0.98] cursor-pointer dark:bg-sky-600 dark:hover:bg-blue-600"
        @click="isFormOpen = true"
      >
        <Plus class="h-4 w-4" />
        New user story
      </button>
    </div>

    <div
      v-if="userStories.isLoading"
      class="flex flex-1 items-center justify-center gap-2 text-base text-slate-600 dark:text-slate-400"
    >
      <Loader2 class="h-4 w-4 animate-spin" />
      Loading…
    </div>

    <div
      v-else-if="userStories.items.length === 0"
      class="rounded-xl border border-blue-400/30 bg-blue-50/40 px-5 py-6 text-center text-base text-slate-600 dark:border-slate-700 dark:bg-slate-900/60 dark:text-slate-400"
    >
      No user stories created yet.
    </div>

    <div v-else class="flex-1 min-h-0 overflow-y-auto pr-1 scrollbar-thin">
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div
          v-for="story in userStories.items"
          :key="story.id"
          class="rounded-xl border border-blue-400/30 bg-white/70 p-4 backdrop-blur-sm transition-colors hover:bg-blue-50/40 dark:border-slate-700 dark:bg-slate-900/60 dark:hover:bg-slate-800/40"
        >
          <div class="mb-2 flex items-center justify-between">
            <span class="font-mono text-sm text-slate-400 dark:text-slate-500">{{
              story.code
            }}</span>
            <button
              class="inline-flex items-center gap-1 text-sm text-red-500 transition-colors hover:text-red-600 dark:text-red-400 dark:hover:text-red-300 hover:cursor-pointer"
              @click="remove(story.id)"
            >
              <Trash2 class="h-3.5 w-3.5" />
              Remove
            </button>
          </div>
          <p class="mb-3 text-sm text-slate-700 dark:text-slate-300">
            As a
            <strong class="text-slate-900 dark:text-white"> {{ story.role }}</strong>
            , I want to
            <strong class="text-slate-900 dark:text-white">{{ story.goal }}</strong>
            , so that
            <strong class="text-slate-900 dark:text-white">{{ story.benefit }}</strong>
            .
          </p>

          <div v-if="story.acceptance_criteria.length > 0">
            <span
              class="flex items-center gap-1.5 text-sm font-medium uppercase tracking-wider text-slate-400 dark:text-slate-500"
            >
              <ListChecks class="h-3.5 w-3.5" />
              Acceptance criteria
            </span>
            <ul class="mt-1.5 space-y-1">
              <li
                v-for="(c, i) in story.acceptance_criteria"
                :key="i"
                class="flex items-start gap-2 text-sm text-slate-700 dark:text-slate-300"
              >
                <CheckSquare
                  class="mt-0.5 h-3.5 w-3.5 shrink-0 text-slate-400 dark:text-slate-500"
                />
                <span>{{ c }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <UserStoryForm v-if="isFormOpen" @close="isFormOpen = false" />
  </section>
</template>
