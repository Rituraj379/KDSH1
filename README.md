# Amazon Clone

Modernized Amazon-style storefront with a Vite React frontend and a new FastAPI backend. The legacy Express/Mongo backend is still kept in `amazon-backend` for reference, but the recommended backend is now `fastapi-backend`.

## Modern Stack

- Frontend: React 18, Vite, Redux, MUI, Axios
- Backend: FastAPI, Uvicorn, JSON-backed local development store
- API contract: `/api/products`, `/api/users`, `/api/orders`, `/api/config/paypal`
- AI-ready hook: `/api/agent/chat`

## Quick Start

Shortcut scripts are available from the project root:

```powershell
npm run frontend:install
npm run api:install
npm run api:dev
npm run frontend:dev
```

Or run each side manually:

Install frontend packages:

```powershell
npm --prefix amazon-frontend install
```

Install backend packages:

```powershell
python -m venv fastapi-backend\.venv
fastapi-backend\.venv\Scripts\Activate.ps1
pip install -r fastapi-backend\requirements.txt
```

Start the backend:

```powershell
cd fastapi-backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Start the frontend in another terminal:

```powershell
npm --prefix amazon-frontend run dev
```

Open `http://localhost:3000`.

## Demo Login

- Email: `admin2023@gmail.com`
- Password: `1234`

## Configuration

- Frontend API URL: copy `amazon-frontend/.env.example` to `amazon-frontend/.env`
- Backend env values: copy `fastapi-backend/.env.example` to `fastapi-backend/.env`
- API docs: `http://localhost:8000/docs`

## Features

- Register and sign in
- Update user profile
- Browse, search, and filter products
- Add products to cart
- Create orders
- View order history and order details
- PayPal SDK integration point
- Future AI agent route placeholder
