"""
Flask application for Banking Application with Loans feature.
Provides routes for loan applications, approvals, disbursements, and tracking.
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime, timedelta
from decimal import Decimal
import os
import random
import string

from banking_app.models import db, Account, Loan, Transaction
from banking_app.models import AccountType, LoanType, LoanStatus, TransactionType
from banking_app.config import config


def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_name = os.environ.get('FLASK_ENV', config_name)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Register routes within app context
    register_routes(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app


def register_routes(app):
    """Register all routes with the app"""
    
    # ==================== Routes ====================
    
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    
    @app.route('/accounts')
    def list_accounts():
        """List all accounts"""
        accounts = Account.query.all()
        return render_template('accounts.html', accounts=accounts)
    
    
    @app.route('/accounts/create', methods=['GET', 'POST'])
    def create_account():
        """Create a new account"""
        if request.method == 'POST':
            try:
                account = Account(
                    account_number=generate_account_number(),
                    account_type=AccountType[request.form['account_type'].upper()],
                    customer_name=request.form['customer_name'],
                    customer_email=request.form['customer_email'],
                    balance=float(request.form.get('initial_balance', 0.0))
                )
                db.session.add(account)
                db.session.commit()
                flash(f'Account {account.account_number} created successfully!', 'success')
                return redirect(url_for('list_accounts'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error creating account: {str(e)}', 'error')
        
        account_types = [t.value for t in AccountType]
        return render_template('create_account.html', account_types=account_types)
    
    
    @app.route('/accounts/<int:account_id>')
    def account_detail(account_id):
        """View account details"""
        account = Account.query.get_or_404(account_id)
        loans = account.loans.all()
        transactions = account.transactions.order_by(Transaction.transaction_date.desc()).limit(10).all()
        return render_template('account_detail.html', account=account, loans=loans, transactions=transactions)
    
    
    @app.route('/loans')
    def list_loans():
        """List all loans"""
        status_filter = request.args.get('status', 'all')
        query = Loan.query
        
        if status_filter != 'all':
            try:
                query = query.filter_by(loan_status=LoanStatus[status_filter.upper()])
            except KeyError:
                pass
        
        loans = query.order_by(Loan.application_date.desc()).all()
        loan_statuses = [s.value for s in LoanStatus]
        return render_template('loans.html', loans=loans, loan_statuses=loan_statuses, current_status=status_filter)
    
    
    @app.route('/loans/apply', methods=['GET', 'POST'])
    def apply_loan():
        """Apply for a new loan"""
        if request.method == 'POST':
            try:
                account_id = int(request.form['account_id'])
                account = Account.query.get_or_404(account_id)
                
                principal = float(request.form['principal_amount'])
                interest_rate = float(request.form['interest_rate'])
                term_months = int(request.form['term_months'])
                
                # Validate loan parameters
                if principal < app.config['MIN_LOAN_AMOUNT'] or principal > app.config['MAX_LOAN_AMOUNT']:
                    flash(f'Loan amount must be between ${app.config["MIN_LOAN_AMOUNT"]} and ${app.config["MAX_LOAN_AMOUNT"]}', 'error')
                    return redirect(url_for('apply_loan'))
                
                if interest_rate < app.config['MIN_INTEREST_RATE'] or interest_rate > app.config['MAX_INTEREST_RATE']:
                    flash(f'Interest rate must be between {app.config["MIN_INTEREST_RATE"]}% and {app.config["MAX_INTEREST_RATE"]}%', 'error')
                    return redirect(url_for('apply_loan'))
                
                if term_months < app.config['MIN_TERM_MONTHS'] or term_months > app.config['MAX_TERM_MONTHS']:
                    flash(f'Loan term must be between {app.config["MIN_TERM_MONTHS"]} and {app.config["MAX_TERM_MONTHS"]} months', 'error')
                    return redirect(url_for('apply_loan'))
                
                loan = Loan(
                    loan_number=generate_loan_number(),
                    account_id=account_id,
                    loan_type=LoanType[request.form['loan_type'].upper()],
                    principal_amount=principal,
                    interest_rate=interest_rate,
                    term_months=term_months,
                    outstanding_balance=principal,
                    purpose=request.form.get('purpose', ''),
                    loan_status=LoanStatus.PENDING
                )
                
                # Calculate monthly payment
                loan.monthly_payment = loan.calculate_monthly_payment()
                
                db.session.add(loan)
                db.session.commit()
                
                flash(f'Loan application {loan.loan_number} submitted successfully!', 'success')
                return redirect(url_for('loan_detail', loan_id=loan.id))
            except Exception as e:
                db.session.rollback()
                flash(f'Error submitting loan application: {str(e)}', 'error')
        
        accounts = Account.query.all()
        loan_types = [t.value for t in LoanType]
        return render_template('apply_loan.html', accounts=accounts, loan_types=loan_types)
    
    
    @app.route('/loans/<int:loan_id>')
    def loan_detail(loan_id):
        """View loan details"""
        loan = Loan.query.get_or_404(loan_id)
        transactions = loan.transactions.order_by(Transaction.transaction_date.desc()).all()
        return render_template('loan_detail.html', loan=loan, transactions=transactions)
    
    
    @app.route('/loans/<int:loan_id>/approve', methods=['POST'])
    def approve_loan(loan_id):
        """Approve a loan application"""
        try:
            loan = Loan.query.get_or_404(loan_id)
            
            if loan.loan_status != LoanStatus.PENDING:
                flash(f'Loan cannot be approved. Current status: {loan.loan_status.value}', 'error')
                return redirect(url_for('loan_detail', loan_id=loan_id))
            
            loan.loan_status = LoanStatus.APPROVED
            loan.approval_date = datetime.utcnow()
            
            db.session.commit()
            flash(f'Loan {loan.loan_number} approved successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error approving loan: {str(e)}', 'error')
        
        return redirect(url_for('loan_detail', loan_id=loan_id))
    
    
    @app.route('/loans/<int:loan_id>/reject', methods=['POST'])
    def reject_loan(loan_id):
        """Reject a loan application"""
        try:
            loan = Loan.query.get_or_404(loan_id)
            
            if loan.loan_status != LoanStatus.PENDING:
                flash(f'Loan cannot be rejected. Current status: {loan.loan_status.value}', 'error')
                return redirect(url_for('loan_detail', loan_id=loan_id))
            
            loan.loan_status = LoanStatus.REJECTED
            loan.notes = request.form.get('rejection_reason', 'Application rejected')
            
            db.session.commit()
            flash(f'Loan {loan.loan_number} rejected.', 'info')
        except Exception as e:
            db.session.rollback()
            flash(f'Error rejecting loan: {str(e)}', 'error')
        
        return redirect(url_for('loan_detail', loan_id=loan_id))
    
    
    @app.route('/loans/<int:loan_id>/disburse', methods=['POST'])
    def disburse_loan(loan_id):
        """Disburse an approved loan"""
        try:
            loan = Loan.query.get_or_404(loan_id)
            account = loan.account
            
            if loan.loan_status != LoanStatus.APPROVED:
                flash(f'Loan cannot be disbursed. Current status: {loan.loan_status.value}', 'error')
                return redirect(url_for('loan_detail', loan_id=loan_id))
            
            # Update loan status
            loan.loan_status = LoanStatus.ACTIVE
            loan.disbursement_date = datetime.utcnow()
            loan.maturity_date = datetime.utcnow() + timedelta(days=loan.term_months * 30)
            
            # Update account balance
            account.balance += loan.principal_amount
            
            # Create disbursement transaction
            transaction = Transaction(
                transaction_number=generate_transaction_number(),
                account_id=account.id,
                loan_id=loan.id,
                transaction_type=TransactionType.LOAN_DISBURSEMENT,
                amount=loan.principal_amount,
                balance_after=account.balance,
                description=f'Loan disbursement for {loan.loan_number}'
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            flash(f'Loan {loan.loan_number} disbursed successfully! Amount: ${loan.principal_amount:.2f}', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error disbursing loan: {str(e)}', 'error')
        
        return redirect(url_for('loan_detail', loan_id=loan_id))
    
    
    @app.route('/loans/<int:loan_id>/pay', methods=['POST'])
    def make_loan_payment(loan_id):
        """Make a payment towards a loan"""
        try:
            loan = Loan.query.get_or_404(loan_id)
            account = loan.account
            
            if loan.loan_status != LoanStatus.ACTIVE:
                flash(f'Cannot make payment. Loan status: {loan.loan_status.value}', 'error')
                return redirect(url_for('loan_detail', loan_id=loan_id))
            
            payment_amount = float(request.form['payment_amount'])
            
            if payment_amount <= 0:
                flash('Payment amount must be greater than zero', 'error')
                return redirect(url_for('loan_detail', loan_id=loan_id))
            
            if account.balance < payment_amount:
                flash('Insufficient account balance', 'error')
                return redirect(url_for('loan_detail', loan_id=loan_id))
            
            # Update account balance
            account.balance -= payment_amount
            
            # Update loan outstanding balance
            loan.outstanding_balance -= payment_amount
            
            # Check if loan is fully paid
            if loan.outstanding_balance <= 0:
                loan.outstanding_balance = 0
                loan.loan_status = LoanStatus.CLOSED
                loan.closed_date = datetime.utcnow()
            
            # Create payment transaction
            transaction = Transaction(
                transaction_number=generate_transaction_number(),
                account_id=account.id,
                loan_id=loan.id,
                transaction_type=TransactionType.LOAN_PAYMENT,
                amount=payment_amount,
                balance_after=account.balance,
                description=f'Loan payment for {loan.loan_number}'
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            if loan.loan_status == LoanStatus.CLOSED:
                flash(f'Loan {loan.loan_number} paid in full and closed!', 'success')
            else:
                flash(f'Payment of ${payment_amount:.2f} processed successfully. Remaining balance: ${loan.outstanding_balance:.2f}', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error processing payment: {str(e)}', 'error')
        
        return redirect(url_for('loan_detail', loan_id=loan_id))
    
    
    @app.route('/transactions')
    def list_transactions():
        """List all transactions"""
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        transactions = Transaction.query.order_by(Transaction.transaction_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('transactions.html', transactions=transactions)
    
    
    # ==================== API Routes ====================
    
    @app.route('/api/accounts', methods=['GET'])
    def api_list_accounts():
        """API endpoint to list accounts"""
        accounts = Account.query.all()
        return jsonify([{
            'id': a.id,
            'account_number': a.account_number,
            'account_type': a.account_type.value,
            'customer_name': a.customer_name,
            'balance': a.balance
        } for a in accounts])
    
    
    @app.route('/api/loans', methods=['GET'])
    def api_list_loans():
        """API endpoint to list loans"""
        loans = Loan.query.all()
        return jsonify([{
            'id': l.id,
            'loan_number': l.loan_number,
            'loan_type': l.loan_type.value,
            'loan_status': l.loan_status.value,
            'principal_amount': l.principal_amount,
            'outstanding_balance': l.outstanding_balance,
            'monthly_payment': l.monthly_payment
        } for l in loans])
    
    
    @app.route('/api/loans/<int:loan_id>/calculate', methods=['POST'])
    def api_calculate_loan_payment():
        """API endpoint to calculate loan payment"""
        data = request.get_json()
        
        try:
            principal = float(data['principal_amount'])
            interest_rate = float(data['interest_rate'])
            term_months = int(data['term_months'])
            
            # Calculate using same formula as model
            monthly_rate = interest_rate / 100 / 12
            if monthly_rate == 0:
                monthly_payment = principal / term_months
            else:
                numerator = monthly_rate * ((1 + monthly_rate) ** term_months)
                denominator = ((1 + monthly_rate) ** term_months) - 1
                monthly_payment = principal * (numerator / denominator)
            
            total_payment = monthly_payment * term_months
            total_interest = total_payment - principal
            
            return jsonify({
                'monthly_payment': round(monthly_payment, 2),
                'total_payment': round(total_payment, 2),
                'total_interest': round(total_interest, 2)
            })
        except Exception as e:
            # Log the error for debugging but don't expose details to user
            app.logger.error(f'Loan calculation error: {str(e)}')
            return jsonify({'error': 'Invalid loan parameters'}), 400
    
    
    # ==================== Error Handlers ====================
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return render_template('404.html'), 404
    
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        db.session.rollback()
        return render_template('500.html'), 500


app = create_app()


def generate_account_number():
    """Generate a unique account number"""
    while True:
        number = ''.join(random.choices(string.digits, k=10))
        if not Account.query.filter_by(account_number=number).first():
            return number


def generate_loan_number():
    """Generate a unique loan number"""
    while True:
        number = 'LN' + ''.join(random.choices(string.digits, k=8))
        if not Loan.query.filter_by(loan_number=number).first():
            return number


def generate_transaction_number():
    """Generate a unique transaction number"""
    while True:
        number = 'TXN' + ''.join(random.choices(string.digits, k=10))
        if not Transaction.query.filter_by(transaction_number=number).first():
            return number


if __name__ == '__main__':
    # Debug mode is ONLY for local development
    # In production, use a WSGI server (gunicorn, uwsgi) with debug=False
    app.run(debug=True)
