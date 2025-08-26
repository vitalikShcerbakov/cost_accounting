import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: () => import('pages/LoginComp.vue'),
    meta: { verboseName: 'Логин', requiresAuth: false }
  },
  {
    path: '',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'index',
        component: () => import('pages/IndexPage.vue'),
        meta: { verboseName: 'Главная', requiresAuth: true },
      },
      {
        path: 'categories/',
        name: 'categories',
        component: () => import('pages/CategoriesPage.vue'),
        meta: { verboseName: 'Категории', requiresAuth: true },
      },
      {
        path: 'expenses/',
        name: 'expenses',
        component: () => import('pages/ExpensesPage.vue'),
        meta: { verboseName: 'Траты', requiresAuth: true },
      },
      {
        path: 'incomes/',
        name: 'incomes',
        component: () => import('pages/IncomesPage.vue'),
        meta: { verboseName: 'Доходы', requiresAuth: true },
      },
      {
        path: 'reports/',
        name: 'reports',
        component: () => import('pages/ReportsPage.vue'),
        meta: { verboseName: 'Отчёты', requiresAuth: true },
      },
    ],
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
    meta: { verboseName: '' },
  },
];
export default routes;
