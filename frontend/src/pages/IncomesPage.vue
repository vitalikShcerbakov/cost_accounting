<template>
  <q-page class="q-pa-md">
    <div class="row q-col-gutter-md">
      <!-- Заголовок и фильтры -->
      <div class="col-12">
        <div class="row q-col-gutter-md items-center">
          <div class="col">
            <h1 class="text-h4 text-weight-bold text-primary">Доходы</h1>
          </div>
          <div class="col-auto">
            <q-btn color="positive" icon="add" label="Добавить доход" @click="showDialog = true" />
          </div>
        </div>
      </div>

      <!-- Фильтры -->
      <div class="col-12">
        <q-card>
          <q-card-section>
            <div class="row q-col-gutter-md">
              <div class="col-12 col-md-3">
                <q-input
                  v-model="filters.start_date"
                  label="Дата начала"
                  type="date"
                  clearable
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model="filters.end_date"
                  label="Дата окончания"
                  type="date"
                  clearable
                />
              </div>
              <div class="col-12 col-md-3">
                <q-select
                  v-model="filters.category_id"
                  :options="categories"
                  option-label="name"
                  option-value="id"
                  label="Категория"
                  clearable
                />
              </div>
              <div class="col-12 col-md-3">
                <q-btn color="primary" label="Применить фильтры" @click="loadIncomes" />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Таблица доходов -->
      <div class="col-12">
        <q-card>
          <q-card-section>
            <q-table
              :rows="incomes"
              :columns="columns"
              row-key="id"
              :loading="loading"
              :pagination="pagination"
              @request="onRequest"
            >
              <template #body-cell-actions="props">
                <q-td :props="props">
                  <q-btn flat round icon="edit" color="primary" @click="editIncome(props.row)" />
                  <q-btn flat round icon="delete" color="negative" @click="deleteIncome(props.row.id)" />
                </q-td>
              </template>
            </q-table>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Диалог добавления/редактирования дохода -->
    <q-dialog v-model="showDialog">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">{{ editingIncome ? 'Редактировать доход' : 'Добавить доход' }}</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="saveIncome" class="q-gutter-md">
            <q-input
              v-model.number="form.amount"
              label="Сумма"
              type="number"
              :rules="[val => val > 0 || 'Сумма должна быть больше 0']"
              required
            />
            <q-input
              v-model="form.description"
              label="Описание"
              :rules="[val => val.length > 0 || 'Введите описание']"
              required
            />
            <q-input
              v-model="form.date"
              label="Дата"
              type="date"
              required
            />
            <q-select
              v-model="form.category_id"
              :options="categories"
              option-label="name"
              option-value="id"
              label="Категория"
              :rules="[val => val > 0 || 'Выберите категорию']"
              required
            />
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" v-close-popup />
          <q-btn flat label="Сохранить" color="primary" @click="saveIncome" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { incomesApi, categoriesApi } from '../services/api'
import type { Income, IncomeCreate, IncomeUpdate, Category } from '../types/api'
import type { QTableProps } from 'quasar'

const $q = useQuasar()

// Реактивные данные
const incomes = ref<Income[]>([])
const categories = ref<Category[]>([])
const loading = ref(false)
const showDialog = ref(false)
const editingIncome = ref<Income | null>(null)

const filters = ref({
  start_date: '',
  end_date: '',
  category_id: 0
})

const pagination = ref({
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0,
  sortBy: '',
  descending: false
})

const form = ref<IncomeCreate>({
  amount: 0,
  description: '',
  date: new Date().toISOString().split('T')[0] || '',
  category_id: 0
})

// Колонки таблицы
const columns = [
  { name: 'id', label: 'ID', field: 'id', sortable: true, align: 'left' as const },
  { name: 'amount', label: 'Сумма', field: 'amount', sortable: true, align: 'right' as const, format: (val: number) => `${val.toLocaleString()} ₽` },
  { name: 'description', label: 'Описание', field: 'description', sortable: true, align: 'left' as const },
  { name: 'date', label: 'Дата', field: 'date', sortable: true, align: 'left' as const },
  { name: 'category', label: 'Категория', field: (row: Income) => row.category?.name || '', sortable: true, align: 'left' as const },
  { name: 'actions', label: 'Действия', field: 'actions', align: 'center' as const }
]

// Методы
const loadIncomes = async () => {
  loading.value = true
  try {
    // const params: Record<string, any> = {
    const params: Record<string, unknown> = {
      skip: (pagination.value.page - 1) * pagination.value.rowsPerPage,
      limit: pagination.value.rowsPerPage
    }
    
    if (filters.value.start_date) params.start_date = filters.value.start_date
    if (filters.value.end_date) params.end_date = filters.value.end_date
    if (filters.value.category_id) params.category_id = filters.value.category_id

    const response = await incomesApi.getAll(params)
    incomes.value = response.data
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка загрузки доходов'
    })
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const response = await categoriesApi.getAll()
    categories.value = response.data
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка загрузки категорий'
    })
  }
}

const saveIncome = async () => {
  try {
    if (editingIncome.value) {
      await incomesApi.update(editingIncome.value.id, form.value as IncomeUpdate)
      $q.notify({
        type: 'positive',
        message: 'Доход успешно обновлен'
      })
    } else {
      await incomesApi.create(form.value)
      $q.notify({
        type: 'positive',
        message: 'Доход успешно добавлен'
      })
    }
    
    await loadIncomes()
    showDialog.value = false
    resetForm()
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка сохранения дохода'
    })
  }
}

const editIncome = (income: Income) => {
  editingIncome.value = income
  form.value = {
    amount: income.amount,
    description: income.description || '',
    date: income.date.split('T')[0] || '',
    category_id: income.category_id
  }
  showDialog.value = true
}

const deleteIncome = async (id: number) => {
  try {
    const result = $q.dialog({
      title: 'Подтверждение',
      message: 'Вы уверены, что хотите удалить этот доход?',
      cancel: true,
      persistent: true
    })

    if (result) {
      await incomesApi.delete(id)
      await loadIncomes()
      $q.notify({
        type: 'positive',
        message: 'Доход успешно удален'
      })
    }
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка удаления дохода'
    })
  }
}

const resetForm = () => {
  editingIncome.value = null
  form.value = {
    amount: 0,
    description: '',
    date: new Date().toISOString().split('T')[0] || '',
    category_id: 0
  }
}

// const onRequest = (props: { pagination: typeof pagination.value }) => {
//   pagination.value = props.pagination
//   void loadIncomes()
// }

const onRequest: QTableProps['onRequest'] = (props) => {
  pagination.value = {
    page: props.pagination.page,
    rowsPerPage: props.pagination.rowsPerPage,
    rowsNumber: props.pagination.rowsNumber ?? 0,
    sortBy: props.pagination.sortBy ?? '',
    descending: props.pagination.descending ?? false
  }

  void loadIncomes()
}

onMounted(() => {
  void loadIncomes()
  void loadCategories()
})
</script> 