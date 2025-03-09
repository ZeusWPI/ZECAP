import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/HomeView.vue';
import MovieView from '@/views/MovieView.vue';

const routes = [
  // Home page
  { path: '/', component: Home, name: 'home' },

  // Movies
  {
    path: '/movies',
    children: [
      { path: ':movieId', 
        children: [
          { path: '', component: MovieView, name: 'movieDetail' }
        ]
      }
    ],
  },

  // Make sure to keep this as the last route, as it will default to the home page
  { path: '/:pathMatch(.*)*', redirect: { name: 'home' } },
];

const router = createRouter({
    async scrollBehavior() {
        return await new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    top: 0,
                    behavior: 'smooth',
                });
            }, 350);
        });
    },
    history: createWebHistory(),
    linkActiveClass: 'active',
    routes,
});


export default router;