# 🔐 Krili Transaction Handler

A secure, production-ready Go backend service for handling payments and payouts in the Krili rental platform.

## 🌟 Features

### 💳 Payment Processing
- **Multiple Payment Methods**: Credit/Debit cards, PayPal, Apple Pay
- **Real-time Validation**: Card number, expiry date, CVV validation
- **Secure Processing**: PCI-compliant data handling
- **Fee Calculation**: Automatic processing fee calculation
- **Transaction Tracking**: Complete audit trail

### 💰 Payout Management
- **Bank Transfers**: Direct deposit to user bank accounts
- **PayPal Payouts**: Instant PayPal transfers
- **Balance Management**: Real-time balance tracking
- **Fee Transparency**: Clear fee breakdown
- **Payout History**: Complete transaction history

### 🔒 Security Features
- **Data Encryption**: AES-256 encryption for sensitive data
- **JWT Authentication**: Secure token-based authentication
- **Rate Limiting**: Protection against abuse
- **Input Validation**: Comprehensive input sanitization
- **Audit Logging**: Complete transaction audit trail
- **PCI Compliance**: Secure payment data handling

### 🏗️ Architecture
- **RESTful API**: Clean, well-documented endpoints
- **Database Transactions**: ACID compliance
- **Error Handling**: Comprehensive error management
- **Monitoring**: Built-in health checks and logging
- **Scalability**: Designed for high-volume transactions

## 📋 Prerequisites

- **Go 1.21+**: [Download Go](https://golang.org/doc/install)
- **MySQL 8.0+**: [Download MySQL](https://dev.mysql.com/downloads/mysql/)
- **Git**: For version control
- **OpenSSL**: For key generation (usually pre-installed)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Navigate to the backend directory
cd Backend

# Make setup script executable (Linux/Mac)
chmod +x setup.sh

# Run the setup script
./setup.sh
```

### 2. Manual Setup (Windows)

```powershell
# Install Go dependencies
go mod tidy
go mod download

# Copy environment file
copy .env.example .env

# Edit .env file with your configuration
notepad .env

# Build the application
go build -o transaction-handler.exe transaction_handler.go

# Run the application
./transaction-handler.exe
```

### 3. Database Setup

```sql
-- Create database
CREATE DATABASE krili_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Import schema
mysql -u root -p krili_db < transaction_schema.sql
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following configuration:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=krili_db

# Security Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
ENCRYPTION_KEY=your-32-byte-encryption-key-here-change-this

# Payment Provider Keys
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
PAYPAL_SECRET_KEY=your_paypal_secret_key_here

# Server Configuration
SERVER_PORT=8080
GIN_MODE=release
```

### Payment Provider Setup

#### Stripe Setup
1. Create a [Stripe account](https://stripe.com)
2. Get your API keys from the Stripe dashboard
3. Add your secret key to the `.env` file
4. Configure webhooks for transaction updates

#### PayPal Setup
1. Create a [PayPal Developer account](https://developer.paypal.com)
2. Create a new application
3. Get your client ID and secret
4. Add credentials to the `.env` file

## 📡 API Endpoints

### Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Payment Endpoints

#### Process Payment
```http
POST /api/v1/payments
Content-Type: application/json

{
  "amount": 410.00,
  "currency": "USD",
  "payment_method": "card",
  "item_id": 123,
  "card_details": {
    "number": "4242424242424242",
    "expiry_month": "12",
    "expiry_year": "25",
    "cvv": "123",
    "holder_name": "John Doe"
  },
  "billing_info": {
    "country": "US",
    "zip_code": "12345"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Payment processed successfully",
  "transaction_id": "PAY_1640995200_123456",
  "status": "completed"
}
```

### Payout Endpoints

#### Request Payout
```http
POST /api/v1/payouts
Content-Type: application/json

{
  "amount": 500.00,
  "currency": "USD",
  "payout_method": "bank",
  "bank_details": {
    "account_holder": "John Doe",
    "bank_name": "Chase Bank",
    "account_type": "checking",
    "routing_number": "123456789",
    "account_number": "1234567890"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Payout request processed successfully",
  "transaction_id": "OUT_1640995200_789012",
  "status": "pending"
}
```

### Balance and History

#### Get User Balance
```http
GET /api/v1/balance
```

**Response:**
```json
{
  "user_id": 123,
  "available_balance": 1247.50,
  "pending_balance": 250.00,
  "total_earnings": 2500.00,
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Get Transaction History
```http
GET /api/v1/transactions?limit=20&offset=0
```

**Response:**
```json
{
  "transactions": [
    {
      "id": 1,
      "user_id": 123,
      "type": "payment",
      "amount": 410.00,
      "currency": "USD",
      "status": "completed",
      "payment_method": "card",
      "transaction_ref": "PAY_1640995200_123456",
      "processing_fee": 11.89,
      "net_amount": 398.11,
      "created_at": "2024-01-15T10:30:00Z",
      "completed_at": "2024-01-15T10:30:05Z"
    }
  ]
}
```

## 🔧 Development

### Running in Development Mode

```bash
# Set development mode
export GIN_MODE=debug

# Run with hot reload (install air first: go install github.com/cosmtrek/air@latest)
air

# Or run directly
go run transaction_handler.go
```

### Testing

```bash
# Run tests
go test ./...

# Run tests with coverage
go test -cover ./...

# Run specific test
go test -run TestProcessPayment
```

### Database Migrations

```bash
# Run migrations
mysql -u root -p krili_db < transaction_schema.sql

# Backup database
mysqldump -u root -p krili_db > backup.sql
```

## 🛡️ Security Best Practices

### Data Protection
- **Encryption**: All sensitive data is encrypted using AES-256
- **PCI Compliance**: Card data is never stored in plain text
- **Data Retention**: Sensitive data is automatically purged
- **Access Control**: Role-based access to sensitive operations

### Network Security
- **HTTPS Only**: All communications must use HTTPS in production
- **CORS**: Properly configured cross-origin resource sharing
- **Rate Limiting**: Protection against brute force attacks
- **Input Validation**: All inputs are validated and sanitized

### Monitoring and Logging
- **Audit Trail**: Complete transaction audit logging
- **Security Events**: Automatic detection of suspicious activities
- **Error Tracking**: Comprehensive error logging and monitoring
- **Performance Metrics**: Real-time performance monitoring

## 📊 Monitoring and Maintenance

### Health Checks
```http
GET /health
```

### Log Files
- **Application Logs**: `logs/transaction-YYYYMMDD.log`
- **Error Logs**: `logs/error-YYYYMMDD.log`
- **Security Logs**: `logs/security-YYYYMMDD.log`

### Database Maintenance
```bash
# Create backup
./backup.sh

# Monitor database performance
mysql -u root -p -e "SHOW PROCESSLIST;"

# Check table sizes
mysql -u root -p krili_db -e "
SELECT 
    table_name AS 'Table',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = 'krili_db'
ORDER BY (data_length + index_length) DESC;
"
```

## 🚀 Deployment

### Production Deployment

1. **Server Setup**
   ```bash
   # Install dependencies
   sudo apt update
   sudo apt install mysql-server nginx certbot

   # Setup SSL certificate
   sudo certbot --nginx -d yourdomain.com
   ```

2. **Application Deployment**
   ```bash
   # Build for production
   CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o transaction-handler transaction_handler.go

   # Create systemd service
   sudo cp krili-transaction.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable krili-transaction
   sudo systemctl start krili-transaction
   ```

3. **Nginx Configuration**
   ```nginx
   server {
       listen 443 ssl;
       server_name yourdomain.com;

       ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

       location /api/ {
           proxy_pass http://localhost:8080;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

### Docker Deployment

```dockerfile
FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o transaction-handler transaction_handler.go

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/

COPY --from=builder /app/transaction-handler .
COPY --from=builder /app/.env .

CMD ["./transaction-handler"]
```

```bash
# Build and run with Docker
docker build -t krili-transaction .
docker run -p 8080:8080 krili-transaction
```

## 🐛 Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check MySQL status
sudo systemctl status mysql

# Test connection
mysql -u root -p -e "SELECT 1;"

# Check user permissions
mysql -u root -p -e "SHOW GRANTS FOR 'krili_user'@'localhost';"
```

#### Payment Processing Issues
- **Invalid API Keys**: Verify Stripe/PayPal credentials
- **Network Issues**: Check firewall and network connectivity
- **Rate Limiting**: Implement proper retry logic
- **Webhook Failures**: Verify webhook endpoints and signatures

#### Performance Issues
```bash
# Check system resources
top
df -h
free -m

# Monitor database performance
mysql -u root -p -e "SHOW FULL PROCESSLIST;"

# Check application logs
tail -f logs/transaction-$(date +%Y%m%d).log
```

## 📚 Additional Resources

- [Go Documentation](https://golang.org/doc/)
- [Gin Framework](https://gin-gonic.com/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Stripe API Documentation](https://stripe.com/docs/api)
- [PayPal API Documentation](https://developer.paypal.com/docs/api/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the logs for error details

---

**⚠️ Security Notice**: Never commit sensitive information like API keys, passwords, or encryption keys to version control. Always use environment variables for sensitive configuration.