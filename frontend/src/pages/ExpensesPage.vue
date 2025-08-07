<template>
  <q-page class="q-pa-md">
    <div class="row q-col-gutter-md">
      <!-- Заголовок и фильтры -->
      <div class="col-12">
        <div class="row q-col-gutter-md items-center">
          <div class="col">
            <h1 class="text-h4 text-weight-bold text-primary">Расходы</h1>
          </div>
          <div class="col-auto">
            <q-btn color="negative" icon="add" label="Добавить расход" @click="showDialog = true" />
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
              <div class="col-12 col-md-2">
                <q-select
                  v-model="filters.category_id"
                  :options="categories"
                  option-label="name"
                  option-value="id"
                  label="Категория"
                  clearable
                />
              </div>
              <div class="col-12 col-md-2">
                <q-select
                  v-model="filters.expense_type_id"
                  :options="expenseTypes"
                  option-label="name"
                  option-value="id"
                  label="Тип расхода"
                  clearable
                />
              </div>
              <div class="col-12 col-md-2">
                <q-btn color="primary" label="Применить фильтры" @click="loadExpenses" />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Таблица расходов -->
      <div class="col-12">
        <q-card>
          <q-card-section>
            <q-table
              :rows="expenses"
              :columns="columns"
              row-key="id"
              :loading="loading"
              :pagination="pagination"
              @request="onRequest"
            >
              <template #body-cell-actions="props">
                <q-td :props="props">
                  <q-btn flat round icon="edit" color="primary" @click="editExpense(props.row)" />
                  <q-btn flat round icon="delete" color="negative" @click="deleteExpense(props.row.id)" />
                </q-td>
              </template>
            </q-table>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Диалог добавления/редактирования расхода -->
    <q-dialog v-model="showDialog">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">{{ editingExpense ? 'Редактировать расход' : 'Добавить расход' }}</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="saveExpense" class="q-gutter-md">
            <q-input
              v-model.number="form.amount"
              label="Сумма"
              type="number"
              :rules="[val => val > '' || 'Сумма должна быть больше 0']"
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
              :rules="[val => val > ' ' || 'Выберите категорию']"
              emit-value
              map-options
              required
            />
            <q-select
              v-model="form.expense_type_id"
              :options="expenseTypes"
              option-label="name"
              option-value="id"
              label="Тип расхода"
              :rules="[val => val > 0 || 'Выберите тип расхода']"
              emit-value
              map-options
              required
            />
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" v-close-popup />
          <q-btn flat label="Сохранить" color="primary" @click="saveExpense" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { expensesApi, categoriesExpenseApi, expenseTypesApi } from '../services/api'
import type { Expense, ExpenseCreate, ExpenseUpdate, Category, ExpenseType } from '../types/api'
import type { QTableProps } from 'quasar'

const $q = useQuasar()

// Реактивные данные
const expenses = ref<Expense[]>([])
const categories = ref<Category[]>([])
const expenseTypes = ref<ExpenseType[]>([])
const loading = ref(false)
const showDialog = ref(false)
const editingExpense = ref<Expense | null>(null)

const filters = ref({
  start_date: '',
  end_date: '',
  category_id: 0,
  expense_type_id: 0
})

const pagination = ref({
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0,
  sortBy: '',
  descending: false
})


const form = ref<ExpenseCreate>({
  amount: 0,
  description: '',
  date: new Date().toISOString().split('T')[0] || '',
  category_id: 0,
  expense_type_id: 0
})

// Колонки таблицы
const columns = [
  { name: 'id', label: 'ID', field: 'id', sortable: true, align: 'left' as const },
  { name: 'amount', label: 'Сумма', field: 'amount', sortable: true, align: 'right' as const, format: (val: number) => `${val.toLocaleString()} ₽` },
  { name: 'description', label: 'Описание', field: 'description', sortable: true, align: 'left' as const },
  { name: 'date', label: 'Дата', field: 'date', sortable: true, align: 'left' as const },
  { name: 'category', label: 'Категория', field: (row: Expense) => row.category?.name || '', sortable: true, align: 'left' as const },
  { name: 'expense_type', label: 'Тип расхода', field: (row: Expense) => row.expense_type?.name || '', sortable: true, align: 'left' as const },
  { name: 'actions', label: 'Действия', field: 'actions', align: 'center' as const }
]

// Методы
const loadExpenses = async () => {
  loading.value = true
  try {
    //const params: Record<string, any> = {
    const params: Record<string, unknown> = {
      skip: (pagination.value.page - 1) * pagination.value.rowsPerPage,
      limit: pagination.value.rowsPerPage
    }
    
    if (filters.value.start_date) params.start_date = filters.value.start_date
    if (filters.value.end_date) params.end_date = filters.value.end_date
    if (filters.value.category_id) params.category_id = filters.value.category_id
    if (filters.value.expense_type_id) params.expense_type_id = filters.value.expense_type_id

    const response = await expensesApi.getAll(params)
    expenses.value = response.data
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка загрузки расходов'
    })
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const response = await categoriesExpenseApi.getAll()
    categories.value = response.data
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка загрузки категорий'
    })
  }
}

const loadExpenseTypes = async () => {
  try {
    const response = await expenseTypesApi.getAll()
    expenseTypes.value = response.data
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка загрузки типов расходов'
    })
  }
}

const saveExpense = async () => {
  try {
    form.value.date = form.value.date + ' ' + new Date().toISOString().split('T')[1]  // подумать как заменить кастыль
    if (editingExpense.value) {
      await expensesApi.update(
        editingExpense.value.id,
      form.value as ExpenseUpdate)
      $q.notify({
        type: 'positive',
        message: 'Расход успешно обновлен'
      })
    } else {
      await expensesApi.create(form.value)
      $q.notify({
        type: 'positive',
        message: 'Расход успешно добавлен'
      })
    }
    
    await loadExpenses()
    showDialog.value = false
    resetForm()
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка сохранения расхода'
    })
  }
}

const editExpense = (expense: Expense) => {
  editingExpense.value = expense
  form.value = {
    amount: expense.amount,
    description: expense.description || '',
    date: expense.date.split('T')[0] || '',
    category_id: expense.category_id,
    expense_type_id: expense.expense_type_id
  }
  showDialog.value = true
}

const deleteExpense = async (id: number) => {
  try {
    const result = $q.dialog({
      title: 'Подтверждение',
      message: 'Вы уверены, что хотите удалить этот расход?',
      cancel: true,
      persistent: true
    })

    if (result) {
      await expensesApi.delete(id)
      await loadExpenses()
      $q.notify({
        type: 'positive',
        message: 'Расход успешно удален'
      })
    }
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка удаления расхода'
    })
  }
}

const resetForm = () => {
  editingExpense.value = null
  form.value = {
    amount: 0,
    description: '',
    date: new Date().toISOString().split('T')[0] || '',
    category_id: 0,
    expense_type_id: 0
  }
}

const onRequest: QTableProps['onRequest'] = (props) => {
  pagination.value = {
    page: props.pagination.page,
    rowsPerPage: props.pagination.rowsPerPage,
    rowsNumber: props.pagination.rowsNumber ?? 0,
    sortBy: props.pagination.sortBy ?? '',
    descending: props.pagination.descending ?? false
  }

  void loadExpenses()
}

onMounted(() => {
  void loadExpenses()
  void loadCategories()
  void loadExpenseTypes()
})
</script> 