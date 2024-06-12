import logic
import math


def get_sector_data(sectors):
    total_paid_for_nea = sum(sector["paid_for_nea"] for sector in sectors)
    for sector in sectors:
        revenue = sector["paid_for_nea"] - sector["other_expenses"]
        sector["revenue"] = revenue
        sector["adjusted_percentage"] = sector["paid_for_nea"] / total_paid_for_nea if total_paid_for_nea != 0 else 0
    return sectors


def adjust_distribution(sectors):
    total_percentage = sum(sector["adjusted_percentage"] for sector in sectors)

    for sector in sectors:
        revenue = sector["revenue"]
        sector["adjusted_percentage"] += (revenue / total_percentage) * 0.1 if total_percentage != 0 else 0

    # Normalize percentages to sum up to 1
    total_adjusted_percentage = sum(sector["adjusted_percentage"] for sector in sectors)
    for sector in sectors:
        sector["adjusted_percentage"] /= total_adjusted_percentage if total_adjusted_percentage != 0 else 1

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
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    def predict(coefs, x):
        return sigmoid(coefs[0] + coefs[1] * x)

    def loss(coefs):
        return sum((data[i] - predict(coefs, i)) ** 2 for i in range(len(data))) / len(data)

    initial_coefs = [0, 0]

    # Simple gradient descent for optimization
    learning_rate = 0.01
    num_iterations = 10000

    coefs = initial_coefs
    for _ in range(num_iterations):
        gradients = [0, 0]
        for i in range(len(data)):
            prediction = predict(coefs, i)
            error = data[i] - prediction
            gradients[0] += -2 * error * prediction * (1 - prediction)
            gradients[1] += -2 * error * prediction * (1 - prediction) * i

        coefs[0] -= learning_rate * gradients[0] / len(data)
        coefs[1] -= learning_rate * gradients[1] / len(data)

    return coefs


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
    display_sector_info(sectors)

    # Linear and logistic regression data
    roi_times = [roi_time_before, roi_time_after]
    npvs = [npv_before, npv_after]
    profitability_indices = [profitability_index_before, profitability_index_after]

    # Linear Regression
    a_roi, b_roi = linear_regression(roi_times)
    a_npv, b_npv = linear_regression(npvs)
    a_pi, b_pi = linear_regression(profitability_indices)

    print("\nLinear Regression Results:")
    print(f"ROI Time: y = {a_roi:.2f}x + {b_roi:.2f}")
    print(f"NPV: y = {a_npv:.2f}x + {b_npv:.2f}")
    print(f"Profitability Index: y = {a_pi:.2f}x + {b_pi:.2f}")

    # Logistic Regression
    coefs_roi = logistic_regression(roi_times)
    coefs_npv = logistic_regression(npvs)
    coefs_pi = logistic_regression(profitability_indices)

    print("\nLogistic Regression Results:")
    print(f"ROI Time: y = 1 / (1 + e^(-({coefs_roi[0]:.2f} + {coefs_roi[1]:.2f}x)))")
    print(f"NPV: y = 1 / (1 + e^(-({coefs_npv[0]:.2f} + {coefs_npv[1]:.2f}x)))")
    print(f"Profitability Index: y = 1 / (1 + e^(-({coefs_pi[0]:.2f} + {coefs_pi[1]:.2f}x)))")


if __name__ == "__main__":
    main()
