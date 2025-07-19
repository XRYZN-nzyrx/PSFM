# expense_classifier.py
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def train_expense_model(dataset_path):
    df = pd.read_csv(dataset_path)

    # Use only relevant features: Monthly_Expense and Purchase_Frequency
    X = df[["Monthly_Expense", "Purchase_Frequency"]]
    y = df["Label"]

    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Train Logistic Regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    return model, scaler

# Rule-based essential keywords
ESSENTIAL_KEYWORDS = ["rent", "emi", "grocery", "groceries", "transport","mediclaim", "insurance", "medicine", "electricity", "water"]

def categorize_expenses(expenses, model, scaler):
    result = []
    for item in expenses:
        name, amount, freq, unit, seasonal_flag = item

        if seasonal_flag == 1:
            label = "Luxury"
        elif any(keyword in name.lower() for keyword in ESSENTIAL_KEYWORDS):
            label = "Essential"
        else:
            features = scaler.transform([[amount, freq]])
            prediction = model.predict(features)[0]
            label = "Essential" if prediction == 0 else "Luxury"

        result.append((name, amount, label))
    return result

