import { createRouter, createWebHistory } from 'vue-router'
import FeedView from '../views/FeedView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import SearchView from '../views/SearchView.vue'
import MessageView from '../views/MessageView.vue'
import ProfileView from '../views/ProfileView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'feed',
      component: FeedView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/message',
      name: 'message',
      component: MessageView
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView
    }
  ]
})

export default router
