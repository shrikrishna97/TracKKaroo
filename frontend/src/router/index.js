import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import login from "../components/login.vue";
import register from "../components/registration.vue";
import forgot from "../components/forgotPass.vue"
import dashboard from "../components/dashboard.vue"
import createTracker from "../components/createTracker.vue"
import updateLog from "../components/updateLog.vue"
import updateTracker from "../components/updateTracker"
import addLog from "../components/AddLog.vue"

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  
  {
    path: "/login",
    name: "login",
    component: login,
  },
  {
    path: "/register",
    name: "register",
    component: register,
  },
  {
    path: "/forgot",
    name: "forgotPass",
    component: forgot,
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: dashboard,
  },
  {
    path: "/createTracker",
    name: "createTracker",
    component: createTracker,
  },
{
    path: "/dashboard/:id/updateTracker",
    name: "updateTracker",
    component: updateTracker,
  },
  {
    path: "/addLog/:id",
    name: "addLog",
    component: addLog,
  },
  {
    path: "/addLog/:id/updateLog",
    name: "updateLog",
    component: updateLog,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
