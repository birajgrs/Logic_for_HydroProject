import math

def get_user_input():
    initial_investment = float(input("Enter the initial investment: "))
    total_investment = float(input("Enter the total investment for constructing full power houses: "))
    discount_rate = float(input("Enter the discount rate (as a decimal, e.g., 0.1 for 10%): "))
    operational_days = int(input("Enter the number of operational days per year: "))
    project_lifetime = int(input("Enter the project lifetime in years: "))

    sectors = []
    sector_names = ["public_sector", "hospital", "railway_sector", "oil_corporation"]
    for sector_name in sector_names:
        other_expenses = float(input(f"Enter the other expenses for {sector_name}: "))
        paid_for_nea = float(input(f"Enter the Paid_for_NEA for {sector_name}: "))
        sectors.append({"name": sector_name, "other_expenses": other_expenses, "paid_for_nea": paid_for_nea})

    return initial_investment, total_investment, discount_rate, operational_days, project_lifetime, sectors


def calculate_roi(initial_investment, total_expenses, total_income):
    if total_income == 0:
        return float('inf')
    return (initial_investment + total_expenses) / total_income


def calculate_npv(initial_investment, total_income, total_expenses, discount_rate, operational_days, project_lifetime):
    npv = -initial_investment
    for year in range(1, project_lifetime + 1):
        discounted_cash_flow = (total_income - total_expenses) / operational_days / ((1 + discount_rate) ** year)
        npv += discounted_cash_flow
    return npv


def calculate_profitability_index(initial_investment, total_income, total_expenses, discount_rate, operational_days, project_lifetime):
    present_value_of_cash_flows = sum((total_income - total_expenses) / operational_days / ((1 + discount_rate) ** year) for year in range(1, project_lifetime + 1))
    return present_value_of_cash_flows / initial_investment


def calculate_break_even_point(fixed_costs, price_per_unit, variable_cost_per_unit):
    return fixed_costs / (price_per_unit - variable_cost_per_unit)
