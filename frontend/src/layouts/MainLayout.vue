<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          Учет доходов и расходов
        </q-toolbar-title>
        <div @click="$q.dark.toggle()">
          <q-btn
            :class="{ 'text-black bg-grey-4': $q.dark.isActive, 'text-white bg-primary': !$q.dark.isActive }"
            :fab-mini="true"
            :dense="true"
            >
            смена темы
          </q-btn>
        </div>
        <div >Quasar v{{ $q.version }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label header>
          Навигация
        </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

const essentialLinks = [
  {
    title: 'Главная',
    caption: 'Дашборд',
    icon: 'home',
    link: '/'
  },
  {
    title: 'Доходы',
    caption: 'Управление доходами',
    icon: 'trending_up',
    link: '/incomes'
  },
  {
    title: 'Расходы',
    caption: 'Управление расходами',
    icon: 'trending_down',
    link: '/expenses'
  },
  {
    title: 'Категории',
    caption: 'Управление категориями',
    icon: 'category',
    link: '/categories'
  },
  {
    title: 'Отчеты',
    caption: 'Аналитика и отчеты',
    icon: 'analytics',
    link: '/reports'
  }
]

const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script> 