<script setup lang="ts">
import { computed, ref, useTemplateRef, watch, nextTick } from 'vue'
import { onClickOutside } from '@vueuse/core'
import { ChevronDown, Check, Component, type LucideIcon } from '@lucide/vue'

export interface SelectOption {
  value: string | undefined
  label: string
}

const props = withDefaults(
  defineProps<{
    modelValue: string | undefined
    options: SelectOption[]
    icon?: LucideIcon
    placeholder?: string
  }>(),
  {
    placeholder: 'Select…',
  },
)

const emit = defineEmits<{ 'update:modelValue': [value: string | undefined] }>()

const isOpen = ref(false)
const activeIndex = ref(-1)

const rootEl = useTemplateRef<HTMLElement>('rootEl')
const listEl = useTemplateRef<HTMLElement>('listEl')

const selectedOption = computed(() => props.options.find(o => o.value === props.modelValue))

onClickOutside(rootEl, () => {
  isOpen.value = false
})

function toggle() {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    activeIndex.value = props.options.findIndex(o => o.value === props.modelValue)
    nextTick(scrollActiveIntoView)
  }
}

function close() {
  isOpen.value = false
}

function select(option: SelectOption) {
  emit('update:modelValue', option.value)
  close()
}

function scrollActiveIntoView() {
  const list = listEl.value
  if (!list || activeIndex.value < 0) return
  const el = list.children[activeIndex.value] as HTMLElement | undefined
  el?.scrollIntoView({ block: 'nearest' })
}

function onKeydown(e: KeyboardEvent) {
  if (!isOpen.value) {
    if (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault()
      toggle()
    }
    return
  }

  switch (e.key) {
    case 'ArrowDown':
      e.preventDefault()
      activeIndex.value = Math.min(activeIndex.value + 1, props.options.length - 1)
      scrollActiveIntoView()
      break
    case 'ArrowUp':
      e.preventDefault()
      activeIndex.value = Math.max(activeIndex.value - 1, 0)
      scrollActiveIntoView()
      break
    case 'Enter':
      e.preventDefault()
      if (activeIndex.value >= 0) select(props.options[activeIndex.value])
      break
    case 'Escape':
      e.preventDefault()
      close()
      break
    case 'Tab':
      close()
      break
  }
}

watch(
  () => props.modelValue,
  () => nextTick(scrollActiveIntoView),
)
</script>

<template>
  <div ref="rootEl" class="relative h-[3.125rem]" @keydown="onKeydown">
    <button
      type="button"
      role="combobox"
      :aria-expanded="isOpen"
      aria-haspopup="listbox"
      class="flex w-full h-full items-center rounded-xl border border-blue-400/50 bg-blue-50/40 text-md text-slate-800 outline-none transition-all focus:border-blue-400 focus:bg-gray-100 focus:ring-2 focus:ring-blue-200/30 dark:border-slate-700 dark:bg-slate-900/90 dark:text-white dark:focus:border-blue-900/80 dark:focus:bg-slate-950/80 dark:focus:ring-blue-950/50 hover:cursor-pointer"
      :class="icon ? 'pl-11 pr-9' : 'pl-4 pr-9'"
      @click="toggle"
    >
      <component
        :is="icon"
        v-if="icon"
        class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600 dark:text-slate-400"
      />
      <span
        class="truncate text-left"
        :class="{ 'text-slate-500/80 dark:text-slate-500': !selectedOption }"
      >
        {{ selectedOption?.label ?? placeholder }}
      </span>
      <ChevronDown
        class="pointer-events-none absolute right-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600 transition-transform dark:text-slate-400"
        :class="{ 'rotate-180': isOpen }"
      />
    </button>

    <Transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 -translate-y-1 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <ul
        v-if="isOpen"
        ref="listEl"
        role="listbox"
        class="absolute z-35 mt-2 max-h-70 w-full overflow-y-auto rounded-xl border border-blue-400/30 bg-white p-1.5 shadow-lg scrollbar-thin dark:border-slate-700 dark:bg-slate-900"
      >
        <li
          v-for="(option, index) in options"
          :key="option.value ?? '__undefined__'"
          role="option"
          :aria-selected="option.value === modelValue"
          class="flex cursor-pointer items-center justify-between gap-2 rounded-lg px-3 py-2 text-sm text-slate-700 transition-colors dark:text-slate-300"
          :class="[
            index === activeIndex
              ? 'bg-blue-50/70 dark:bg-slate-800/70'
              : 'hover:bg-blue-50/70 dark:hover:bg-slate-800/70',
            option.value === modelValue && 'font-medium text-sky-600 dark:text-sky-400',
          ]"
          @click="select(option)"
          @mouseenter="activeIndex = index"
        >
          {{ option.label }}
          <Check v-if="option.value === modelValue" class="h-3.5 w-3.5 shrink-0" />
        </li>
      </ul>
    </Transition>
  </div>
</template>
