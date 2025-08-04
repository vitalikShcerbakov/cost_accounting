import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'index',
        component: () => import('pages/IndexPage.vue'),
        meta: { verboseName: 'Главная' },
      },
      {
        path: 'categories/',
        name: 'categories',
        component: () => import('pages/CategoriesPage.vue'),
        meta: { verboseName: 'Категории' },
      },
      {
        path: 'expenses/',
        name: 'expenses',
        component: () => import('pages/ExpensesPage.vue'),
        meta: { verboseName: 'Траты' },
      },
      {
        path: 'incomes/',
        name: 'incomes',
        component: () => import('pages/IncomesPage.vue'),
        meta: { verboseName: 'Доходы' },
      },
      {
        path: 'reports/',
        name: 'reports',
        component: () => import('pages/ReportsPage.vue'),
        meta: { verboseName: 'Отчёты' },
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

