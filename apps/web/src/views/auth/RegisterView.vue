<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { z } from 'zod'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const schema = toTypedSchema(
  z.object({
    full_name: z.string().min(1, 'Введіть імʼя'),
    email: z.string().email('Введіть коректний email'),
    password: z.string().min(8, 'Мінімум 8 символів'),
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

const onSubmit = handleSubmit(async values => {
  serverError.value = null
  isSubmitting.value = true
  try {
    await auth.register(values)
    router.push({ name: 'projects' })
  } catch {
    serverError.value = 'Такий email вже зареєстровано'
  } finally {
    isSubmitting.value = false
  }
})
</script>

<template>
  <main class="flex min-h-screen items-center justify-center bg-slate-50">
    <form
      class="w-full max-w-sm rounded-lg border border-slate-200 bg-white p-8 shadow-sm"
      @submit="onSubmit"
    >
      <h1 class="mb-6 text-xl font-semibold text-slate-900">Реєстрація в ReqFlow</h1>

      <label class="mb-1 block text-sm font-medium text-slate-700">Імʼя</label>
      <input
        v-model="fullName"
        v-bind="fullNameAttrs"
        type="text"
        class="mb-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
      />
      <p v-if="errors.full_name" class="mb-2 text-xs text-red-600">{{ errors.full_name }}</p>

      <label class="mb-1 block text-sm font-medium text-slate-700">Email</label>
      <input
        v-model="email"
        v-bind="emailAttrs"
        type="email"
        class="mb-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
      />
      <p v-if="errors.email" class="mb-2 text-xs text-red-600">{{ errors.email }}</p>

      <label class="mb-1 block text-sm font-medium text-slate-700">Пароль</label>
      <input
        v-model="password"
        v-bind="passwordAttrs"
        type="password"
        class="mb-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
      />
      <p v-if="errors.password" class="mb-2 text-xs text-red-600">{{ errors.password }}</p>

      <p v-if="serverError" class="mb-3 text-xs text-red-600">{{ serverError }}</p>

      <button
        type="submit"
        :disabled="isSubmitting"
        class="w-full rounded-md bg-slate-900 py-2 text-sm font-medium text-white disabled:opacity-50"
      >
        Зареєструватися
      </button>

      <p class="mt-4 text-center text-sm text-slate-600">
        Вже маєте акаунт?
        <router-link :to="{ name: 'login' }" class="font-medium text-slate-900 underline"
          >Увійти</router-link
        >
      </p>
    </form>
  </main>
</template>
