def get_user_input():
    initial_investment = float(input("Enter the initial investment: "))
    total_investment = float(input("Enter the total investment for constructing full power houses: "))
    daily_expenses = float(input("Enter the daily expenses: "))
    daily_income = float(input("Enter the daily income: "))
    discount_rate = float(input("Enter the discount rate (as a decimal, e.g., 0.1 for 10%): "))
    operational_days = int(input("Enter the number of operational days per year: "))
    project_lifetime = int(input("Enter the project lifetime in years: "))

    return initial_investment, total_investment, daily_expenses, daily_income, discount_rate, operational_days, project_lifetime

def calculate_roi(initial_investment, daily_expenses, daily_income):
    net_daily_profit = daily_income - daily_expenses
    roi_time = initial_investment / net_daily_profit
    return roi_time

def calculate_npv(initial_investment, daily_income, daily_expenses, discount_rate, operational_days, project_lifetime):
    npv = 0
    for t in range(project_lifetime):
        cash_flow = (daily_income - daily_expenses) * operational_days
        npv += cash_flow / (1 + discount_rate) ** (t + 1)
    npv -= initial_investment
    return npv

def calculate_profitability_index(initial_investment, daily_income, daily_expenses, discount_rate, operational_days, project_lifetime):
    pv_cash_flows = 0
    for t in range(project_lifetime):
        cash_flow = (daily_income - daily_expenses) * operational_days
        pv_cash_flows += cash_flow / (1 + discount_rate) ** (t + 1)
    pi = pv_cash_flows / initial_investment
    return pi

def calculate_break_even_point(fixed_costs, price_per_unit, variable_cost_per_unit):
    break_even_units = fixed_costs / (price_per_unit - variable_cost_per_unit)
    return break_even_units

# Main script
if __name__ == "__main__":
    initial_investment, total_investment, daily_expenses, daily_income, discount_rate, operational_days, project_lifetime = get_user_input()

    roi_time = calculate_roi(initial_investment, daily_expenses, daily_income)
    npv = calculate_npv(initial_investment, daily_income, daily_expenses, discount_rate, operational_days, project_lifetime)
    profitability_index = calculate_profitability_index(initial_investment, daily_income, daily_expenses, discount_rate, operational_days, project_lifetime)

    fixed_costs = total_investment
    price_per_unit = daily_income / operational_days
    variable_cost_per_unit = daily_expenses / operational_days
    break_even_units = calculate_break_even_point(fixed_costs, price_per_unit, variable_cost_per_unit)

    print(f"ROI Time: {roi_time:.2f} days")
    print(f"NPV: {npv:.2f}")
    print(f"Profitability Index: {profitability_index:.2f}")
    print(f"Break-Even Point: {break_even_units:.2f} units/day")
