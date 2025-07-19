def calculate_savings_potential(income, expenses):
    total_expenses = 0
    for _, amount, freq, unit, _ in expenses:  # <- Unpack all 5 items
        if unit == "yearly":
            total_expenses += amount * freq
        else:
            total_expenses += amount * freq * 12
    return income - total_expenses


def check_savings_goal(savings_potential, savings_goal):
    if savings_potential >= savings_goal:
        print("✅ Your savings potential aligns with your goal.")
        return True
    else:
        print("⚠️ Your savings goal is higher than your savings potential.")
        return False


def suggest_savings_goal(savings_potential, savings_goal):
    if savings_potential >= savings_goal:
        return savings_goal
    else:
        suggested = round(savings_potential * 0.9, 2)  # Keep a 10% buffer
        print(f"💡 Suggested new savings goal: {suggested}")
        return suggested
