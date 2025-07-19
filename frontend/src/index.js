import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Global styles
import './components/styles/styles.css';
import './App.css';
import './components/styles/ExpenseForm.css';
import './components/styles/ResultSummary.css';
import './components/styles/Loader.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Optional performance monitoring
//reportWebVitals();
