# distribution.py

import importlib
import logic

def get_sector_data():
    sectors = {
        "public_sector": {"percentage": 0.25, "daily_income": 10000, "daily_expenses": 5000},
        "hospital": {"percentage": 0.25, "daily_income": 15000, "daily_expenses": 7000},
        "railway_sector": {"percentage": 0.25, "daily_income": 20000, "daily_expenses": 8000},
        "oil_corporation": {"percentage": 0.25, "daily_income": 30000, "daily_expenses": 10000},
    }
    return sectors

def adjust_distribution(sectors):
    total_percentage = sum(sector["percentage"] for sector in sectors.values())

    for sector_name, sector_data in sectors.items():
        revenue = sector_data["daily_income"] - sector_data["daily_expenses"]
        sector_data["revenue"] = revenue
        sector_data["adjusted_percentage"] = sector_data["percentage"] + (revenue / total_percentage) * 0.1

    # Normalize percentages to sum up to 1
    total_adjusted_percentage = sum(sector["adjusted_percentage"] for sector in sectors.values())
    for sector_name, sector_data in sectors.items():
        sector_data["adjusted_percentage"] /= total_adjusted_percentage

    return sectors

def calculate_combined_values(sectors, total_investment, discount_rate, operational_days, project_lifetime):
    combined_daily_income = sum(sector["daily_income"] * sector["adjusted_percentage"] for sector in sectors.values())
    combined_daily_expenses = sum(sector["daily_expenses"] * sector["adjusted_percentage"] for sector in sectors.values())

    roi_time = logic.calculate_roi(total_investment, combined_daily_expenses, combined_daily_income)
    npv = logic.calculate_npv(total_investment, combined_daily_income, combined_daily_expenses, discount_rate, operational_days, project_lifetime)
    profitability_index = logic.calculate_profitability_index(total_investment, combined_daily_income, combined_daily_expenses, discount_rate, operational_days, project_lifetime)

    return roi_time, npv, profitability_index

def display_sector_info(sectors):
    sorted_sectors = sorted(sectors.items(), key=lambda x: x[1]["revenue"], reverse=True)
    most_revenue_sector = sorted_sectors[0]
    least_revenue_sector = sorted_sectors[-1]

    print("\nSector Revenue and Distribution:")
    for sector_name, sector_data in sorted_sectors:
        print(f"{sector_name}: Revenue = {sector_data['revenue']:.2f}, Adjusted Percentage = {sector_data['adjusted_percentage']*100:.2f}%")

    print(f"\nSector with the Most Revenue: {most_revenue_sector[0]} with Revenue = {most_revenue_sector[1]['revenue']:.2f}")
    print(f"Sector with the Least Revenue: {least_revenue_sector[0]} with Revenue = {least_revenue_sector[1]['revenue']:.2f}")

def main():
    # Fetch user input and sector data
    initial_investment, total_investment, daily_expenses, daily_income, discount_rate, operational_days, project_lifetime = logic.get_user_input()
    sectors = get_sector_data()

    # Adjust distribution and calculate combined values
    sectors = adjust_distribution(sectors)
    roi_time, npv, profitability_index = calculate_combined_values(sectors, total_investment, discount_rate, operational_days, project_lifetime)

    # Display sector info
    display_sector_info(sectors)

    print("\nAfter distribution adjustment:")
    print(f"ROI Time: {roi_time:.2f} days")
    print(f"NPV: {npv:.2f}")
    print(f"Profitability Index: {profitability_index:.2f}")

    # Break-even analysis
    fixed_costs = total_investment
    price_per_unit = daily_income / operational_days
    variable_cost_per_unit = daily_expenses / operational_days
    break_even_units = logic.calculate_break_even_point(fixed_costs, price_per_unit, variable_cost_per_unit)
    print(f"Break-Even Point: {break_even_units:.2f} units/day")

if __name__ == "__main__":
    main()
