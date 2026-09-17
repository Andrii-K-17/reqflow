<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import mermaid from 'mermaid'
import { useDark } from '@vueuse/core'
import { AlertTriangle } from '@lucide/vue'

const props = defineProps<{ code: string }>()

const isDark = useDark()
const containerId = `mermaid-${Math.random().toString(36).slice(2, 10)}`
const svg = ref<string>('')
const error = ref<string | null>(null)

const lightThemeVariables = {
  fontFamily: 'inherit',
  primaryColor: '#e0f2fe',
  primaryTextColor: '#0c4a6e',
  primaryBorderColor: '#38bdf8',
  lineColor: '#8090a6',
  secondaryColor: '#e0f2fe',
  edgeLabelBackground: 'transparent',
}

const darkThemeVariables = {
  fontFamily: 'inherit',
  primaryColor: '#0c4a6e',
  primaryTextColor: '#e0f2fe',
  primaryBorderColor: '#0ea5e9',
  lineColor: '#64748b',
  secondaryColor: '#1e293b',
  edgeLabelBackground: 'transparent',
}

async function render() {
  error.value = null

  mermaid.initialize({
    startOnLoad: false,
    theme: 'base',
    themeVariables: isDark.value ? darkThemeVariables : lightThemeVariables,
    themeCSS: `
      .node rect, .node circle, .node polygon { rx: 8px; ry: 8px; }
      .edgeLabel rect,
      .edgeLabel .labelBkg {
        fill: transparent !important;
        background: transparent !important;
      }
      .edgeLabel { border-radius: 6px; padding: 2px 6px; }
    `,
  })

  if (!props.code.trim()) {
    svg.value = ''
    return
  }
  try {
    const result = await mermaid.render(containerId, props.code)
    svg.value = result.svg
  } catch {
    error.value = 'Failed to render the diagram.'
  }
}

onMounted(render)
watch(() => props.code, render)
watch(isDark, render)
</script>

<template>
  <div>
    <p
      v-if="error"
      class="flex items-center gap-1.5 rounded-xl bg-red-50 px-3 py-2 text-sm text-red-600 dark:bg-red-500/10 dark:text-red-400"
    >
      <AlertTriangle class="h-4 w-4 shrink-0" />
      {{ error }}
    </p>
    <div v-else class="mermaid-diagram flex justify-center" v-html="svg"></div>
  </div>
</template>
