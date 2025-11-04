# Banking Application - Loans Management System

## Overview
A comprehensive banking application with full loan management capabilities, built with Flask and SQLAlchemy.

## Features

### Account Management
- Create and manage multiple account types (Savings, Checking, Business)
- View account details and balances
- Track account transactions

### Loan Services
- Apply for various loan types:
  - Personal Loans
  - Home Loans
  - Auto Loans
  - Business Loans
  - Education Loans
- Complete loan workflow:
  - Application submission
  - Approval/rejection
  - Loan disbursement
  - Payment processing
- Automatic monthly payment calculations
- Loan status tracking

### Transaction Management
- Complete audit trail of all financial transactions
- Transaction types:
  - Deposits and withdrawals
  - Loan disbursements
  - Loan payments
  - Interest charges
  - Fees and transfers

## Technical Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLAlchemy 2.0.23 with SQLite/PostgreSQL support
- **Frontend**: Bootstrap 5.3.0
- **Testing**: Pytest 7.4.3

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/kavyashri-as/foundation-demo.git
cd foundation-demo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables (optional):
```bash
export FLASK_ENV=development
export SECRET_KEY=your-secret-key
export DATABASE_URL=sqlite:///banking_app.db
```

## Running the Application

### Development Mode
```bash
cd banking_app
python app.py
```

The application will be available at `http://localhost:5000`

### Production Mode
```bash
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=postgresql://user:pass@host:5432/banking_app

python app.py
```

## Running Tests

### Run all tests:
```bash
pytest
```

### Run with coverage:
```bash
pytest --cov=banking_app --cov-report=html
```

### Run specific test file:
```bash
pytest banking_app/tests/test_models.py
pytest banking_app/tests/test_routes.py
```

## Project Structure

```
banking_app/
├── __init__.py           # Package initialization
├── app.py                # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── accounts.html
│   ├── loans.html
│   └── ...
└── tests/               # Test suite
    ├── __init__.py
    ├── conftest.py
    ├── test_models.py
    └── test_routes.py
```

## API Endpoints

### Accounts
- `GET /accounts` - List all accounts
- `GET /accounts/create` - Show create account form
- `POST /accounts/create` - Create new account
- `GET /accounts/<id>` - View account details

### Loans
- `GET /loans` - List all loans (with optional status filter)
- `GET /loans/apply` - Show loan application form
- `POST /loans/apply` - Submit loan application
- `GET /loans/<id>` - View loan details
- `POST /loans/<id>/approve` - Approve loan
- `POST /loans/<id>/reject` - Reject loan
- `POST /loans/<id>/disburse` - Disburse loan
- `POST /loans/<id>/pay` - Make loan payment

### Transactions
- `GET /transactions` - List all transactions (paginated)

### API
- `GET /api/accounts` - Get accounts as JSON
- `GET /api/loans` - Get loans as JSON

## Configuration

The application supports three configurations:

### Development
- Debug mode enabled
- SQLite database
- Verbose logging

### Testing
- Test database
- CSRF disabled
- Debug mode enabled

### Production
- Debug mode disabled
- Secure cookies
- Environment variable validation
- PostgreSQL recommended

## Database Schema

### Tables
- **accounts**: Customer bank accounts
- **loans**: Loan records
- **transactions**: Financial transaction history

### Relationships
- One account can have many loans
- One account can have many transactions
- One loan can have many transactions

## Security Features

- Secure session management
- CSRF protection (production)
- Input validation
- SQL injection protection (SQLAlchemy ORM)
- XSS protection (Jinja2 auto-escaping)

## Loan Calculation

Monthly payments are calculated using the standard amortization formula:

```
Monthly Payment = P × [r(1+r)^n] / [(1+r)^n - 1]

Where:
P = Principal loan amount
r = Monthly interest rate (annual rate / 12)
n = Number of payment months
```

## Configuration Limits

- **Loan Amount**: $1,000 - $1,000,000
- **Interest Rate**: 3.0% - 25.0%
- **Loan Term**: 6 - 360 months

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure everything works
5. Submit a pull request

## Testing

The application includes comprehensive test coverage:

- **Unit Tests**: Test individual models and functions
- **Integration Tests**: Test complete workflows and API endpoints
- **Coverage Target**: 90%+

## Documentation

- [Deployment Plan](.github/deployment/deployment_plan.md)
- [User Guide](.github/documentation/user_guide.md)

## License

Copyright © 2025 Banking Application. All rights reserved.

## Support

For issues, questions, or contributions, please contact:
- Development Lead: @kavyashri-as
- Email: support@example.com
