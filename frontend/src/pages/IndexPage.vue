<template>
  <q-page class="q-pa-md">
    <div class="row q-col-gutter-md">
      <!-- Статистика -->
      <div class="col-12">
        <q-card class="bg-primary text-white">
          <q-card-section>
            <div class="row q-col-gutter-md">
              <div class="col-4 text-center">
                <div class="text-h4">{{ totalIncome.toLocaleString() }} ₽</div>
                <div class="text-subtitle2">Общий доход</div>
              </div>
              <div class="col-4 text-center">
                <div class="text-h4">{{ totalExpenses.toLocaleString() }} ₽</div>
                <div class="text-subtitle2">Общие расходы</div>
              </div>
              <div class="col-4 text-center">
                <div class="text-h4" :class="balance >= 0 ? 'text-positive' : 'text-negative'">
                  {{ balance.toLocaleString() }} ₽
                </div>
                <div class="text-subtitle2">Баланс</div>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Быстрые действия -->
      <div class="col-12">
        <q-card>
          <q-card-section>
            <div class="text-h6">Быстрые действия</div>
            <div class="row q-col-gutter-sm q-mt-md">
              <q-btn color="positive" icon="add" label="Добавить доход" @click="showIncomeDialog = true" />
              <q-btn color="negative" icon="remove" label="Добавить расход" @click="showExpenseDialog = true" />
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Ежемесячные расходы -->
      <div class="col-12 col-md-6">
        <q-card>
          <q-card-section>
            <div class="text-h6">Ежемесячные расходы</div>
            <div class="text-h4 text-negative">{{ monthlyExpenses.toLocaleString() }} ₽</div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Последние транзакции -->
      <div class="col-12 col-md-6">
        <q-card>
          <q-card-section>
            <div class="text-h6">Последние доходы</div>
            <q-list>
              <q-item v-for="income in recentIncomes" :key="income.id">
                <q-item-section>
                  <q-item-label>{{ income.description }}</q-item-label>
                  <q-item-label caption>{{ income.date }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-item-label class="text-positive">{{ income.amount.toLocaleString() }} ₽</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-6">
        <q-card>
          <q-card-section>
            <div class="text-h6">Последние расходы</div>
            <q-list>
              <q-item v-for="expense in recentExpenses" :key="expense.id">
                <q-item-section>
                  <q-item-label>{{ expense.description }}</q-item-label>
                  <q-item-label caption>{{ expense.date }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-item-label class="text-negative">{{ expense.amount.toLocaleString() }} ₽</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Диалог добавления дохода -->
    <q-dialog v-model="showIncomeDialog">
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">Добавить доход</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="addIncome" class="q-gutter-md">
            <q-input v-model.number="newIncome.amount" label="Сумма" type="number"
              :rules="[val => val !== '', val => val > 0 || 'Сумма должна быть больше 0']" required />
            <q-input v-model="newIncome.description" label="Описание"
              :rules="[val => val.length > 0 || 'Введите описание']" required />
            <q-input v-model="newIncome.date" label="Дата" type="date" required />
            <q-select v-model="newIncome.category_id" :options="categoriesIncome" option-label="name" option-value="id"
              label="Категория" :rules="[val => val > ' ' || 'Выберите категорию']" required emit-value map-options />
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" v-close-popup />
          <q-btn flat label="Добавить" color="primary" @click="addIncome" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Диалог добавления расхода -->
    <q-dialog v-model="showExpenseDialog">
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">Добавить расход</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="addExpense" class="q-gutter-md">
            <q-input v-model="newExpense.amount"
              @keyup.enter="calculateAmount((result: number) => newExpense.amount = result, newExpense.amount)"
              label="Сумма" type="text" :rules="[val => val > 0 || 'Сумма должна быть больше 0']" required />
            <q-input v-model="newExpense.description" label="Описание"
              :rules="[val => val.length > 0 || 'Введите описание']" required />
            <q-input v-model="newExpense.date" label="Дата" type="date" required />
            <q-select v-model="newExpense.category_id" :options="categoriesExpense" option-label="name"
              option-value="id" label="Категория" :rules="[val => val > '' || 'Выберите категорию']" emit-value
              map-options required />
            <q-select v-model="newExpense.expense_type_id" :options="expenseTypes" option-label="name" option-value="id"
              label="Тип расхода" :rules="[val => val > '' || 'Выберите тип расхода']" emit-value map-options
              required />
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" v-close-popup />
          <q-btn flat label="Добавить" color="primary" @click="addExpense" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { categoriesExpenseApi, expenseTypesApi, incomesApi, expensesApi, categoriesIncomeApi } from '../services/api'
import type { Category, ExpenseType, Income, IncomeCreate, Expense, ExpenseCreate } from '../types/api'
import { useAuthStore } from '../store/auth'

const $q = useQuasar()
const authStore = useAuthStore()

// Реактивные данные
const categoriesExpense = ref<Category[]>([])
const categoriesIncome = ref<Category[]>([])
const expenseTypes = ref<ExpenseType[]>([])
const recentIncomes = ref<Income[]>([])
const recentExpenses = ref<Expense[]>([])

const showIncomeDialog = ref(false)
const showExpenseDialog = ref(false)

const newIncome = ref<IncomeCreate>({
  amount: 0,
  description: '',
  date: new Date().toISOString().split('T')[0] || '',
  category_id: 0
})

const newExpense = ref<ExpenseCreate>({
  amount: 0,
  description: '',
  date: new Date().toISOString().split('T')[0] || '',
  category_id: 0,
  expense_type_id: 0
})

// Вычисляемые свойства
const totalIncome = computed(() => {
  return recentIncomes.value.reduce((sum, income) => sum + income.amount, 0)
})

const totalExpenses = computed(() => {
  return recentExpenses.value.reduce((sum, expense) => sum + expense.amount, 0)
})

const balance = computed(() => {
  return totalIncome.value - totalExpenses.value
})

const monthlyExpenses = computed(() => {
  return recentExpenses.value
    .filter(expense => {
      const expenseType = expenseTypes.value.find(et => et.id === expense.expense_type_id)
      return expenseType?.is_monthly
    })
    .reduce((sum, expense) => sum + expense.amount, 0)
})

// Методы
const calculateAmount = (callback: CallableFunction, value: string | null | number) => {
  try {
    const operator = (value as string).match(/[+\-*/]/g)
    const nums = (value as string).match(/\d+\.?\d*/g)
    if (operator && nums) {
      const result: number = eval(value as string)
      callback(result)
    }
  } catch {
    console.error('все пропало..')
    return
  }
}

const loadData = async () => {
  try {
    const [categoriesExpenseRes, categoriesIncomeRes, expenseTypesRes, incomesRes, expensesRes] = await Promise.all([
      categoriesExpenseApi.getAll(),
      categoriesIncomeApi.getAll(),
      expenseTypesApi.getAll(),
      incomesApi.getAll({ limit: 5 }),
      expensesApi.getAll({ limit: 5 })
    ])

    categoriesExpense.value = categoriesExpenseRes.data
    categoriesIncome.value = categoriesIncomeRes.data
    expenseTypes.value = expenseTypesRes.data
    recentIncomes.value = incomesRes.data
    recentExpenses.value = expensesRes.data
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка загрузки данных'
    })
  }
}
const addIncome = async () => {
  try {
    await loadData()
    showIncomeDialog.value = false
    const obj: IncomeCreate = {
      amount: newIncome.value.amount,
      description: newIncome.value.description,
      date: newIncome.value.date + ' ' + new Date().toISOString().split('T')[1],
      category_id: newIncome.value.category_id
    }
    
    // Добавляем user_id только если пользователь авторизован
    if (authStore.user?.id) {
      obj.user_id = authStore.user.id
    }
    
    await incomesApi.create(obj)
    $q.notify({
      type: 'positive',
      message: 'Доход успешно добавлен'
    })
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка добавления дохода'
    })
  }
}

const addExpense = async () => {
  try {
    await loadData()
    showExpenseDialog.value = false
    const timeStr = new Date().toISOString().split('T')[1]
    // const timeNow = timeStr.substring(0, timeStr.length - 1)
    if (timeStr) {
      // const timeNow = timeStr.replace(/.$/, '')
      const timeNow = timeStr.substring(0, timeStr.length - 1)
      console.log('fddfdf', timeNow)
    }
    const obj: ExpenseCreate = {
      amount: newExpense.value.amount,
      description: newExpense.value.description,
      date: newExpense.value.date + ' ' + timeStr,
      category_id: newExpense.value.category_id,
      expense_type_id: newExpense.value.expense_type_id,
    }
    
    // Добавляем user_id только если пользователь авторизован
    if (authStore.user?.id) {
      obj.user_id = authStore.user.id
    }
    
    await expensesApi.create(obj)
    $q.notify({
      type: 'positive',
      message: 'Расход успешно добавлен'
    })
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка добавления расхода'
    })
  }
}


// Загрузка данных при монтировании
onMounted(() => {
  void loadData()
  newExpense.value.expense_type_id = 1
})
</script>