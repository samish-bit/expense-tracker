# Expense Tracker

A personal finance web app to track income and expenses, built with Python and Flask.

![Dashboard Screenshot](screenshot.png)

## Features

- User registration and login with password hashing
- Add income and expense transactions with category, date, and notes
- Dashboard with live balance, total income, and total expenses
- Donut chart showing income vs expense breakdown
- Filter transactions by category
- Delete transactions
- Fully responsive layout

## Tech Stack

- **Frontend:** HTML, CSS, Vanilla JavaScript, Chart.js
- **Backend:** Python, Flask, Flask-Login, Flask-SQLAlchemy
- **Database:** SQLite
- **Deployment:** Render

## Running locally

1. Clone the repo
```bash
   git clone https://github.com/YOUR_USERNAME/expense-tracker.git
   cd expense-tracker
```

2. Create and activate a virtual environment
```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
```

3. Install dependencies
```bash
   pip install -r requirements.txt
```

4. Run the app
```bash
   python app.py
```

5. Open `http://127.0.0.1:5000` in your browser

## Live Demo

[View live app](https://expense-tracker-54jl.onrender.com)
