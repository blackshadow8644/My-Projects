class ViewTransactionsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Transactions")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        date_layout = QHBoxLayout()
        self.start_date_edit = QDateEdit(calendarPopup=True)
        self.start_date_edit.setDate(QDate.currentDate().addMonths(-1))
        date_layout.addWidget(QLabel("Start Date:"))
        date_layout.addWidget(self.start_date_edit)

        self.end_date_edit = QDateEdit(calendarPopup=True)
        self.end_date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(QLabel("End Date:"))
        date_layout.addWidget(self.end_date_edit)

        self.view_button = QPushButton("View Transactions")
        self.view_button.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; border: none;"
            "border-radius: 4px; padding: 10px; font-size: 16px; }"
            "QPushButton:hover { background-color: #45a049; }"
        )
        self.view_button.clicked.connect(self.view_transactions)
        date_layout.addWidget(self.view_button)

        self.layout.addLayout(date_layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

    def view_transactions(self):
        start_date = self.start_date_edit.date().toString("dd-MM-yyyy")
        end_date = self.end_date_edit.date().toString("dd-MM-yyyy")

        df = CSV.get_transactions(start_date, end_date)

        if df.empty:
            QMessageBox.warning(self, "No Transactions", "No transactions found in the given date range.")
            return

        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)

        for i, row in df.iterrows():
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

        self.graph_window = GraphWindow(df)
        self.graph_window.show()

