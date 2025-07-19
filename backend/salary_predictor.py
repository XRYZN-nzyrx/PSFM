import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from datetime import datetime
from backend.cpi_utils import get_yearly_inflation_rate
import numpy as np

def predict_future_salary(current_salary, inflation_rate, dataset_path):
    # Load and clean dataset
    df = pd.read_csv(dataset_path)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df.dropna(subset=['Timestamp'], inplace=True)
    df['Year'] = df['Timestamp'].dt.year

    # Sort and compute previous salary
    df.sort_values(['Individual_ID', 'Timestamp'], inplace=True)
    df['Prev_Salary'] = df.groupby('Individual_ID')['Salary'].shift(1)
    df.dropna(subset=['Prev_Salary'], inplace=True)

    # Aggregate to yearly level
    yearly_df = df.groupby(['Individual_ID', 'Year']).agg({
        'Salary': 'mean',
        'Prev_Salary': 'mean',
        'Inflation_Rate': 'mean',
        'GDP_Growth': 'mean',
        'Unemployment_Rate': 'mean'
    }).reset_index()

    # Add features
    yearly_df['TimeIndex'] = yearly_df['Year'] - yearly_df['Year'].min()
    yearly_df['LogSalary'] = np.log1p(yearly_df['Salary'])

    # Feature matrix and labels
    X = yearly_df[['TimeIndex', 'Inflation_Rate', 'GDP_Growth', 'Unemployment_Rate', 'Prev_Salary']]
    y = yearly_df['LogSalary']

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    model = xgb.XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        verbosity=0
    )
    model.fit(X_train, y_train)

    # Prepare prediction input for next year
    last = yearly_df.iloc[-1]
    next_year = int(last['Year'] + 1)
    next_time_index = int(last['TimeIndex'] + 1)

    # Use user-provided inflation rate if valid, otherwise fallback
    if inflation_rate is None or not isinstance(inflation_rate, (int, float)) or np.isnan(inflation_rate):
        inflation_rate = get_yearly_inflation_rate(next_year)
        if inflation_rate is None:
            inflation_rate = float(last['Inflation_Rate'])  # fallback

    prediction_input = [[
        next_time_index,
        inflation_rate,
        float(last['GDP_Growth']),
        float(last['Unemployment_Rate']),
        float(current_salary)
    ]]
    prediction_input_scaled = scaler.transform(prediction_input)

    predicted_log_salary = model.predict(prediction_input_scaled)[0]
    predicted_salary = float(np.expm1(predicted_log_salary))

    # Inflation-adjusted fallback
    inflation_adjusted = float(current_salary) * (1 + inflation_rate / 100)

    # Weighting model vs inflation logic
    if current_salary < 500000:
        weight_model = 0.03
    elif current_salary < 1000000:
        weight_model = 0.02
    else:
        weight_model = 0.01

    final_salary = round(
        (1 - weight_model) * inflation_adjusted + weight_model * predicted_salary,
        2
    )

    print(f"📈 Predicted Salary (Next Year): ₹{final_salary}")
    return float(final_salary)  
