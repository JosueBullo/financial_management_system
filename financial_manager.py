import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import os

class FinancialManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Management System")
        self.root.geometry("800x600")

        self.create_main_menu()

    def create_main_menu(self):
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=20)

        tk.Label(menu_frame, text="Financial Management System", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Button(menu_frame, text="Add Transaction", command=self.add_transaction_window).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(menu_frame, text="View Transactions", command=self.view_transactions_window).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(menu_frame, text="Generate Summary", command=self.generate_summary_window).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(menu_frame, text="Visualize Data", command=self.visualize_data_window).grid(row=2, column=1, padx=10, pady=10)

    # Function to add a transaction
    def add_transaction_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Transaction")

        tk.Label(add_window, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5)
        date_entry = tk.Entry(add_window)
        date_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Category:").grid(row=1, column=0, padx=10, pady=5)
        category_entry = tk.Entry(add_window)
        category_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Amount:").grid(row=2, column=0, padx=10, pady=5)
        amount_entry = tk.Entry(add_window)
        amount_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Description:").grid(row=3, column=0, padx=10, pady=5)
        description_entry = tk.Entry(add_window)
        description_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Type:").grid(row=4, column=0, padx=10, pady=5)
        transaction_type = ttk.Combobox(add_window, values=["Income", "Expense"])
        transaction_type.grid(row=4, column=1, padx=10, pady=5)

        def save_transaction():
            date = date_entry.get()
            category = category_entry.get()
            amount = amount_entry.get()
            description = description_entry.get()
            type_ = transaction_type.get()

            if not all([date, category, amount, description, type_]):
                messagebox.showerror("Error", "All fields must be filled out.")
                return
            
            try:
                amount = float(amount)
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number.")
                return

            # Save to CSV
            with open('financial_data.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([date, category, amount, description, type_])
            messagebox.showinfo("Success", "Transaction added successfully!")
            add_window.destroy()

        tk.Button(add_window, text="Save Transaction", command=save_transaction).grid(row=5, column=0, columnspan=2, pady=10)

    # Function to view transactions
    def view_transactions_window(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View Transactions")

        tree = ttk.Treeview(view_window, columns=("Date", "Category", "Amount", "Description", "Type"), show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Category", text="Category")
        tree.heading("Amount", text="Amount")
        tree.heading("Description", text="Description")
        tree.heading("Type", text="Type")
        tree.pack(fill=tk.BOTH, expand=True)

        # Load data from CSV
        if os.path.exists('financial_data.csv'):
            with open('financial_data.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    tree.insert("", tk.END, values=row)

    # Function to generate a summary of transactions
    def generate_summary_window(self):
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Generate Summary")

        total_income = 0
        total_expenses = 0

        if os.path.exists('financial_data.csv'):
            with open('financial_data.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    # Check if the row has the expected number of columns
                    if len(row) < 5:
                        continue  # Skip rows with insufficient data
                    try:
                        amount = float(row[2])  # Amount is in the third column
                        if row[4] == "Income":
                            total_income += amount
                        elif row[4] == "Expense":
                            total_expenses += amount
                    except ValueError:
                        continue  # Skip rows with invalid amount

        remaining_balance = total_income - total_expenses

        tk.Label(summary_window, text=f"Total Income: {total_income}").pack()
        tk.Label(summary_window, text=f"Total Expenses: {total_expenses}").pack()
        tk.Label(summary_window, text=f"Remaining Balance: {remaining_balance}").pack()

    # Function to visualize data
    def visualize_data_window(self):
        vis_window = tk.Toplevel(self.root)
        vis_window.title("Data Visualization")

        income = 0
        expenses = 0

        if os.path.exists('financial_data.csv'):
            with open('financial_data.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    # Check if the row has the expected number of columns
                    if len(row) < 5:
                        continue  # Skip rows with insufficient data
                    try:
                        amount = float(row[2])
                        if row[4] == "Income":
                            income += amount
                        elif row[4] == "Expense":
                            expenses += amount
                    except ValueError:
                        continue  # Skip rows with invalid amount

        fig, ax = plt.subplots()
        ax.bar(["Income", "Expenses"], [income, expenses], color=['green', 'red'])
        ax.set_title("Income vs. Expenses")

        canvas = FigureCanvasTkAgg(fig, master=vis_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialManagerApp(root)
    root.mainloop()
