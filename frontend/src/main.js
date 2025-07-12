import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { createRouter, createWebHistory } from 'vue-router';
import { configure } from 'vee-validate';

import App from './App.vue';
import './style.css';

// Import views
import HomeView from './views/HomeView.vue';
import CandidateRegistrationView from './views/CandidateRegistrationView.vue';
import CandidateStatusView from './views/CandidateStatusView.vue';
import AdminDashboardView from './views/AdminDashboardView.vue';

// Configure Vee-Validate
configure({
  validateOnBlur: true,
  validateOnChange: false,
  validateOnInput: false,
  validateOnModelUpdate: false,
});

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/register',
      name: 'candidate-registration',
      component: CandidateRegistrationView,
    },
    {
      path: '/status',
      name: 'candidate-status',
      component: CandidateStatusView,
    },
    {
      path: '/admin',
      name: 'admin-dashboard',
      component: AdminDashboardView,
    },
  ],
});

// Create Pinia store
const pinia = createPinia();

// Create and mount app
const app = createApp(App);

app.use(pinia);
app.use(router);

app.mount('#app'); 