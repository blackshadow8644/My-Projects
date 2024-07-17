import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QGroupBox, QFormLayout, QDateEdit, QDialog, QLineEdit, QComboBox, QPlainTextEdit, QMessageBox
from PyQt5.QtCore import Qt, QDate
from datetime import datetime
import pandas as pd
import csv
import matplotlib.pyplot as plt

date_format = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    DATE_FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.DATE_FORMAT)
        start_date = datetime.strptime(start_date, cls.DATE_FORMAT)
        end_date = datetime.strptime(end_date, cls.DATE_FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range")
        else:
            print(f"Transactions from {start_date.strftime(cls.DATE_FORMAT)} to {end_date.strftime(cls.DATE_FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(cls.DATE_FORMAT)}))

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net saving: ${(total_income - total_expense):.2f}")

        return filtered_df

class FinanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Finance Tracker')
        self.setGeometry(100, 100, 600, 400)

        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()

        label_title = QLabel('Finance Tracker')
        label_title.setAlignment(Qt.AlignCenter)
        vbox.addWidget(label_title)

        group_box = QGroupBox('Options')
        form_layout = QFormLayout()

        self.button_add = QPushButton('Add a new transaction')
        self.button_add.clicked.connect(self.add_transaction)
        form_layout.addRow(self.button_add)

        self.button_view = QPushButton('View transactions and summary')
        self.button_view.clicked.connect(self.view_transactions)
        form_layout.addRow(self.button_view)

        group_box.setLayout(form_layout)
        vbox.addWidget(group_box)

        self.setLayout(vbox)

    def add_transaction(self):
        dialog = AddTransactionDialog()
        if dialog.exec_() == QDialog.Accepted:
            date = dialog.date_edit.date().toString("dd-MM-yyyy")
            amount = dialog.amount_edit.text()
            category = dialog.category_combo.currentText()
            description = dialog.description_edit.toPlainText()
            CSV.add_entry(date, amount, category, description)
            QMessageBox.information(self, 'Success', 'Entry added successfully')

    def view_transactions(self):
        dialog = ViewTransactionsDialog()
        if dialog.exec_() == QDialog.Accepted:
            start_date = dialog.start_date_edit.date().toString("dd-MM-yyyy")
            end_date = dialog.end_date_edit.date().toString("dd-MM-yyyy")
            df = CSV.get_transactions(start_date, end_date)
            if df.empty:
                QMessageBox.information(self, 'No Transactions', 'No transactions found in the given date range')
                return
            reply = QMessageBox.question(self, 'Plot Graph', 'Do you want to see a graph?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.plot_transaction(df)

    def plot_transaction(self, df):
        df.set_index('date', inplace=True)

        income_df = (df[df["category"] == "Income"]
                     .resample("D")
                     .sum()
                     .reindex(df.index, fill_value=0)
                     )

        expense_df = (df[df["category"] == "Expense"]
                      .resample("D")
                      .sum()
                      .reindex(df.index, fill_value=0)
                      )

        plt.figure(figsize=(10, 5))
        plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
        plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Income and Expense Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()

class AddTransactionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Transaction')
        self.setGeometry(100, 100, 400, 300)

        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.date_edit = QDateEdit()
        self.date_edit.setDisplayFormat("dd-MM-yyyy")
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        layout.addRow("Date:", self.date_edit)

        self.amount_edit = QLineEdit()
        layout.addRow("Amount:", self.amount_edit)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["Income", "Expense"])
        layout.addRow("Category:", self.category_combo)

        self.description_edit = QPlainTextEdit()
        layout.addRow("Description:", self.description_edit)

        self.button_add = QPushButton('Add')
        self.button_add.clicked.connect(self.accept)
        layout.addRow(self.button_add)

        self.setLayout(layout)

class ViewTransactionsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('View Transactions')
        self.setGeometry(100, 100, 400, 200)

        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDisplayFormat("dd-MM-yyyy")
        self.start_date_edit.setDate(QDate.currentDate())
        self.start_date_edit.setCalendarPopup(True)
        layout.addRow("Start Date:", self.start_date_edit)

        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDisplayFormat("dd-MM-yyyy")
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setCalendarPopup(True)
        layout.addRow("End Date:", self.end_date_edit)

        self.button_view = QPushButton('View')
        self.button_view.clicked.connect(self.accept)
        layout.addRow(self.button_view)

        self.setLayout(layout)

if __name__ == '__main__':
    CSV.initialize_csv()
    app = QApplication(sys.argv)
    window = FinanceApp()
    window.show()
    sys.exit(app.exec_())
