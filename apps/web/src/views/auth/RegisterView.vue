<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { z } from 'zod'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { Mail, Lock, User, Loader2, AlertCircle, Eye, EyeOff, MoonIcon, SunIcon } from '@lucide/vue'
import { useDark, useToggle } from '@vueuse/core'

const isDark = useDark()
const toggleDark = useToggle(isDark)

const schema = toTypedSchema(
  z.object({
    full_name: z.string().min(1, 'Please enter your name'),
    email: z.email('Please enter a valid email'),
    password: z.string().min(8, 'Minimum 8 characters'),
  }),
)

const { handleSubmit, defineField, errors } = useForm({ validationSchema: schema })

const [fullName, fullNameAttrs] = defineField('full_name')
const [email, emailAttrs] = defineField('email')
const [password, passwordAttrs] = defineField('password')

const auth = useAuthStore()
const router = useRouter()
const serverError = ref<string | null>(null)
const isSubmitting = ref(false)
const showPassword = ref(false)

const onSubmit = handleSubmit(async values => {
  serverError.value = null
  isSubmitting.value = true
  try {
    await auth.register(values)
    router.push({ name: 'projects' })
  } catch {
    serverError.value = 'This email is already registered'
  } finally {
    isSubmitting.value = false
  }
})
</script>

<template>
  <main
    class="flex min-h-screen items-center justify-center bg-gradient-to-tr from-indigo-300/50 to-blue-200/50 px-4 dark:from-slate-950 dark:to-slate-900"
  >
    <button
      @click="toggleDark()"
      class="absolute top-4 right-4 z-10 p-2 rounded-xl text-slate-900 hover:text-sky-500 dark:text-slate-300 dark:hover:text-sky-400 hover:cursor-pointer transform transition-transform active:scale-110"
      aria-label="Toggle dark mode"
    >
      <SunIcon v-if="isDark" class="w-6 h-6" />
      <MoonIcon v-else class="w-6 h-6" />
    </button>

    <form class="w-full max-w-md p-10" @submit="onSubmit">
      <div class="mb-8 flex flex-col items-center text-center">
        <div class="flex items-center justify-center gap-3">
          <img src="/icon.svg" alt="ReqFlow logo" class="size-11" />
          <h1 class="text-5xl select-none font tracking-tight text-sky-500 dark:text-sky-400">
            ReqFlow
          </h1>
        </div>

        <p class="mt-3 text-base text-slate-700 dark:text-slate-300">
          Create an account to get started
        </p>
      </div>

      <div class="mb-5">
        <label class="mb-1.5 block text-base tracking-wider text-slate-700 dark:text-slate-300">
          Full name
        </label>
        <div class="relative">
          <User
            class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600 dark:text-slate-400"
          />
          <input
            v-model="fullName"
            v-bind="fullNameAttrs"
            type="text"
            spellcheck="false"
            placeholder="John Doe"
            class="w-full rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-base text-slate-800 placeholder:text-slate-500/80 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
          />
        </div>
        <p
          v-if="errors.full_name"
          class="mt-1.5 flex items-center gap-1 text-sm text-red-500 dark:text-red-400"
        >
          <AlertCircle class="h-3.5 w-3.5 shrink-0" />
          {{ errors.full_name }}
        </p>
      </div>

      <div class="mb-5">
        <label class="mb-1.5 block text-base tracking-wider text-slate-700 dark:text-slate-300">
          Email address
        </label>
        <div class="relative">
          <Mail
            class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600 dark:text-slate-400"
          />
          <input
            v-model="email"
            v-bind="emailAttrs"
            type="email"
            spellcheck="false"
            placeholder="you@example.com"
            class="w-full rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-base text-slate-800 placeholder:text-slate-500/80 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
          />
        </div>
        <p
          v-if="errors.email"
          class="mt-1.5 flex items-center gap-1 text-sm text-red-500 dark:text-red-400"
        >
          <AlertCircle class="h-3.5 w-3.5 shrink-0" />
          {{ errors.email }}
        </p>
      </div>

      <div class="mb-6">
        <label class="mb-1.5 block text-base tracking-wider text-slate-700 dark:text-slate-300">
          Password
        </label>
        <div class="relative">
          <Lock
            class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600 dark:text-slate-400"
          />
          <input
            v-model="password"
            v-bind="passwordAttrs"
            spellcheck="false"
            :type="showPassword ? 'text' : 'password'"
            placeholder="••••••••••"
            class="w-full rounded-xl border border-blue-400/50 bg-blue-50/40 py-3 pl-11 pr-4 text-base text-slate-800 placeholder:text-slate-500/80 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50"
          />
          <button
            type="button"
            tabindex="-1"
            class="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 transition-colors hover:text-blue-500 dark:text-slate-600 dark:hover:text-blue-400"
            @click="showPassword = !showPassword"
          >
            <EyeOff v-if="showPassword" class="h-4 w-4" />
            <Eye v-else class="h-4 w-4" />
          </button>
        </div>
        <p
          v-if="errors.password"
          class="mt-1.5 flex items-center gap-1 text-sm text-red-500 dark:text-red-400"
        >
          <AlertCircle class="h-3.5 w-3.5 shrink-0" />
          {{ errors.password }}
        </p>
      </div>

      <p
        v-if="serverError"
        class="mb-4 flex items-center gap-2 rounded-xl bg-red-50/60 px-4 py-3 text-sm text-red-600 backdrop-blur-sm dark:bg-red-500/10 dark:text-red-400"
      >
        <AlertCircle class="h-4 w-4 shrink-0" />
        {{ serverError }}
      </p>

      <button
        type="submit"
        :disabled="isSubmitting"
        class="flex w-full items-center justify-center gap-2 rounded-xl bg-sky-500 py-3 text-xl cursor-pointer font-medium text-white transition-all hover:bg-blue-500 hover:shadow-md active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60 dark:bg-sky-600 dark:hover:bg-blue-600"
      >
        <Loader2 v-if="isSubmitting" class="h-4 w-4 animate-spin" />
        {{ isSubmitting ? 'Creating account...' : 'Sign up' }}
      </button>

      <p class="mt-3 text-center text-base text-slate-700 dark:text-slate-300">
        Already have an account?
        <router-link
          :to="{ name: 'login' }"
          class="font-semibold text-blue-500 hover:text-blue-600 hover:underline dark:text-blue-500 dark:hover:text-blue-400"
        >
          Sign in
        </router-link>
      </p>
    </form>
  </main>
</template>
