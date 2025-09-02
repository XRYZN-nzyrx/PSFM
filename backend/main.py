from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from backend.expense_classifier import train_expense_model, categorize_expenses
from backend.finance_calculations import calculate_savings_potential, check_savings_goal, suggest_savings_goal
from backend.salary_predictor import predict_future_salary
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

app = FastAPI(title="Personal Finance Management API")

# CORS setup for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://personal-finance-manager-wne3.onrender.com", 
        "http://localhost:3000",

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPENSE_DATA_PATH = os.path.join(BASE_DIR, "Datasets", "logistic_regression_product_dataset_10000.csv")
SALARY_DATA_PATH = os.path.join(BASE_DIR, "Datasets", "salarydata.csv")

# Mount static files from React build
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

# Train expense model on startup
clf, scaler = train_expense_model(EXPENSE_DATA_PATH)

# ----------- Data Models -----------

class Expense(BaseModel):
    name: str
    amount: float
    frequency: float
    unit: Optional[str] = "monthly"
    seasonal_flag: Optional[int] = 0

class FinanceInput(BaseModel):
    income: float
    expenses: List[Expense]
    savings_goal: float
    current_salary: float
    inflation_rate: Optional[float] = None

# ----------- API Route -----------

@app.post("/analyze")
def analyze_finance(data: FinanceInput):
    structured_expenses = [
        (e.name, e.amount, e.frequency, e.unit, e.seasonal_flag or 0)
        for e in data.expenses
    ]

    savings_potential = calculate_savings_potential(data.income, structured_expenses)
    aligned = check_savings_goal(savings_potential, data.savings_goal)
    updated_goal = suggest_savings_goal(savings_potential, data.savings_goal)

    inflation_rate = None
    if data.inflation_rate is not None:
        try:
            inflation_rate = float(data.inflation_rate)
        except (ValueError, TypeError):
            inflation_rate = None

    future_salary = predict_future_salary(
        current_salary=data.current_salary,
        inflation_rate=inflation_rate,
        dataset_path=SALARY_DATA_PATH
    )

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

# ----------- React Frontend Serving Routes -----------

@app.get("/")
def serve_react():
    return FileResponse("frontend/build/index.html")

@app.get("/{full_path:path}")
def serve_react_app(full_path: str):
    if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
        return {"error": "Not found"}
    return FileResponse("frontend/build/index.html")
