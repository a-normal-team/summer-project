import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import OrganizerPresentationFormView from '../views/OrganizerPresentationFormView.vue'
import OrganizerPresentationManageView from '../views/OrganizerPresentationManageView.vue'
import SpeakerPresentationDetailView from '../views/SpeakerPresentationDetailView.vue'
import ListenerPresentationView from '../views/ListenerPresentationView.vue'
import ListenerPersonalReportView from '../views/ListenerPersonalReportView.vue'
import DiscussionView from '../views/DiscussionView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/organizer/presentations/create',
      name: 'create-presentation',
      component: OrganizerPresentationFormView
    },
    {
      path: '/organizer/presentations/:id/edit',
      name: 'edit-presentation',
      component: OrganizerPresentationFormView
    },
    {
      path: '/organizer/presentations/:id/manage',
      name: 'manage-presentation',
      component: OrganizerPresentationManageView
    },
    {
      path: '/speaker/presentations/:id',
      name: 'speaker-presentation-detail',
      component: SpeakerPresentationDetailView
    },
    {
      path: '/listener/presentations/:id',
      name: 'listener-presentation',
      component: ListenerPresentationView
    },
    {
      path: '/listener/presentations/:id/report',
      name: 'listener-personal-report',
      component: ListenerPersonalReportView
    },
    {
      path: '/discussion/questions/:id',
      name: 'question-discussion',
      component: DiscussionView
    }
  ]
})

export default router
