
import logic
import distribution
import time
import os


def clear_screen():
    # Clear the console screen for better readability
    os.system('cls' if os.name == 'nt' else 'clear')


def print_line():
    print("=" * 50)


def text_based_pie_chart(data, title):
    total = sum(data.values())
    print_line()
    print(f"{title}")
    print_line()
    for key, value in data.items():
        percentage = (value / total) * 100
        bar = '*' * int(percentage // 2)
        print(f"{key:20}: {bar} {percentage:.2f}%")


def text_based_bar_chart(data, title):
    print_line()
    print(f"{title}")
    print_line()
    for key, value in data.items():
        bar = '*' * (value // 1000)  # Assuming the values are large, adjust as needed
        print(f"{key:20}: {bar} {value}")


def text_based_animation(data, title):
    print_line()
    print(f"{title}")
    print_line()
    for key, value in data.items():
        bar = '*' * (value // 1000)  # Adjust scale as needed
        for i in range(1, len(bar) + 1):
            print(f"{key:20}: {bar[:i]}")
            time.sleep(0.05)
            if i < len(bar):
                print("\033[F", end='')  # Move cursor up one line to overwrite


def main():
    initial_investment, total_investment, discount_rate, operational_days, project_lifetime, sectors = logic.get_user_input()

    # Adjust distribution
    sectors = distribution.adjust_distribution(sectors)

    # Before adjustment calculations
    total_daily_income = sum(sector['paid_for_nea'] for sector in sectors)
    total_daily_expenses = sum(sector['other_expenses'] + sector['paid_for_nea'] for sector in sectors)

    roi_time_before = logic.calculate_roi(initial_investment, total_daily_expenses, total_daily_income)
    npv_before = logic.calculate_npv(initial_investment, total_daily_income, total_daily_expenses, discount_rate,
                                     operational_days, project_lifetime)
    profitability_index_before = logic.calculate_profitability_index(initial_investment, total_daily_income,
                                                                     total_daily_expenses, discount_rate,
                                                                     operational_days, project_lifetime)

    # After adjustment calculations
    roi_time_after, npv_after, profitability_index_after = distribution.calculate_combined_values(sectors,
                                                                                                  total_investment,
                                                                                                  discount_rate,
                                                                                                  operational_days,
                                                                                                  project_lifetime)

    total_daily_income_after = sum(sector['paid_for_nea'] * sector['adjusted_percentage'] for sector in sectors)
    total_daily_expenses_after = sum(
        (sector['other_expenses'] + sector['paid_for_nea']) * sector['adjusted_percentage'] for sector in sectors)

    # Clear screen and print dashboard
    clear_screen()

    print("ROI, NPV, and Profitability Index Before and After Distribution Adjustment")
    print_line()
    print(f"Before Adjustment:")
    print(f"ROI Time: {roi_time_before:.2f} days")
    print(f"NPV: {npv_before:.2f}")
    print(f"Profitability Index: {profitability_index_before:.2f}")

    print_line()
    print(f"After Adjustment:")
    print(f"ROI Time: {roi_time_after:.2f} days")
    print(f"NPV: {npv_after:.2f}")
    print(f"Profitability Index: {profitability_index_after:.2f}")

    # Sector data visualization
    sector_revenues = {sector['name']: sector['revenue'] for sector in sectors}
    sector_expenses = {sector['name']: sector['other_expenses'] + sector['paid_for_nea'] for sector in sectors}

    text_based_pie_chart(sector_revenues, "Sector Revenues Distribution")
    text_based_bar_chart(sector_expenses, "Sector Expenses Distribution")

    print_line()
    print("Animated Bar Chart for Sector Revenues:")
    text_based_animation(sector_revenues, "Animated Sector Revenues")

    # Display sector info
    distribution.display_sector_info(sectors)


if __name__ == "__main__":
    main()
