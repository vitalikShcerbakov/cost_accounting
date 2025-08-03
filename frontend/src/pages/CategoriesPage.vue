<template>
  <q-page class="q-pa-md">
    <div class="row q-col-gutter-md">
      <!-- Заголовок -->
      <div class="col-12">
        <div class="row q-col-gutter-md items-center">
          <div class="col">
            <h1 class="text-h4 text-weight-bold text-primary">Категории</h1>
          </div>
          <div class="col-auto">
            <q-btn color="primary" icon="add" label="Добавить категорию" @click="showDialog = true" />
          </div>
        </div>
      </div>

      <!-- Таблица категорий -->
      <div class="col-12">
        <q-card>
          <q-card-section>
            <q-table
              :rows="categories"
              :columns="columns"
              row-key="id"
              :loading="loading"
            >
              <template #body-cell-actions="props">
                <q-td :props="props">
                  <q-btn flat round icon="edit" color="primary" @click="editCategory(props.row)" />
                  <q-btn flat round icon="delete" color="negative" @click="deleteCategory(props.row.id)" />
                </q-td>
              </template>
            </q-table>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Диалог добавления/редактирования категории -->
    <q-dialog v-model="showDialog">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">{{ editingCategory ? 'Редактировать категорию' : 'Добавить категорию' }}</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="saveCategory" class="q-gutter-md">
            <q-input
              v-model="form.name"
              label="Название"
              :rules="[val => val.length > 0 || 'Введите название']"
              required
            />
            <q-input
              v-model="form.description"
              label="Описание"
              type="textarea"
            />
            <q-input
              v-model="form.color"
              label="Цвет"
            />
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" v-close-popup />
          <q-btn flat label="Сохранить" color="primary" @click="saveCategory" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { categoriesApi } from '../services/api'
import type { Category, CategoryCreate, CategoryUpdate } from '../types/api'

const $q = useQuasar()

// Реактивные данные
const categories = ref<Category[]>([])
const loading = ref(false)
const showDialog = ref(false)
const editingCategory = ref<Category | null>(null)

const form = ref<CategoryCreate>({
  name: '',
  description: '',
  color: '#1976D2'
})

// Колонки таблицы
const columns = [
  { name: 'id', label: 'ID', field: 'id', sortable: true, align: 'left' as const },
  { name: 'name', label: 'Название', field: 'name', sortable: true, align: 'left' as const },
  { name: 'description', label: 'Описание', field: 'description', sortable: true, align: 'left' as const },
  { name: 'color', label: 'Цвет', field: 'color', align: 'center' as const },
  { name: 'actions', label: 'Действия', field: 'actions', align: 'center' as const }
]

// Методы
const loadCategories = async () => {
  loading.value = true
  try {
    const response = await categoriesApi.getAll()
    categories.value = response.data
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка загрузки категорий'
    })
  } finally {
    loading.value = false
  }
}

const saveCategory = async () => {
  try {
    if (editingCategory.value) {
      await categoriesApi.update(editingCategory.value.id, form.value as CategoryUpdate)
      $q.notify({
        type: 'positive',
        message: 'Категория успешно обновлена'
      })
    } else {
      await categoriesApi.create(form.value)
      $q.notify({
        type: 'positive',
        message: 'Категория успешно добавлена'
      })
    }
    
    await loadCategories()
    showDialog.value = false
    resetForm()
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка сохранения категории'
    })
  }
}

const editCategory = (category: Category) => {
  editingCategory.value = category
  form.value = {
    name: category.name,
    description: category.description || '',
    color: category.color || '#1976D2'
  }
  showDialog.value = true
}

const deleteCategory = async (id: number) => {
  try {
    const result = await $q.dialog({
      title: 'Подтверждение',
      message: 'Вы уверены, что хотите удалить эту категорию?',
      cancel: true,
      persistent: true
    })

    if (result) {
      await categoriesApi.delete(id)
      await loadCategories()
      $q.notify({
        type: 'positive',
        message: 'Категория успешно удалена'
      })
    }
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка удаления категории'
    })
  }
}

const resetForm = () => {
  editingCategory.value = null
  form.value = {
    name: '',
    description: '',
    color: '#1976D2'
  }
}

onMounted(() => {
  void loadCategories()
})
</script> 