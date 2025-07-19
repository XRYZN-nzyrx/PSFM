import React, { useState } from "react";
import './styles/ExpenseForm.css';
import Loader from "./Loader";

export default function FinanceForm({ setResult }) {
  const [income, setIncome] = useState("");
  const [savingsGoal, setSavingsGoal] = useState("");
  const [currentSalary, setCurrentSalary] = useState("");
  const [inflationRate, setInflationRate] = useState("");
  const [expenses, setExpenses] = useState([
    { name: "", amount: "", frequency: "", unit: "monthly", seasonal_flag: 0 },
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [errorKey, setErrorKey] = useState(0);
  const [showSuccess, setShowSuccess] = useState(false);

  const handleExpenseChange = (index, field, value) => {
    const updated = [...expenses];
    updated[index][field] = field === "seasonal_flag" ? parseInt(value) : value;
    setExpenses(updated);
  };

  const addExpense = () => {
    setExpenses([
      ...expenses,
      { name: "", amount: "", frequency: "", unit: "monthly", seasonal_flag: 0 },
    ]);
  };

  const removeExpense = (index) => {
    setExpenses(expenses.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setShowSuccess(false);

    const incomeNum = parseFloat(income);
    const savingsGoalNum = parseFloat(savingsGoal);
    const salaryNum = parseFloat(currentSalary);

    const totalYearlyExpenses = expenses.reduce((acc, exp) => {
      const amount = parseFloat(exp.amount) || 0;
      const freq = parseFloat(exp.frequency) || 0;
      const yearly = exp.unit === "yearly" ? amount * freq : amount * freq * 12;
      return acc + yearly;
    }, 0);

    if (incomeNum <= 0 || isNaN(incomeNum)) {
      setError("❌ Yearly income must be greater than 0.");
      setErrorKey(prev => prev + 1);
      setLoading(false);
      return;
    }
    if (salaryNum <= 0) {
      setError("❌ Current salary must be greater than 0.");
      setErrorKey(prev => prev + 1);
      setLoading(false);
      return;
    }
    if (savingsGoalNum <= 0 || isNaN(savingsGoalNum)) {
      setError("❌ Savings goal must be greater than 0.");
      setErrorKey(prev => prev + 1);
      setLoading(false);
      return;
    }
    if (totalYearlyExpenses > incomeNum) {
      setError("❌ Total expenses exceed your yearly income.");
      setErrorKey(prev => prev + 1);
      setLoading(false);
      return;
    }
    if (!isNaN(salaryNum) && salaryNum > incomeNum) {
      setError("❌ Current salary cannot be greater than yearly income.");
      setErrorKey(prev => prev + 1);
      setLoading(false);
      return;
    }
    if (salaryNum < 100000) {
      setError(" Current salary is very low. Predictions may be inaccurate for such small values.");
      setErrorKey(prev => prev + 1);
      setLoading(false);
      return;
    }

    const inflationClean =
      inflationRate !== "" && !isNaN(parseFloat(inflationRate))
        ? parseFloat(inflationRate)
        : null;

    const payload = {
      income: incomeNum,
      expenses: expenses.map(exp => ({
        ...exp,
        amount: parseFloat(exp.amount) || 0,
        frequency: parseFloat(exp.frequency) || 0,
        seasonal_flag: parseInt(exp.seasonal_flag),
      })),
      savings_goal: savingsGoalNum,
      current_salary: !isNaN(salaryNum) ? salaryNum : incomeNum,
      inflation_rate: inflationClean,
    };

    try {
      const res = await fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Request failed");

      const result = await res.json();
      setResult(result);
      setShowSuccess(true);
      setError(null);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch {
      setError("❌ Failed to fetch data. Check backend or internet.");
      setErrorKey(prev => prev + 1);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit} className="finance-form">
        <div className="form-header">
          <h2 className="form-title">📊 Financial Analysis</h2>
          <p className="form-subtitle">
            Enter your financial details for personalized insights
          </p>
        </div>

        <div className="input-section">
          <h3 className="section-title">💰 Income & Goals</h3>
          <div className="input-grid">
            <div className="input-group">
              <label className="input-label">Yearly Income</label>
              <input type="number" value={income} onChange={(e) => setIncome(e.target.value)} placeholder="₹ 0" className="form-input" required />
            </div>
            <div className="input-group">
              <label className="input-label">Yearly Savings Goal</label>
              <input type="number" value={savingsGoal} onChange={(e) => setSavingsGoal(e.target.value)} placeholder="₹ 0" className="form-input" required />
            </div>
            <div className="input-group">
              <label className="input-label">Current Salary</label>
              <input type="number" value={currentSalary} onChange={(e) => setCurrentSalary(e.target.value)} placeholder="₹ 0" className="form-input" />
            </div>
            <div className="input-group">
              <label className="input-label">Inflation Rate (Optional)</label>
              <input type="number" value={inflationRate} onChange={(e) => setInflationRate(e.target.value)} placeholder="%(auto/leave blank)" className="form-input" />
            </div>
          </div>
        </div>

        <div className="expenses-section">
          <div className="expenses-header">
            <h3 className="section-title">📋 Expenses</h3>
            <button type="button" onClick={addExpense} className="add-expense-btn">+ Add Expense</button>
          </div>

          <div className="expenses-list">
            {expenses.map((exp, index) => (
              <div key={index} className="expense-item">
                <div className="expense-inputs">
                  <div className="input-group">
                    <label className="input-label">Name</label>
                    <input type="text" value={exp.name} onChange={(e) => handleExpenseChange(index, "name", e.target.value)} className="form-input" placeholder="e.g., Rent" required />
                  </div>
                  <div className="input-group">
                    <label className="input-label">Amount</label>
                    <input type="number" value={exp.amount} onChange={(e) => handleExpenseChange(index, "amount", e.target.value)} className="form-input" required />
                  </div>
                  <div className="input-group">
                    <label className="input-label">Frequency</label>
                    <div className="frequency-with-unit">
                      <input type="number" value={exp.frequency} onChange={(e) => handleExpenseChange(index, "frequency", e.target.value)} className="form-input" required />
                      <select value={exp.unit} onChange={(e) => handleExpenseChange(index, "unit", e.target.value)} className="form-select frequency-unit">
                        <option value="monthly">/month</option>
                        <option value="yearly">/year</option>
                      </select>
                    </div>
                  </div>
                  <div className="input-group">
                    <label className="input-label">Seasonal</label>
                    <select value={exp.seasonal_flag} onChange={(e) => handleExpenseChange(index, "seasonal_flag", e.target.value)} className="form-select seasonal-select">
                      <option value={0}>No</option>
                      <option value={1}>Yes</option>
                    </select>
                  </div>
                </div>
                <button type="button" onClick={() => removeExpense(index)} className="remove-expense-btn" title="Remove expense">🗑️</button>
              </div>
            ))}
          </div>
        </div>

        {error && (
          <div key={errorKey} className="error-message">
            <span className="error-icon">⚠️</span>
            <span>{error}</span>
          </div>
        )}

        <div className="form-actions">
          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? (
              <>
                <span className="btn-loading">⏳</span>
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <span>🚀</span>
                <span>Analyze Finances</span>
              </>
            )}
          </button>
        </div>

        {loading && <div className="loading-container"><Loader /></div>}

        {showSuccess && (
          <div className="success-message">
            <span className="success-icon">✅</span>
            <span>Analysis Complete! Check your results below.</span>
          </div>
        )}
      </form>
    </div>
  );
}
