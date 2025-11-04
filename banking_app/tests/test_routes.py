"""Integration tests for Flask application routes"""
import pytest
from banking_app.models import db, Account, Loan, Transaction
from banking_app.models import AccountType, LoanType, LoanStatus


class TestAccountRoutes:
    """Tests for account-related routes"""
    
    def test_index_page(self, client):
        """Test home page loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Banking Application' in response.data
    
    def test_list_accounts_empty(self, client):
        """Test listing accounts when none exist"""
        response = client.get('/accounts')
        assert response.status_code == 200
        assert b'No accounts found' in response.data
    
    def test_create_account(self, client, app):
        """Test creating an account via form"""
        response = client.post('/accounts/create', data={
            'customer_name': 'John Doe',
            'customer_email': 'john@example.com',
            'account_type': 'savings',
            'initial_balance': '1000.00'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'created successfully' in response.data
        
        # Verify account was created in database
        with app.app_context():
            account = Account.query.filter_by(customer_name='John Doe').first()
            assert account is not None
            assert account.balance == 1000.0
    
    def test_account_detail(self, client, app):
        """Test viewing account details"""
        with app.app_context():
            account = Account(
                account_number='1234567890',
                account_type=AccountType.CHECKING,
                customer_name='Jane Doe',
                customer_email='jane@example.com',
                balance=2500.0
            )
            db.session.add(account)
            db.session.commit()
            account_id = account.id
        
        response = client.get(f'/accounts/{account_id}')
        assert response.status_code == 200
        assert b'1234567890' in response.data
        assert b'Jane Doe' in response.data


class TestLoanRoutes:
    """Tests for loan-related routes"""
    
    def test_list_loans_empty(self, client):
        """Test listing loans when none exist"""
        response = client.get('/loans')
        assert response.status_code == 200
        assert b'No loans found' in response.data
    
    def test_apply_loan_page(self, client, app):
        """Test loan application page loads"""
        with app.app_context():
            account = Account(
                account_number='1234567890',
                account_type=AccountType.SAVINGS,
                customer_name='Test User',
                customer_email='test@example.com'
            )
            db.session.add(account)
            db.session.commit()
        
        response = client.get('/loans/apply')
        assert response.status_code == 200
        assert b'Apply for Loan' in response.data
    
    def test_apply_loan_submit(self, client, app):
        """Test submitting loan application"""
        with app.app_context():
            account = Account(
                account_number='1234567890',
                account_type=AccountType.SAVINGS,
                customer_name='Test User',
                customer_email='test@example.com',
                balance=5000.0
            )
            db.session.add(account)
            db.session.commit()
            account_id = account.id
        
        response = client.post('/loans/apply', data={
            'account_id': account_id,
            'loan_type': 'personal',
            'principal_amount': '10000.00',
            'interest_rate': '8.5',
            'term_months': '24',
            'purpose': 'Home improvement'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'submitted successfully' in response.data
        
        # Verify loan was created
        with app.app_context():
            loan = Loan.query.filter_by(account_id=account_id).first()
            assert loan is not None
            assert loan.principal_amount == 10000.0
            assert loan.loan_status == LoanStatus.PENDING
    
    def test_approve_loan(self, client, app):
        """Test approving a loan"""
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
                interest_rate=7.0,
                term_months=24,
                monthly_payment=226.0,
                outstanding_balance=5000.0,
                loan_status=LoanStatus.PENDING
            )
            db.session.add(loan)
            db.session.commit()
            loan_id = loan.id
        
        response = client.post(f'/loans/{loan_id}/approve', follow_redirects=True)
        assert response.status_code == 200
        assert b'approved successfully' in response.data
        
        # Verify loan status changed
        with app.app_context():
            loan = Loan.query.get(loan_id)
            assert loan.loan_status == LoanStatus.APPROVED
            assert loan.approval_date is not None
    
    def test_disburse_loan(self, client, app):
        """Test disbursing an approved loan"""
        with app.app_context():
            account = Account(
                account_number='1234567890',
                account_type=AccountType.SAVINGS,
                customer_name='Test User',
                customer_email='test@example.com',
                balance=0.0
            )
            db.session.add(account)
            db.session.commit()
            
            loan = Loan(
                loan_number='LN12345678',
                account_id=account.id,
                loan_type=LoanType.PERSONAL,
                principal_amount=5000.0,
                interest_rate=7.0,
                term_months=24,
                monthly_payment=226.0,
                outstanding_balance=5000.0,
                loan_status=LoanStatus.APPROVED
            )
            db.session.add(loan)
            db.session.commit()
            loan_id = loan.id
            account_id = account.id
        
        response = client.post(f'/loans/{loan_id}/disburse', follow_redirects=True)
        assert response.status_code == 200
        assert b'disbursed successfully' in response.data
        
        # Verify loan status and account balance
        with app.app_context():
            loan = Loan.query.get(loan_id)
            account = Account.query.get(account_id)
            assert loan.loan_status == LoanStatus.ACTIVE
            assert account.balance == 5000.0
    
    def test_make_loan_payment(self, client, app):
        """Test making a payment on an active loan"""
        with app.app_context():
            account = Account(
                account_number='1234567890',
                account_type=AccountType.SAVINGS,
                customer_name='Test User',
                customer_email='test@example.com',
                balance=5000.0
            )
            db.session.add(account)
            db.session.commit()
            
            loan = Loan(
                loan_number='LN12345678',
                account_id=account.id,
                loan_type=LoanType.PERSONAL,
                principal_amount=5000.0,
                interest_rate=7.0,
                term_months=24,
                monthly_payment=226.0,
                outstanding_balance=5000.0,
                loan_status=LoanStatus.ACTIVE
            )
            db.session.add(loan)
            db.session.commit()
            loan_id = loan.id
            account_id = account.id
        
        response = client.post(f'/loans/{loan_id}/pay', data={
            'payment_amount': '500.00'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'processed successfully' in response.data
        
        # Verify balances updated
        with app.app_context():
            loan = Loan.query.get(loan_id)
            account = Account.query.get(account_id)
            assert loan.outstanding_balance == 4500.0
            assert account.balance == 4500.0


class TestAPIRoutes:
    """Tests for API endpoints"""
    
    def test_api_list_accounts(self, client, app):
        """Test API endpoint for listing accounts"""
        with app.app_context():
            account = Account(
                account_number='1234567890',
                account_type=AccountType.SAVINGS,
                customer_name='Test User',
                customer_email='test@example.com',
                balance=1000.0
            )
            db.session.add(account)
            db.session.commit()
        
        response = client.get('/api/accounts')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['account_number'] == '1234567890'
    
    def test_api_list_loans(self, client, app):
        """Test API endpoint for listing loans"""
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
                interest_rate=7.0,
                term_months=24,
                monthly_payment=226.0,
                outstanding_balance=5000.0
            )
            db.session.add(loan)
            db.session.commit()
        
        response = client.get('/api/loans')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['loan_number'] == 'LN12345678'


class TestTransactionRoutes:
    """Tests for transaction-related routes"""
    
    def test_list_transactions(self, client, app):
        """Test listing transactions"""
        response = client.get('/transactions')
        assert response.status_code == 200
