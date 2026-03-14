# Wragby Wallet API

A Django REST Framework application for managing digital wallets and transactions with background job processing using Celery.

## Features

- **User Management**: Create and manage user accounts
- **Wallet Management**: Each user has a digital wallet with balance tracking
- **Wallet Funding**: Add funds to user wallets with atomic transactions
- **Transactions**: Transfer funds between wallets with transaction history
- **Background Processing**: Asynchronous transaction processing using Celery
- **API Documentation**: Interactive API documentation with Swagger UI and ReDoc

## Tech Stack

- Django 6.0.1
- Django REST Framework
- drf-spectacular (API documentation)
- Celery (Background tasks)
- Redis (Celery broker)
- SQLite (Database)

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd wragby-app
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

## Running the Application

The application requires three separate processes to run simultaneously:

### Prerequisites
- **Redis**: Install Redis if you haven't already
  - **macOS**: `brew install redis`
  - **Ubuntu/Debian**: `sudo apt-get install redis-server`
  - **Windows**: Download from https://redis.io/download

### Step-by-Step Guide

**Terminal 1: Start Redis Server**
```bash
redis-server
```
Keep this terminal running. You should see output indicating Redis is running on port 6379.

**Terminal 2: Start Django Development Server**
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run Django server
python manage.py runserver
```
The API will be available at http://localhost:8000

**Terminal 3: Start Celery Worker**
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start Celery worker
celery -A core worker --loglevel=info
```
Keep this running to process background tasks.

### Quick Start (All in one command - macOS/Linux)
```bash
# Terminal 1
redis-server

# Terminal 2
source venv/bin/activate && python manage.py runserver

# Terminal 3
source venv/bin/activate && celery -A core worker --loglevel=info
```

## API Endpoints

### Users
- `GET /api/user/users/` - List all users
- `POST /api/user/users/` - Create a new user
- `GET /api/user/users/{id}/` - Get user details
- `PUT /api/user/users/{id}/` - Update user

### Wallets
- `GET /api/wallet/wallets/` - List all wallets
- `POST /api/wallet/wallets/` - Create a new wallet
- `GET /api/wallet/wallets/{id}/` - Get wallet details
- `POST /api/wallet/wallets/fund/` - Fund a wallet

**Fund Wallet Request Body:**
```json
{
  "wallet_id": 1,
  "amount": 100.00
}
```

**Fund Wallet Response:**
```json
{
  "message": "Wallet funded successfully",
  "success": true,
  "wallet_id": 1,
  "new_balance": 150.00
}
```

### Transactions
- `POST /api/transaction/transactions/` - Initiate a new transaction

**Transaction Request Body:**
```json
{
  "sender_wallet_id": 1,
  "recipient_wallet_id": 2,
  "amount": 100.00
}
```

**Transaction Response:**
```json
{
  "message": "Transaction initiated successfully",
  "success": true,
  "transaction_id": 1
}
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## Project Structure

```
wragby-app/
├── core/
│   ├── __init__.py
│   ├── celery.py          # Celery configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py
├── user/
│   ├── models.py          # User model
│   ├── serializers.py     # User serializers
│   ├── views.py           # User viewsets
│   └── urls.py            # User URLs
├── wallet/
│   ├── models.py          # Wallet model
│   ├── serializers.py     # Wallet serializers
│   ├── views.py           # Wallet viewsets
│   └── urls.py            # Wallet URLs
├── transaction/
│   ├── models.py          # Transaction model
│   ├── serializers.py     # Transaction serializers
│   ├── views.py           # Transaction viewsets
│   ├── urls.py            # Transaction URLs
│   ├── tasks.py           # Celery tasks
│   └── utils.py           # Transaction utilities
└── manage.py
```

## How It Works

### Wallet Funding Flow

1. Client sends a POST request to `/api/wallet/wallets/fund/` with wallet_id and amount
2. The system validates the amount is positive
3. Using an atomic database transaction:
   - The amount is added to the wallet balance
   - The wallet is saved
4. Returns success response with new balance

### Transaction Flow

1. Client sends a POST request to `/api/transaction/transactions/` with sender wallet, recipient wallet, and amount
2. The system validates:
   - Sufficient balance in sender's wallet
   - Sender and recipient are different
3. A transaction record is created with `pending` status
4. The transaction is queued as a background Celery task
5. The Celery worker processes the transaction asynchronously:
   - Deducts amount from sender's wallet
   - Adds amount to recipient's wallet
   - Updates transaction status to `completed` or `failed`

### Background Processing

Celery handles transaction processing asynchronously, ensuring:
- Fast API response times
- Reliable transaction processing
- Ability to handle high transaction volumes
- Automatic retry on failures

### Atomic Transactions

Both wallet funding and transfers use Django's atomic transactions to ensure:
- Data consistency
- All-or-nothing operations
- Protection against race conditions

## Configuration

Key settings in `core/settings.py`:

```python
# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# DRF Spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'Wragby Wallet API',
    'VERSION': '1.0.0',
}
```

## Development

### Running Tests
```bash
python manage.py test
```

### Admin Interface
Access the Django admin at: http://localhost:8000/admin/

## Testing the API

You can test the API using the Swagger UI at http://localhost:8000/api/docs/ or using curl:

### Create a User
```bash
curl -X POST http://localhost:8000/api/user/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "email": "john@example.com", "password": "securepass123"}'
```

### Create a Wallet
```bash
curl -X POST http://localhost:8000/api/wallet/wallets/ \
  -H "Content-Type: application/json" \
  -d '{"user": 1}'
```

### Fund a Wallet
```bash
curl -X POST http://localhost:8000/api/wallet/wallets/fund/ \
  -H "Content-Type: application/json" \
  -d '{"wallet_id": 1, "amount": 1000.00}'
```

### Transfer Funds
```bash
curl -X POST http://localhost:8000/api/transaction/transactions/ \
  -H "Content-Type: application/json" \
  -d '{"sender_wallet_id": 1, "recipient_wallet_id": 2, "amount": 100.00}'
```

## Notes

- The application uses SQLite for development. For production, use PostgreSQL or MySQL
- Redis is required for Celery to function
- Transaction processing is atomic to ensure data consistency
- All monetary amounts should be handled with decimal precision in production
- Ensure all three processes (Redis, Django, Celery) are running for full functionality

## License

MIT License
