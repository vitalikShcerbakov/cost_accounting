export interface Category {
  id: number
  name: string
  description?: string
  color?: string
  created_at: string
  updated_at?: string
}

export interface ExpenseType {
  id: number
  name: string
  description?: string
  is_monthly: boolean
  monthly_budget?: number
  created_at: string
  updated_at?: string
}

export interface Expense {
  id: number
  amount: number
  description?: string
  date: string
  category_id: number
  expense_type_id: number
  created_at: string
  updated_at?: string
  category: Category
  expense_type: ExpenseType
}

export interface Income {
  id: number
  amount: number
  description?: string
  date: string
  category_id: number
  created_at: string
  updated_at?: string
  category: Category
}

export interface MonthlySummary {
  month: string
  total_income: number
  total_expenses: number
  balance: number
  monthly_expenses: number
  other_expenses: number
}

export interface CategorySummary {
  category_id: number
  category_name: string
  total_amount: number
  count: number
}

// Create/Update DTOs
export interface CategoryCreate {
  name: string
  description?: string
  color?: string
}

export interface CategoryUpdate {
  name?: string
  description?: string
  color?: string
}

export interface ExpenseTypeCreate {
  name: string
  description?: string
  is_monthly: boolean
  monthly_budget?: number
}

export interface ExpenseTypeUpdate {
  name?: string
  description?: string
  is_monthly?: boolean
  monthly_budget?: number
}

export interface ExpenseCreate {
  amount: number
  description?: string
  date: string
  category_id: number
  expense_type_id: number
}

export interface ExpenseUpdate {
  amount?: number
  description?: string
  date?: string
  category_id?: number
  expense_type_id?: number
}

export interface IncomeCreate {
  amount: number
  description?: string
  date: string
  category_id: number
}

export interface IncomeUpdate {
  amount?: number
  description?: string
  date?: string
  category_id?: number
} 