# data_handler.py
def collect_user_data():
    print("--- Personal Finance Data Input ---")

    # Collect income
    income = float(input("Enter your yearly income (in INR): "))

    # Collect enriched expense data (without seasonal flag)
    num_expenses = int(input("How many expense items do you want to enter? "))
    expenses = []
    for _ in range(num_expenses):
        name = input("Enter expense name: ")
        amount = float(input(f"Enter amount for {name} (in INR): "))
        freq = float(input(f"Enter purchase frequency per month for {name}: "))
        expenses.append((name, amount, freq, 0))  # Placeholder 0 for removed seasonal field

    # Savings goal
    savings_goal = float(input("Enter your yearly savings goal (in INR): "))

    # Current salary
    current_salary = float(input("Enter your current yearly salary (in INR): "))

    # Ask whether to use auto CPI
    use_auto_cpi = input("Do you want to auto-fetch inflation rate from CPI dataset? (y/n): ").strip().lower()
    if use_auto_cpi == 'y':
        inflation_rate = None
    else:
        inflation_rate = float(input("Enter expected inflation rate (in %): "))

    return income, expenses, savings_goal, current_salary, inflation_rate
