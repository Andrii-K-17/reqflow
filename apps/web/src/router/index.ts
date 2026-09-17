import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginView.vue'),
      meta: { public: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/auth/RegisterView.vue'),
      meta: { public: true },
    },
    {
      path: '/projects',
      name: 'projects',
      component: () => import('@/views/ProjectsDashboardView.vue'),
    },
    {
      path: '/projects/:projectId',
      component: () => import('@/views/project/ProjectLayout.vue'),
      children: [
        {
          path: '',
          redirect: to => ({ name: 'project-vision', params: to.params }),
        },
        {
          path: 'vision',
          name: 'project-vision',
          component: () => import('@/views/project/VisionView.vue'),
        },
        {
          path: 'requirements',
          name: 'project-requirements',
          component: () => import('@/views/project/RequirementsView.vue'),
        },
        {
          path: 'requirements/:requirementId',
          name: 'requirement-detail',
          component: () => import('@/views/project/RequirementDetailView.vue'),
        },
        {
          path: 'use-cases',
          name: 'project-use-cases',
          component: () => import('@/views/project/UseCasesView.vue'),
        },
        {
          path: 'user-stories',
          name: 'project-user-stories',
          component: () => import('@/views/project/UserStoriesView.vue'),
        },
        {
          path: 'diagrams',
          name: 'project-diagrams',
          component: () => import('@/views/ProjectsDashboardView.vue'),
        },
        {
          path: 'traceability',
          name: 'project-traceability',
          component: () => import('@/views/project/TraceabilityMatrixView.vue'),
        },
        {
          path: 'documents',
          name: 'project-documents',
          component: () => import('@/views/ProjectsDashboardView.vue'),
        },
        {
          path: 'ai',
          name: 'project-ai',
          component: () => import('@/views/ProjectsDashboardView.vue'),
        },
      ],
    },
    {
      path: '/',
      redirect: '/projects',
    },
  ],
})

router.beforeEach(to => {
  const auth = useAuthStore()
  if (!to.meta.public && !auth.isAuthenticated) {
    return { name: 'login' }
  }
  return true
})

export default router
