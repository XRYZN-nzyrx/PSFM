from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from expense_classifier import train_expense_model, categorize_expenses
from finance_calculations import calculate_savings_potential, check_savings_goal, suggest_savings_goal
from salary_predictor import predict_future_salary
import os

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Personal Finance Management API")

# CORS setup for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPENSE_DATA_PATH = os.path.join(BASE_DIR, "datasets", "logistic_regression_product_dataset_10000.csv")
SALARY_DATA_PATH = os.path.join(BASE_DIR, "datasets", "salarydata.csv")

# Train expense classifier ONCE at startup
clf, scaler = train_expense_model(EXPENSE_DATA_PATH)

# Pydantic models
class Expense(BaseModel):
    name: str
    amount: float
    frequency: float
    unit: Optional[str] = "monthly"
    seasonal_flag: Optional[int] = 0  # Make this optional with a default

class FinanceInput(BaseModel):
    income: float
    expenses: List[Expense]
    savings_goal: float
    current_salary: float
    inflation_rate: Optional[float] = None

@app.post("/analyze")
def analyze_finance(data: FinanceInput):
    # Step 1: Format expenses
    structured_expenses = [
        (e.name, e.amount, e.frequency, e.unit, e.seasonal_flag or 0)
        for e in data.expenses
    ]

    # Step 2: Financial calculations
    savings_potential = calculate_savings_potential(data.income, structured_expenses)
    aligned = check_savings_goal(savings_potential, data.savings_goal)
    updated_goal = suggest_savings_goal(savings_potential, data.savings_goal)

    #  Safely parse inflation_rate (can be blank string or invalid from frontend)
    inflation_rate = None
    if data.inflation_rate is not None:
        try:
            inflation_rate = float(data.inflation_rate)
        except (ValueError, TypeError):
            inflation_rate = None

    # Step 3: Salary prediction
    future_salary = predict_future_salary(
        current_salary=data.current_salary,
        inflation_rate=inflation_rate,
        dataset_path=SALARY_DATA_PATH
    )

    # Step 4: Expense categorization
    categorized_expenses = categorize_expenses(structured_expenses, clf, scaler)
    essential_total = sum(amount for _, amount, label in categorized_expenses if label == "Essential")
    luxury_total = sum(amount for _, amount, label in categorized_expenses if label == "Luxury")

    return {
        "categorized_expenses": categorized_expenses,
        "essential_total": essential_total,
        "luxury_total": luxury_total,
        "savings_potential": savings_potential,
        "goal_alignment": aligned,
        "suggested_goal": updated_goal,
        "predicted_salary": future_salary,
    }
