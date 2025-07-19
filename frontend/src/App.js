import React, { useState } from "react";
import FinanceForm from "./components/ExpenseForm";
import ResultsDisplay from "./components/ResultSummary";
import "./App.css";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="app-container">
      <div className="glass-card">
        <div className="header-section">
          <h1 className="title">💰 Personal Finance Analyzer</h1>
          <p className="subtitle">Smart insights for your financial future</p>
        </div>
        
        <div className="content-section">
          <FinanceForm setResult={setResult} />
          {result && (
            <div className="results-section">
              <ResultsDisplay data={result} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;