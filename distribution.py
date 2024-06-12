import logic
import math


def get_sector_data(sectors):
    total_paid_for_nea = sum(sector["paid_for_nea"] for sector in sectors)
    for sector in sectors:
        revenue = sector["paid_for_nea"] - sector["other_expenses"]
        sector["revenue"] = revenue
    return sectors


def adjust_distribution(sectors):
    total_revenue = sum(sector["revenue"] for sector in sectors)

    for sector in sectors:
        sector["adjusted_percentage"] = sector["revenue"] / total_revenue if total_revenue != 0 else 0

    return sectors


def calculate_combined_values(sectors, total_investment, discount_rate, operational_days, project_lifetime):
    combined_daily_income = sum(sector["paid_for_nea"] * sector["adjusted_percentage"] for sector in sectors)
    combined_daily_expenses = sum(
        (sector["other_expenses"] + sector["paid_for_nea"]) * sector["adjusted_percentage"] for sector in sectors)

    roi_time = logic.calculate_roi(total_investment, combined_daily_expenses, combined_daily_income)
    npv = logic.calculate_npv(total_investment, combined_daily_income, combined_daily_expenses, discount_rate,
                              operational_days, project_lifetime)
    profitability_index = logic.calculate_profitability_index(total_investment, combined_daily_income,
                                                              combined_daily_expenses, discount_rate, operational_days,
                                                              project_lifetime)

    return roi_time, npv, profitability_index


def display_sector_info(sectors):
    sorted_sectors = sorted(sectors, key=lambda x: x["revenue"], reverse=True)
    most_revenue_sector = sorted_sectors[0]
    least_revenue_sector = sorted_sectors[-1]

    print("\nSector Revenue and Distribution:")
    for sector in sorted_sectors:
        print(
            f"{sector['name']}: Revenue = {sector['revenue']:.2f}, Adjusted Percentage = {sector['adjusted_percentage'] * 100:.2f}%")

    print(
        f"\nSector with the Most Revenue: {most_revenue_sector['name']} with Revenue = {most_revenue_sector['revenue']:.2f}")
    print(
        f"Sector with the Least Revenue: {least_revenue_sector['name']} with Revenue = {least_revenue_sector['revenue']:.2f}")


def main():
    initial_investment, total_investment, discount_rate, operational_days, project_lifetime, sectors = logic.get_user_input()

    # Before adjustment
    total_daily_income = sum(sector['paid_for_nea'] for sector in sectors)
    total_daily_expenses = sum(sector['other_expenses'] + sector['paid_for_nea'] for sector in sectors)

    roi_time_before = logic.calculate_roi(initial_investment, total_daily_expenses, total_daily_income)
    npv_before = logic.calculate_npv(initial_investment, total_daily_income, total_daily_expenses, discount_rate,
                                     operational_days, project_lifetime)
    profitability_index_before = logic.calculate_profitability_index(initial_investment, total_daily_income,
                                                                     total_daily_expenses, discount_rate,
                                                                     operational_days, project_lifetime)

    fixed_costs = total_investment
    price_per_unit = total_daily_income / operational_days
    variable_cost_per_unit = total_daily_expenses / operational_days
    break_even_units_before = logic.calculate_break_even_point(fixed_costs, price_per_unit, variable_cost_per_unit)

    print("\nBefore distribution adjustment:")
    print(f"ROI Time: {roi_time_before:.2f} days")
    print(f"NPV: {npv_before:.2f}")
    print(f"Profitability Index: {profitability_index_before:.2f}")
    print(f"Break-Even Point: {break_even_units_before:.2f} units/day")
    print("Sector details before adjustment:")
    for sector in sectors:
        print(
            f"{sector['name']}: Daily Income (Paid_for_NEA) = {sector['paid_for_nea']}, Daily Expenses (other expenses + Paid_for_NEA) = {sector['other_expenses'] + sector['paid_for_nea']}")

    # Adjust distribution
    sectors = adjust_distribution(sectors)

    # After adjustment
    roi_time_after, npv_after, profitability_index_after = calculate_combined_values(sectors, total_investment,
                                                                                     discount_rate, operational_days,
                                                                                     project_lifetime)

    total_daily_income_after = sum(sector['paid_for_nea'] * sector['adjusted_percentage'] for sector in sectors)
    total_daily_expenses_after = sum(
        (sector['other_expenses'] + sector['paid_for_nea']) * sector['adjusted_percentage'] for sector in sectors)

    price_per_unit_after = total_daily_income_after / operational_days
    variable_cost_per_unit_after = total_daily_expenses_after / operational_days
    break_even_units_after = logic.calculate_break_even_point(fixed_costs, price_per_unit_after,
                                                              variable_cost_per_unit_after)

    print("\nAfter distribution adjustment:")
    print(f"ROI Time: {roi_time_after:.2f} days")
    print(f"NPV: {npv_after:.2f}")
    print(f"Profitability Index: {profitability_index_after:.2f}")
    print(f"Break-Even Point: {break_even_units_after:.2f} units/day")

    # Display sector info
    display_sector_info(sectors)


if __name__ == "__main__":
    main()
