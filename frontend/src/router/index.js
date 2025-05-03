import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import OrganizationsView from "@/views/OrganizationsView.vue"
import OrganizerRegisterView from '@/views/OrganizerRegisterView.vue'
import EventListView from "@/views/EventListView.vue";
import GameCollectionView from "@/views/GameCollectionView.vue";
import EventDetailView from "@/views/EventDetailView.vue";

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
  { path: '/events', name: 'events', component: EventListView },
  { path: '/events/:id', name: 'event-detail', component: EventDetailView },
  { path: '/collection', name: 'Kolekcija', component: GameCollectionView },
  { path: '/organizations/:id', name: 'OrganizationDetail', component: () => import('../views/OrganizationDetailView.vue')
  },
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
