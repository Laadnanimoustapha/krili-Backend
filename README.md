[![Support Palestine](https://img.shields.io/badge/Support-Palestine-000000?labelColor=007A3D&color=CE1126)](#support-palestine)
[![Free Palestine](https://img.shields.io/badge/Free-Palestine-CE1126?labelColor=000000&color=007A3D)](#support-palestine)
      MADE BY LAADNANI


# Krili Backend API

A Python Flask backend for the Krili peer-to-peer rental marketplace.

## Features

- User authentication with JWT tokens
- Item listing management
- Rental booking system
- User profiles and reviews
- Category management
- MySQL database integration

## Setup

### 1. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update with your database credentials:

\`\`\`bash
cp .env.example .env
\`\`\`

### 3. Run the Application

\`\`\`bash
python app.py
\`\`\`

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/verify-token` - Verify JWT token
- `GET /api/auth/profile` - Get current user profile

### Items
- `GET /api/items` - Get all items with filters
- `GET /api/items/<id>` - Get item details
- `POST /api/items` - Create new item (requires auth)

### Rentals
- `POST /api/rentals` - Create rental booking (requires auth)
- `GET /api/rentals/user` - Get user rentals (requires auth)

### Categories
- `GET /api/categories` - Get all categories
- `GET /api/categories/<id>` - Get category details

### Users
- `GET /api/users/<id>` - Get user profile
- `PUT /api/users/profile` - Update profile (requires auth)

## Authentication

Include JWT token in request headers:

\`\`\`
Authorization: Bearer <your_jwt_token>
\`\`\`

## Database

The backend connects to a MySQL database with the following tables:
- users
- items
- rentals
- categories
- reviews
- wishlist
- conversations
- messages
- notifications
- payments
- disputes
- And more...

## Frontend Integration

When hosting the backend, update the frontend API base URL in your Next.js app:

\`\`\`typescript
const API_BASE_URL = 'https://your-backend-url.com/api'
\`\`\`

## Deployment

1. Set `FLASK_ENV=production`
2. Update database credentials in `.env`
3. Update `CORS_ORIGINS` with your frontend URL
4. Deploy using your preferred hosting service (Heroku, AWS, DigitalOcean, etc.)
