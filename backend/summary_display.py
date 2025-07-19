# summary_display.py
def display_summary(expenses, original_goal, suggested_goal, savings_potential, predicted_salary, aligned):
    print("\n===== Financial Summary =====")

    # Expense Breakdown
    essential_total = sum(amount for _, amount, category in expenses if category == "Essential")
    luxury_total = sum(amount for _, amount, category in expenses if category == "Luxury")
    
    print("\nExpense Categorization:")
    for name, amount, category in expenses:
        print(f"- {name}: INR {amount} → {category}")

    print("\nBreakdown:")
    print(f"Total Essential Expenses: INR {essential_total}")
    print(f"Total Luxury Expenses   : INR {luxury_total}")

    print("\nSavings Analysis:")
    print(f"Potential Savings        : INR {savings_potential}")
    print(f"Original Savings Goal    : INR {original_goal}")
    if not aligned:
        print(f"💡 Suggested Savings Goal : INR {suggested_goal}")

    print("\nSalary Prediction:")
    print(f"Predicted Salary Next Yr : INR {predicted_salary}")

    print("\n✅ Summary Complete.")