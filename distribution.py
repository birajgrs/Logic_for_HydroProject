import logic


def get_sector_data(sectors):
    total_percentage = sum(sector["paid_for_nea"] for sector in sectors)
    for sector in sectors:
        revenue = sector["paid_for_nea"] - sector["other_expenses"]
        sector["revenue"] = revenue
        sector["adjusted_percentage"] = sector["paid_for_nea"] / total_percentage
    return sectors


def adjust_distribution(sectors):
    total_percentage = sum(sector["adjusted_percentage"] for sector in sectors)

    for sector in sectors:
        revenue = sector["revenue"]
        sector["adjusted_percentage"] += (revenue / total_percentage) * 0.1

    # Normalize percentages to sum up to 1
    total_adjusted_percentage = sum(sector["adjusted_percentage"] for sector in sectors)
    for sector in sectors:
        sector["adjusted_percentage"] /= total_adjusted_percentage

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


def linear_regression(data):
    n = len(data)
    x_sum = sum(i for i in range(n))
    y_sum = sum(data)
    xy_sum = sum(i * data[i] for i in range(n))
    x_squared_sum = sum(i ** 2 for i in range(n))

    a = (n * xy_sum - x_sum * y_sum) / (n * x_squared_sum - x_sum ** 2)
    b = (y_sum - a * x_sum) / n

    return a, b


def logistic_regression(data):
    import math

    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    def predict(coefs, x):
        return sigmoid(coefs[0] + coefs[1] * x)

    def loss(coefs):
        return sum((data[i] - predict(coefs, i)) ** 2 for i in range(len(data))) / len(data)

    initial_coefs = [0, 0]
    from scipy.optimize import minimize
    result = minimize(loss, initial_coefs)
    return result.x


def main():
    initial_investment, total_investment, discount_rate, operational_days, project_lifetime, sectors = logic.get_user_input()
    sectors = get_sector_data(sectors)
    sectors = adjust_distribution(sectors)

    roi_time, npv, profitability_index = calculate_combined_values(sectors, total_investment, discount_rate,
                                                                   operational_days, project_lifetime)

    display_sector_info(sectors)

    print("\nAfter distribution adjustment:")
    print(f"ROI Time: {roi_time:.2f} days")
    print(f"NPV: {npv:.2f}")
    print(f"Profitability Index: {profitability_index:.2f}")

    fixed_costs = total_investment
    total_daily_income = sum(sector['paid_for_nea'] for sector in sectors)
    total_daily_expenses = sum(sector['other_expenses'] + sector['paid_for_nea'] for sector in sectors)
    price_per_unit = total_daily_income / operational_days
    variable_cost_per_unit = total_daily_expenses / operational_days
    break_even_units = logic.calculate_break_even_point(fixed_costs, price_per_unit, variable_cost_per_unit)
    print(f"Break-Even Point: {break_even_units:.2f} units/day")

    # Prediction (regression)
    revenue_data = [sector["revenue"] for sector in sectors]
    a, b = linear_regression(revenue_data)
    logistic_coefs = logistic_regression(revenue_data)

    print("\nLinear Regression Coefficients:")
    print(f"Slope (a): {a:.2f}, Intercept (b): {b:.2f}")

    print("\nLogistic Regression Coefficients:")
    print(f"Coefficients: {logistic_coefs}")


if __name__ == "__main__":
    main()
