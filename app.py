import os

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Transaction
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-later'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tracker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------- Auth routes ----------

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password)
        new_user = User(email=email, name=name, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ---------- Dashboard ----------

@app.route('/dashboard')
@login_required
def dashboard():
    category_filter = request.args.get('category', 'all')
    query = Transaction.query.filter_by(user_id=current_user.id)

    if category_filter != 'all':
        query = query.filter_by(category=category_filter)

    transactions = query.order_by(Transaction.date.desc()).all()

    all_transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    total_income  = sum(t.amount for t in all_transactions if t.type == 'income')
    total_expense = sum(t.amount for t in all_transactions if t.type == 'expense')
    balance = total_income - total_expense

    categories = [
        'Food', 'Transport', 'Rent', 'Utilities',
        'Entertainment', 'Health', 'Education',
        'Salary', 'Freelance', 'Gift', 'Other'
    ]

    return render_template('dashboard.html',
        transactions=transactions,
        balance=balance,
        total_income=total_income,
        total_expense=total_expense,
        categories=categories,
        selected_category=category_filter
    )


# ---------- Transactions ----------

@app.route('/add', methods=['POST'])
@login_required
def add_transaction():
    t = Transaction(
        type=request.form['type'],
        amount=float(request.form['amount']),
        category=request.form['category'],
        note=request.form.get('note', ''),
        date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
        user_id=current_user.id
    )
    db.session.add(t)
    db.session.commit()
    flash('Transaction added!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:id>')
@login_required
def delete_transaction(id):
    t = Transaction.query.get_or_404(id)
    if t.user_id != current_user.id:
        flash('Unauthorized.', 'error')
        return redirect(url_for('dashboard'))
    db.session.delete(t)
    db.session.commit()
    flash('Transaction deleted.', 'success')
    return redirect(url_for('dashboard'))


# ---------- Run ----------

# runs on every startup
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)