"""
Database models for the Banking Application Loans feature.
Includes models for Accounts, Loans, and Transactions.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

db = SQLAlchemy()


class AccountType(enum.Enum):
    """Account type enumeration"""
    SAVINGS = "savings"
    CHECKING = "checking"
    BUSINESS = "business"


class LoanType(enum.Enum):
    """Loan type enumeration"""
    PERSONAL = "personal"
    HOME = "home"
    AUTO = "auto"
    BUSINESS = "business"
    EDUCATION = "education"


class LoanStatus(enum.Enum):
    """Loan status enumeration"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ACTIVE = "active"
    CLOSED = "closed"
    DEFAULTED = "defaulted"


class TransactionType(enum.Enum):
    """Transaction type enumeration"""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    LOAN_DISBURSEMENT = "loan_disbursement"
    LOAN_PAYMENT = "loan_payment"
    INTEREST_CHARGE = "interest_charge"
    FEE = "fee"
    TRANSFER = "transfer"


class Account(db.Model):
    """Account model representing customer bank accounts"""
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    account_number = Column(String(20), unique=True, nullable=False, index=True)
    account_type = Column(Enum(AccountType), nullable=False)
    customer_name = Column(String(100), nullable=False)
    customer_email = Column(String(100), nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    loans = relationship('Loan', back_populates='account', lazy='dynamic')
    transactions = relationship('Transaction', back_populates='account', lazy='dynamic')

    def __repr__(self):
        return f'<Account {self.account_number} - {self.customer_name}>'


class Loan(db.Model):
    """Loan model representing customer loans"""
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True)
    loan_number = Column(String(20), unique=True, nullable=False, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    loan_type = Column(Enum(LoanType), nullable=False)
    loan_status = Column(Enum(LoanStatus), default=LoanStatus.PENDING, nullable=False)
    
    # Financial details
    principal_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)  # Annual interest rate as percentage
    term_months = Column(Integer, nullable=False)  # Loan term in months
    monthly_payment = Column(Float, nullable=False)
    outstanding_balance = Column(Float, nullable=False)
    
    # Dates
    application_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    approval_date = Column(DateTime)
    disbursement_date = Column(DateTime)
    maturity_date = Column(DateTime)
    closed_date = Column(DateTime)
    
    # Additional info
    purpose = Column(String(500))
    notes = Column(String(1000))
    
    # Relationships
    account = relationship('Account', back_populates='loans')
    transactions = relationship('Transaction', back_populates='loan', lazy='dynamic')

    def __repr__(self):
        return f'<Loan {self.loan_number} - {self.loan_type.value} - {self.loan_status.value}>'

    def calculate_monthly_payment(self):
        """Calculate monthly payment using amortization formula"""
        if self.term_months == 0:
            return 0.0
        
        monthly_rate = self.interest_rate / 100 / 12
        if monthly_rate == 0:
            return self.principal_amount / self.term_months
        
        # Amortization formula: P * [r(1+r)^n] / [(1+r)^n - 1]
        numerator = monthly_rate * ((1 + monthly_rate) ** self.term_months)
        denominator = ((1 + monthly_rate) ** self.term_months) - 1
        return self.principal_amount * (numerator / denominator)


class Transaction(db.Model):
    """Transaction model for tracking all financial transactions"""
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    transaction_number = Column(String(20), unique=True, nullable=False, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    loan_id = Column(Integer, ForeignKey('loans.id'))
    
    transaction_type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    balance_after = Column(Float)
    description = Column(String(500))
    transaction_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    account = relationship('Account', back_populates='transactions')
    loan = relationship('Loan', back_populates='transactions')

    def __repr__(self):
        return f'<Transaction {self.transaction_number} - {self.transaction_type.value} - ${self.amount}>'
