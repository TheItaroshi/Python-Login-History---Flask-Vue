import Vue from 'vue'
import VueRouter from 'vue-router'
import Profile from "../components/Profile";
import Home from "../components/Home";

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  { path: '/profile',
    name: 'Profile',
    component: Profile },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router