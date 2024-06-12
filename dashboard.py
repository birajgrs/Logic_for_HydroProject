# dashboard.py

import logic
import distribution
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from matplotlib.animation import FuncAnimation
import pandas as pd


def plot_pie_chart(data, title):
    # Filter out negative values
    filtered_data = {k: v for k, v in data.items() if v >= 0}
    labels = filtered_data.keys()
    sizes = filtered_data.values()
    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.axis('equal')
    plt.show()


def plot_bar_chart(data, title):
    labels = data.keys()
    values = data.values()
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(labels), y=list(values))
    plt.title(title)
    plt.ylabel('Amount')
    plt.xlabel('Sector')
    plt.show()


def plot_histogram(data, title):
    values = data.values()
    plt.figure(figsize=(10, 6))
    sns.histplot(list(values), bins=10, kde=True)
    plt.title(title)
    plt.xlabel('Amount')
    plt.ylabel('Frequency')
    plt.show()


def plot_scatter(data1, data2, title, xlabel, ylabel):
    labels = data1.keys()
    plt.figure(figsize=(10, 6))
    plt.scatter(data1.values(), data2.values(), c='blue', marker='o')
    for label, x, y in zip(labels, data1.values(), data2.values()):
        plt.annotate(label, xy=(x, y), xytext=(5, 5), textcoords='offset points')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def plot_line_chart(data1, data2, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    plt.plot(list(data1.keys()), list(data1.values()), marker='o', label='Revenue')
    plt.plot(list(data2.keys()), list(data2.values()), marker='x', label='Expenses')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()


def animate_bar_chart(data, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    labels = list(data.keys())
    values = list(data.values())
    bars = ax.bar(labels, values)

    def update(frame):
        for bar, new_value in zip(bars, values):
            bar.set_height(new_value)
        return bars

    ani = FuncAnimation(fig, update, frames=range(len(labels)), blit=False, repeat=False)
    plt.title(title)
    plt.xlabel('Sector')
    plt.ylabel('Amount')
    plt.show()


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

    # Prepare data for visualizations
    sector_revenues = {sector['name']: sector['revenue'] for sector in sectors}
    sector_expenses = {sector['name']: sector['other_expenses'] + sector['paid_for_nea'] for sector in sectors}

    # Plot visualizations
    plot_pie_chart(sector_revenues, "Sector Revenues Distribution")
    plot_bar_chart(sector_expenses, "Sector Expenses Distribution")
    plot_histogram(sector_expenses, "Distribution of Sector Expenses")
    plot_scatter(sector_revenues, sector_expenses, "Revenue vs. Expenses by Sector", "Revenue", "Expenses")
    plot_line_chart(sector_revenues, sector_expenses, "Revenue and Expenses Over Time", "Sector", "Amount")
    animate_bar_chart(sector_revenues, "Animated Sector Revenues")

    # Display sector info
    distribution.display_sector_info(sectors)


if __name__ == "__main__":
    main()
