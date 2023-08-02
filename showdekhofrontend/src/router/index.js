import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Show from '../views/Show.vue'
import Adashboard from '../views/Adashboard.vue'
import CreateMovie from '../views/CreateMovie.vue'
import EditMovie from '../views/EditMovie.vue'
import HomeTheatre from '../views/HomeTheatre.vue'
import Editheatre from '../views/Editheatre.vue'
import CreateTheatre from '../views/CreateTheatre.vue'
import Shows from '../views/Shows.vue'
import CreateShow from '../views/CreateShow.vue'
import EditShow from '../views/EditShow.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'loggin',
      component: Login
    },
    {
      path: '/dashboard',
      name: 'dash',
      component: Dashboard
    },
    {
      path:'/mshow/:id',
      name: 'Mshow',
      component: Show
    },
    {
      path:'/adashboard',
      component: Adashboard
    },
    {
      path:'/addmovie',
      component:CreateMovie
    },
    {
      path:'/editmovie/:id',
      name:'EditMovie',
      component:EditMovie
    },
    {
      path:'/theatres',
      component:HomeTheatre
    },
    {
      path:'/editheatre/:id',
      name:'Editheatre',
      component:Editheatre
    },
    {
      path:'/createtheatre',
      component:CreateTheatre
    },
    {
      path:'/shows',
      component:Shows
    },
    {
      path:'/createshow',
      component: CreateShow
    },
    {
      path:'/editshow/:id',
      component:EditShow,
      name:'EditShow'
    }
  ]
})

export default router
