<template>
  <q-page class="q-pa-md">
    <div class="row q-col-gutter-md">
      <!-- Заголовок -->
      <div class="col-12">
        <h1 class="text-h4 text-weight-bold text-primary">Отчеты</h1>
      </div>

      <!-- Месячная сводка -->
      <div class="col-12 col-md-6">
        <q-card>
          <q-card-section>
            <div class="text-h6">Месячная сводка</div>
            <div class="row q-col-gutter-sm q-mt-md">
              <div class="col-6">
                <q-select
                  v-model="selectedYear"
                  :options="years"
                  label="Год"
                  @update:model-value="loadMonthlySummary"
                />
              </div>
              <div class="col-6">
                <q-select
                  v-model="selectedMonth"
                  :options="months"
                  label="Месяц"
                  @update:model-value="loadMonthlySummary"
                />
              </div>
            </div>
          </q-card-section>

          <q-card-section v-if="monthlySummary">
            <div class="row q-col-gutter-md">
              <div class="col-6">
                <div class="text-h6 text-positive">Доходы</div>
                <div class="text-h4">{{ monthlySummary.total_income.toLocaleString() }} ₽</div>
              </div>
              <div class="col-6">
                <div class="text-h6 text-negative">Расходы</div>
                <div class="text-h4">{{ monthlySummary.total_expenses.toLocaleString() }} ₽</div>
              </div>
              <div class="col-12">
                <div class="text-h6" :class="monthlySummary.balance >= 0 ? 'text-positive' : 'text-negative'">
                  Баланс: {{ monthlySummary.balance.toLocaleString() }} ₽
                </div>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Сводка по категориям -->
      <div class="col-12 col-md-6">
        <q-card>
          <q-card-section>
            <div class="text-h6">Сводка по категориям</div>
            <div class="row q-col-gutter-sm q-mt-md">
              <div class="col-6">
                <q-input
                  v-model="categoryFilters.start_date"
                  label="Дата начала"
                  type="date"
                  clearable
                />
              </div>
              <div class="col-6">
                <q-input
                  v-model="categoryFilters.end_date"
                  label="Дата окончания"
                  type="date"
                  clearable
                />
              </div>
              <div class="col-12">
                <q-btn color="primary" label="Загрузить" @click="loadCategorySummary" />
              </div>
            </div>
          </q-card-section>

          <q-card-section v-if="categorySummary.length > 0">
            <q-table
              :rows="categorySummary"
              :columns="categoryColumns"
              row-key="category_id"
              :loading="categoryLoading"
            >
              <template #body-cell-total_amount="props">
                <q-td :props="props">
                  <span class="text-negative">{{ props.value.toLocaleString() }} ₽</span>
                </q-td>
              </template>
            </q-table>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { summaryApi } from '../services/api'
import type { MonthlySummary, CategorySummary } from '../types/api'

const $q = useQuasar()

// Реактивные данные
const monthlySummary = ref<MonthlySummary | null>(null)
const categorySummary = ref<CategorySummary[]>([])
const categoryLoading = ref(false)

const selectedYear = ref(new Date().getFullYear())
const selectedMonth = ref(new Date().getMonth() + 1)

const categoryFilters = ref({
  start_date: '',
  end_date: ''
})

// Опции для селекторов
const years = Array.from({ length: 10 }, (_, i) => new Date().getFullYear() - i)
const months = [
  { label: 'Январь', value: 1 },
  { label: 'Февраль', value: 2 },
  { label: 'Март', value: 3 },
  { label: 'Апрель', value: 4 },
  { label: 'Май', value: 5 },
  { label: 'Июнь', value: 6 },
  { label: 'Июль', value: 7 },
  { label: 'Август', value: 8 },
  { label: 'Сентябрь', value: 9 },
  { label: 'Октябрь', value: 10 },
  { label: 'Ноябрь', value: 11 },
  { label: 'Декабрь', value: 12 }
]

// Колонки для таблицы категорий
const categoryColumns = [
  { name: 'category_name', label: 'Категория', field: 'category_name', sortable: true, align: 'left' as const },
  { name: 'total_amount', label: 'Сумма', field: 'total_amount', sortable: true, align: 'right' as const },
  { name: 'count', label: 'Количество', field: 'count', sortable: true, align: 'center' as const }
]

// Методы
const loadMonthlySummary = async () => {
  try {
    const response = await summaryApi.getMonthly(selectedYear.value, selectedMonth.value)
    monthlySummary.value = response.data
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка загрузки месячной сводки'
    })
  }
}

const loadCategorySummary = async () => {
  categoryLoading.value = true
  try {
    const params: Record<string, any> = {}
    if (categoryFilters.value.start_date) params.start_date = categoryFilters.value.start_date
    if (categoryFilters.value.end_date) params.end_date = categoryFilters.value.end_date

    const response = await summaryApi.getCategorySummary(params)
    categorySummary.value = response.data
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Ошибка загрузки сводки по категориям'
    })
  } finally {
    categoryLoading.value = false
  }
}

onMounted(() => {
  void loadMonthlySummary()
})
</script> 