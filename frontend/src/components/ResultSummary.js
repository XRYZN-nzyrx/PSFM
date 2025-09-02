import React from "react";
import './styles/ResultSummary.css';

function ResultsDisplay({ data }) {
  if (!data) return null;

  const {
    categorized_expenses,
    essential_total,
    luxury_total,
    savings_potential,
    goal_alignment,
    suggested_goal,
    predicted_salary,
  } = data;

  const formatCurrency = (value) =>
    `₹${Number(value).toLocaleString("en-IN", { minimumFractionDigits: 2 })}`;

  return (
    <div className="results-container">
      <h2 className="section-title">📊 Results Summary</h2>

      <div className="results-section">
        <h3>💡 Expense Categorization:</h3>
        <ul>
          {categorized_expenses.map(([name, amount, category], idx) => (
            <li key={idx}>
              <strong>{name}</strong>: {formatCurrency(amount)} →{" "}
              <span className={category === "Essential" ? "essential" : "luxury"}>
                {category}
              </span>
            </li>
          ))}
        </ul>
      </div>

      <div className="results-section">
        <h3>📌 Expense Totals:</h3>
        <p>✅ Essential: {formatCurrency(essential_total)}</p>
        <p>💎 Luxury: {formatCurrency(luxury_total)}</p>
      </div>
        
      <div className="results-section">
        <h3>💰 Savings Analysis:</h3>
        <p>Estimated Savings Potential: {formatCurrency(savings_potential)}</p>
        <p>
          Goal Status:{" "}
          {goal_alignment ? "✔️ Goal Achievable" : "❌ Goal Too High"}
        </p>
        {!goal_alignment && (
          <p>💡 Suggested Goal: {formatCurrency(suggested_goal)}</p>
        )}
      </div>

      <div className="results-section">
        <h3>📈 Predicted Salary (Next Year):</h3>
        <p>{formatCurrency(predicted_salary)}</p>
      </div>
    </div>
  );
}

export default ResultsDisplay;