import json
from datetime import datetime

class Expense:
    """Class to represent an expense entry."""
    def __init__(self, amount, category, date):
        self.amount = amount
        self.category = category
        self.date = datetime.strptime(date, '%Y-%m-%d')

class ExpenseTracker:
    """Class to manage expenses and categories."""
    def __init__(self):
        self.expenses = []
        self.categories = set()

    def add_expense(self, amount, category, date):
        """Add a new expense to the tracker."""
        if category not in self.categories:
            print(f"Category '{category}' not found. Please add it first.")
            return
        expense = Expense(amount, category, date)
        self.expenses.append(expense)

    def add_category(self, category):
        """Add a new category to the tracker."""
        self.categories.add(category)

    def calculate_monthly_totals(self, year, month):
        """Calculate total expenses for each category for a given month."""
        monthly_totals = {}
        for expense in self.expenses:
            if expense.date.year == year and expense.date.month == month:
                if expense.category not in monthly_totals:
                    monthly_totals[expense.category] = 0
                monthly_totals[expense.category] += expense.amount
        return monthly_totals

    def view_categories(self):
        """View all expense categories."""
        return list(self.categories)

def main():
    tracker = ExpenseTracker()
    
    # Add categories
    tracker.add_category("Food")
    tracker.add_category("Transport")
    tracker.add_category("Utilities")
    
    # Add expenses
    tracker.add_expense(50, "Food", "2023-10-01")
    tracker.add_expense(20, "Transport", "2023-10-02")
    tracker.add_expense(100, "Utilities", "2023-10-03")
    tracker.add_expense(30, "Food", "2023-10-04")
    
    # Calculate monthly totals
    totals = tracker.calculate_monthly_totals(2023, 10)
    print("Monthly Totals for October 2023:")
    for category, total in totals.items():
        print(f"{category}: ${total}")

if __name__ == '__main__':
    main()