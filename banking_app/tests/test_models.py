"""Unit tests for database models"""
import pytest
from datetime import datetime
from banking_app.models import db, Account, Loan, Transaction
from banking_app.models import AccountType, LoanType, LoanStatus, TransactionType


class TestAccountModel:
    """Tests for Account model"""
    
    def test_create_account(self, app):
        """Test creating an account"""
        with app.app_context():
            account = Account(
                account_number='1234567890',
                account_type=AccountType.SAVINGS,
                customer_name='John Doe',
                customer_email='john@example.com',
                balance=1000.0
            )
            db.session.add(account)
            db.session.commit()
            
            retrieved = Account.query.filter_by(account_number='1234567890').first()
            assert retrieved is not None
            assert retrieved.customer_name == 'John Doe'
            assert retrieved.balance == 1000.0
            assert retrieved.account_type == AccountType.SAVINGS
    
    def test_account_relationships(self, app):
        """Test account has loans and transactions"""
        with app.app_context():
            account = Account(
                account_number='1234567890',
                account_type=AccountType.CHECKING,
                customer_name='Jane Doe',
                customer_email='jane@example.com'
            )
            db.session.add(account)
            db.session.commit()
            
            loan = Loan(
                loan_number='LN12345678',
                account_id=account.id,
                loan_type=LoanType.PERSONAL,
                principal_amount=5000.0,
                interest_rate=8.5,
                term_months=24,
                monthly_payment=227.53,
                outstanding_balance=5000.0
            )
            db.session.add(loan)
            db.session.commit()
            
            assert account.loans.count() == 1
            assert account.loans.first().loan_number == 'LN12345678'


class TestLoanModel:
    """Tests for Loan model"""
    
    def test_create_loan(self, app):
        """Test creating a loan"""
        with app.app_context():
            account = Account(
                account_number='1234567890',
                account_type=AccountType.SAVINGS,
                customer_name='Test User',
                customer_email='test@example.com'
            )
            db.session.add(account)
            db.session.commit()
            
            loan = Loan(
                loan_number='LN12345678',
                account_id=account.id,
                loan_type=LoanType.HOME,
                principal_amount=200000.0,
                interest_rate=4.5,
                term_months=360,
                monthly_payment=1013.37,
                outstanding_balance=200000.0
            )
            db.session.add(loan)
            db.session.commit()
            
            retrieved = Loan.query.filter_by(loan_number='LN12345678').first()
            assert retrieved is not None
            assert retrieved.principal_amount == 200000.0
            assert retrieved.loan_status == LoanStatus.PENDING
    
    def test_loan_monthly_payment_calculation(self, app):
        """Test monthly payment calculation"""
        with app.app_context():
            account = Account(
                account_number='1234567890',
                account_type=AccountType.SAVINGS,
                customer_name='Test User',
                customer_email='test@example.com'
            )
            db.session.add(account)
            db.session.commit()
            
            loan = Loan(
                loan_number='LN12345678',
                account_id=account.id,
                loan_type=LoanType.AUTO,
                principal_amount=25000.0,
                interest_rate=6.0,
                term_months=60,
                monthly_payment=0,  # Will calculate
                outstanding_balance=25000.0
            )
            
            # Calculate monthly payment
            monthly_payment = loan.calculate_monthly_payment()
            
            # Should be around $483.32
            assert 483.0 < monthly_payment < 484.0
    
    def test_loan_status_workflow(self, app):
        """Test loan status transitions"""
        with app.app_context():
            account = Account(
                account_number='1234567890',
                account_type=AccountType.SAVINGS,
                customer_name='Test User',
                customer_email='test@example.com'
            )
            db.session.add(account)
            db.session.commit()
            
            loan = Loan(
                loan_number='LN12345678',
                account_id=account.id,
                loan_type=LoanType.PERSONAL,
                principal_amount=10000.0,
                interest_rate=7.0,
                term_months=36,
                monthly_payment=308.77,
                outstanding_balance=10000.0
            )
            db.session.add(loan)
            db.session.commit()
            
            # Start as pending
            assert loan.loan_status == LoanStatus.PENDING
            
            # Approve
            loan.loan_status = LoanStatus.APPROVED
            loan.approval_date = datetime.utcnow()
            db.session.commit()
            
            assert loan.loan_status == LoanStatus.APPROVED
            assert loan.approval_date is not None


class TestTransactionModel:
    """Tests for Transaction model"""
    
    def test_create_transaction(self, app):
        """Test creating a transaction"""
        with app.app_context():
            account = Account(
                account_number='1234567890',
                account_type=AccountType.CHECKING,
                customer_name='Test User',
                customer_email='test@example.com',
                balance=5000.0
            )
            db.session.add(account)
            db.session.commit()
            
            transaction = Transaction(
                transaction_number='TXN1234567890',
                account_id=account.id,
                transaction_type=TransactionType.DEPOSIT,
                amount=500.0,
                balance_after=5500.0,
                description='Test deposit'
            )
            db.session.add(transaction)
            db.session.commit()
            
            retrieved = Transaction.query.filter_by(transaction_number='TXN1234567890').first()
            assert retrieved is not None
            assert retrieved.amount == 500.0
            assert retrieved.transaction_type == TransactionType.DEPOSIT
    
    def test_loan_transaction_relationship(self, app):
        """Test transaction linked to loan"""
        with app.app_context():
            account = Account(
                account_number='1234567890',
                account_type=AccountType.SAVINGS,
                customer_name='Test User',
                customer_email='test@example.com'
            )
            db.session.add(account)
            db.session.commit()
            
            loan = Loan(
                loan_number='LN12345678',
                account_id=account.id,
                loan_type=LoanType.PERSONAL,
                principal_amount=5000.0,
                interest_rate=8.0,
                term_months=24,
                monthly_payment=226.07,
                outstanding_balance=5000.0
            )
            db.session.add(loan)
            db.session.commit()
            
            transaction = Transaction(
                transaction_number='TXN1234567890',
                account_id=account.id,
                loan_id=loan.id,
                transaction_type=TransactionType.LOAN_DISBURSEMENT,
                amount=5000.0,
                description='Loan disbursement'
            )
            db.session.add(transaction)
            db.session.commit()
            
            assert transaction.loan_id == loan.id
            assert loan.transactions.count() == 1
