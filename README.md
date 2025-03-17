# CurrencyGlow

A sleek, modern exchange rate application with a credit-based system and stunning dark-themed UI. CurrencyGlow provides real-time currency exchange rates with a user-friendly interface and comprehensive history tracking.

## 🚀 Features

- **Live Exchange Rates**: Check real-time exchange rates against Ukrainian Hryvnia (UAH)
- **Credit System**: Usage tracking with a credit-based system (1 credit per request)
- **User Authentication**: Secure JWT-based authentication
- **Exchange History**: View and filter your past currency exchange requests

## 📋 Table of Contents

- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [API Documentation](#-api-documentation)
- [Usage](#-usage)

## 💻 Technology Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Authentication**: JWT (JSON Web Tokens)
- **UI Design**: Custom CSS with Glassmorphism effects
- **Database**: PostgreSQL

## 📥 Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- Git

### Clone the Repository

```bash
git clone https://github.com/DaniellaMarchevska05/currencyGlow.git
cd currencyGlow
```

### Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root. Copy all needed environment variables names from .env.example and paste them into .env

### PostgreSQL DB

- in PostgreSQL create an empty database and put it`s properties in .env

### EXCHANGE_RATE_API_KEY

- get your EXCHANGE_RATE_API_KEY for .env here: [https://www.exchangerate-api.com/](https://www.exchangerate-api.com/)

### Run Migrations

```bash
python manage.py migrate
```

### Start the Development Server

```bash
python manage.py runserver
```

Access the application at [http://localhost:8000](http://localhost:8000)

## 📚 API Documentation

### Authentication Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/api/token/` | POST | Obtain JWT token | `{username, password}` | `{access, refresh}` |
| `/api/token/refresh/` | POST | Refresh JWT token | `{refresh}` | `{access}` |
| `/api/register/` | POST | Register new user | `{username, email, password, password_confirm}` | `{success, user}` |

### User Endpoints

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/api/balance/` | GET | Get user balance | `{username, balance}` |

### Currency Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/api/currency/` | POST | Get exchange rate | `{currency_code}` | `{currency_code, rate, created_at, balance_remaining}` |
| `/api/history/` | GET | Get exchange history | Query params: `?currency_code=USD&from_date=2023-01-01&to_date=2023-12-31` | `{count, results: [{id, currency_code, rate, created_at}]}` |

## 📝 App Structure

### Frontend Routes

| Route | Name | Description |
|-------|------|-------------|
| `/` | home | Landing page |
| `/app/` | app_home | Main app dashboard |
| `/register/` | register_page | User registration page |
| `/balance/` | balance_page | User balance information |
| `/currency/` | currency_page | Currency exchange rate lookup |
| `/history/` | history_page | Exchange rate history |

### API Routes

| Route | Name | Description |
|-------|------|-------------|
| `/api/register/` | register | User registration endpoint |
| `/api/token/` | token_obtain_pair | JWT token acquisition |
| `/api/token/refresh/` | token_refresh | JWT token refresh |
| `/api/balance/` | balance | User balance endpoint |
| `/api/currency/` | currency | Currency exchange endpoint |
| `/api/history/` | history | Exchange history endpoint |

## 🔧 Usage

### Main Page

1. Navigate to `http://127.0.0.1:8000/` to see the main page
   
![image](https://github.com/user-attachments/assets/e016f2fe-add7-45e0-942b-e691176d0a5e)

3. You can choose one of the options:
   
![image](https://github.com/user-attachments/assets/cd8a20e0-98d4-438b-94e0-b29672079b3d)


### User Registration and Login

1. Navigate to `/register/` to create a new account
   
![image](https://github.com/user-attachments/assets/a40005de-7d9a-4d49-ae0d-fa4e3e81f6a7)
![image](https://github.com/user-attachments/assets/c95d2d8c-3c4f-408b-bc10-3c710c9c467e)
  
4. After successful registration, log in with your credentials

![image](https://github.com/user-attachments/assets/3c6b704e-6403-4da2-b92b-29296def00e0)

6. You will receive 1000 credits upon registration

### Getting Exchange Rates

1. Go to the Currency page (`/currency/`)
2. Select a currency from the dropdown menu
   
![image](https://github.com/user-attachments/assets/3eb5c444-14d5-4d94-85a0-9726e7abe75e)

4. Click "Get Exchange Rate" to see the current rate against UAH

![image](https://github.com/user-attachments/assets/d6f4aacc-530d-4c13-9f42-5780dc6e4518)

6. Each request costs 1 credit from your balance
7. When your balance reaches zero, you will be notified that you need more credits

### Viewing Exchange History

1. Navigate to the History page (`/history/`)
2. Filter your history by currency and/or date range
3. View your past exchange rate requests in chronological order

![image](https://github.com/user-attachments/assets/1b494cb7-a34c-443a-9a70-7ea76e415e30)

### Viewing Balance

1. Navigate to the Balance page (`/balance/`) to see your balance

![image](https://github.com/user-attachments/assets/426e8bf4-f5f0-4684-9385-ced6359d5c40)

### Errors Handling

1. When the user\`s balance reaches 0 he or she can`t get the exchange rate

![image](https://github.com/user-attachments/assets/d557ac1e-a21e-4228-93ce-3e7d3d775ec9)

2. Password constraints:

![image](https://github.com/user-attachments/assets/d41c04a2-b56d-4157-981e-9cffd41982f7)

![image](https://github.com/user-attachments/assets/91fedf84-00d7-490a-8822-2c21a86a8db1)

3. Unregistered users can`t login

![image](https://github.com/user-attachments/assets/f56d0059-10d7-4b17-b20b-90308f967c72)

## Database Preview 

1. Table: user

![image](https://github.com/user-attachments/assets/6c2f27bd-3954-45e1-9fdf-80819808eada)

2. Table: currencyexchange

![image](https://github.com/user-attachments/assets/aa1cba33-feb9-41f7-a968-634223080a25)

3. Table: userbalance

![image](https://github.com/user-attachments/assets/9d5a0b29-0a82-42f8-8280-f9cd4a27c3e8)

### Technical Implementation

The backend is built with Django and Django REST Framework, providing a robust API layer for all operations. The frontend is implemented using vanilla JavaScript for maximum performance, with a custom CSS framework that utilizes modern design principles like glassmorphism.

The application implements a credit system where each user starts with 1000 credits, with each exchange rate request costing 1 credit. When a user's balance reaches zero, they are unable to make further requests until their balance is replenished.

---
