import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import OrganizationsView from "@/views/OrganizationsView.vue"
import OrganizerRegisterView from '@/views/OrganizerRegisterView.vue'

// Galimi būsimi view
// import ProfileView from "@/views/ProfileView.vue"
// import SettingsView from "@/views/SettingsView.vue"
// import CollectionView from "@/views/CollectionView.vue"

const routes = [
  { path: '/', component: HomeView ,  meta: { layout: 'default' }},
  { path: '/login', component: LoginView, meta: { layout: 'auth' } },
  { path: '/register', component: RegisterView, meta: { layout: 'auth' } },
  { path: '/organizations', component: OrganizationsView, meta: { layout: 'default' } },
  { path: '/register-organizer', component: OrganizerRegisterView, meta: { layout: 'auth' } },

  // 404 fallback – kai niekas neatitinka
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
