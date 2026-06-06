import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import LandingView from '../views/LandingView.vue'
import AuthVerifyView from '../views/AuthVerifyView.vue'
import DashboardView from '../views/DashboardView.vue'
import UploadView from '../views/UploadView.vue'
import ResultsView from '../views/ResultsView.vue'
import PricingView from '../views/PricingView.vue'
import TermsView from '../views/TermsView.vue'
import PrivacyView from '../views/PrivacyView.vue'
import RefundView from '../views/RefundView.vue'
import LoginView from '../views/LoginView.vue'

const routes = [
  {
    path: '/',
    name: 'landing',
    component: LandingView,
    meta: { requiresAuth: false },
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresAuth: false },
  },
  {
    path: '/auth/verify',
    name: 'auth-verify',
    component: AuthVerifyView,
    meta: { requiresAuth: false },
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: '/upload',
    name: 'upload',
    component: UploadView,
    meta: { requiresAuth: true },
  },
  {
    path: '/tasks/:id',
    name: 'results',
    component: ResultsView,
    meta: { requiresAuth: true },
  },
  {
    path: '/pricing',
    name: 'pricing',
    component: PricingView,
    meta: { requiresAuth: false },
  },
  {
    path: '/terms',
    name: 'terms',
    component: TermsView,
    meta: { requiresAuth: false },
  },
  {
    path: '/privacy',
    name: 'privacy',
    component: PrivacyView,
    meta: { requiresAuth: false },
  },
  {
    path: '/refunds',
    name: 'refunds',
    component: RefundView,
    meta: { requiresAuth: false },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'landing' }
  }
})

export default router
