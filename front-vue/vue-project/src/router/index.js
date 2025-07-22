import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../components/LoginView.vue';
import OrganizerDashboard from '../components/OrganizerDashboard.vue';
import SpeakerDashboard from '../components/SpeakerDashboard.vue';
import ListenerDashboard from '../components/ListenerDashboard.vue';
import MyPresentations from '../components/organizer/MyPresentations.vue';
import CreatePresentation from '../components/organizer/CreatePresentation.vue';
import OverallStats from '../components/organizer/OverallStats.vue';
import ListenerPerformance from '../components/organizer/ListenerPerformance.vue';

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/organizer/dashboard',
    name: 'OrganizerDashboard',
    component: OrganizerDashboard,
    children: [
      {
        path: 'presentations',
        name: 'MyPresentations',
        component: MyPresentations
      },
      {
        path: 'overall-stats',
        name: 'OverallStats',
        component: OverallStats
      },
      {
        path: 'listener-performance',
        name: 'ListenerPerformance',
        component: ListenerPerformance
      },
      {
        path: '',
        redirect: { name: 'MyPresentations' } // 默认子路由
      }
    ]
  },
  {
    path: '/speaker/dashboard',
    name: 'SpeakerDashboard',
    component: SpeakerDashboard,
    children: [
      {
        path: 'create',
        name: 'PresentationCreate',
        component: () => import('../components/speaker/PresentationCreate.vue')
      },
      {
        path: 'presentations',
        name: 'SpeakerPresentations',
        component: () => import('../components/speaker/MyPresentations.vue')
      },
      {
        path: 'files',
        name: 'FileManagement',
        component: () => import('../components/speaker/FileManagement.vue')
      },
      {
        path: 'quiz',
        name: 'QuizManagement',
        component: () => import('../components/speaker/QuizManagement.vue')
      },
      {
        path: 'stats',
        name: 'PresentationStats',
        component: () => import('../components/speaker/PresentationStats.vue')
      },
      {
        path: '',
        redirect: { name: 'PresentationCreate' }
      }
    ]
  },
  {
    path: '/listener/dashboard',
    name: 'ListenerDashboard',
    component: ListenerDashboard,
    children: [
      {
        path: 'available',
        name: 'AvailablePresentations',
        component: () => import('../components/listener/AvailablePresentations.vue')
      },
      {
        path: 'active',
        name: 'ActivePresentation',
        component: () => import('../components/listener/ActivePresentation.vue')
      },
      {
        path: 'presentations/:id/questions',
        name: 'QuizDiscussion',
        component: () => import('../components/listener/QuizDiscussion.vue')
      },
      {
        path: 'current-questions',
        redirect: to => {
          // 如果本地存储中有选中的演讲ID，则重定向到该演讲的问题页面
          const storedPresentation = localStorage.getItem('selectedPresentation');
          if (storedPresentation) {
            try {
              const parsedPresentation = JSON.parse(storedPresentation);
              return `/listener/dashboard/presentations/${parsedPresentation.id}/questions`;
            } catch (err) {
              console.error('Error parsing selected presentation:', err);
            }
          }
          // 否则重定向到活跃演讲页面
          return '/listener/dashboard/active';
        }
      },
      {
        path: 'files',
        name: 'FileDownload',
        component: () => import('../components/listener/FileDownload.vue')
      },
      {
        path: 'report',
        name: 'PersonalReport',
        component: () => import('../components/listener/PersonalReport.vue')
      },
      {
        path: '',
        redirect: { name: 'AvailablePresentations' }
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
