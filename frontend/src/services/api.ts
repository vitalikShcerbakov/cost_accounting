import axios from 'axios'
import type {
  Category,
  CategoryCreate,
  CategoryUpdate,
  ExpenseType,
  ExpenseTypeCreate,
  ExpenseTypeUpdate,
  Expense,
  ExpenseCreate,
  ExpenseUpdate,
  Income,
  IncomeCreate,
  IncomeUpdate,
  MonthlySummary,
  CategorySummary
} from '../types/api'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Categories API
export const categoriesApi = {
  getAll: () => api.get<Category[]>('/categories/'),
  getById: (id: number) => api.get<Category>(`/categories/${id}`),
  create: (data: CategoryCreate) => api.post<Category>('/categories/', data),
  update: (id: number, data: CategoryUpdate) => api.put<Category>(`/categories/${id}`, data),
  delete: (id: number) => api.delete(`/categories/${id}`)
}

// Expense Types API
export const expenseTypesApi = {
  getAll: () => api.get<ExpenseType[]>('/expense-types/'),
  getMonthly: () => api.get<ExpenseType[]>('/expense-types/monthly'),
  getById: (id: number) => api.get<ExpenseType>(`/expense-types/${id}`),
  create: (data: ExpenseTypeCreate) => api.post<ExpenseType>('/expense-types/', data),
  update: (id: number, data: ExpenseTypeUpdate) => api.put<ExpenseType>(`/expense-types/${id}`, data),
  delete: (id: number) => api.delete(`/expense-types/${id}`)
}

// Expenses API
export const expensesApi = {
  getAll: (params?: {
    skip?: number
    limit?: number
    start_date?: string
    end_date?: string
    category_id?: number
    expense_type_id?: number
  }) => api.get<Expense[]>('/expenses/', { params }),
  getById: (id: number) => api.get<Expense>(`/expenses/${id}`),
  create: (data: ExpenseCreate) => api.post<Expense>('/expenses/', data),
  update: (id: number, data: ExpenseUpdate) => api.put<Expense>(`/expenses/${id}`, data),
  delete: (id: number) => api.delete(`/expenses/${id}`)
}

// Incomes API
export const incomesApi = {
  getAll: (params?: {
    skip?: number
    limit?: number
    start_date?: string
    end_date?: string
    category_id?: number
  }) => api.get<Income[]>('/incomes/', { params }),
  getById: (id: number) => api.get<Income>(`/incomes/${id}`),
  create: (data: IncomeCreate) => api.post<Income>('/incomes/', data),
  update: (id: number, data: IncomeUpdate) => api.put<Income>(`/incomes/${id}`, data),
  delete: (id: number) => api.delete(`/incomes/${id}`)
}

// Summary API
export const summaryApi = {
  getMonthly: (year: number, month: number) => 
    api.get<MonthlySummary>(`/summary/monthly/${year}/${month}`),
  getCategorySummary: (params?: {
    start_date?: string
    end_date?: string
  }) => api.get<CategorySummary[]>('/summary/category-summary', { params })
}

export default api 