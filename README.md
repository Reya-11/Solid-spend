📋 Expense Tracker
A smart, full-stack expense tracking application featuring automated receipt processing with OCR. This project is designed to demonstrate robust backend engineering, clean API design, and a "dumb" but functional frontend.

Core Features:
Receipt OCR: Upload a receipt image to automatically extract the merchant, date, and total amount.
Multi-Currency Support: Record expenses in any currency and see totals automatically normalized to your chosen base currency.
CRUD Operations: Full Create, Read, Update, and Delete functionality for all your expenses.
Analytics Dashboard: Visualize spending habits with charts for spending by category, by merchant, and over time.
CSV Export: Download all your expense data with a single click for personal records or accounting.
User Preferences: Set your preferred base currency for normalization.

Tech Stack:
Backend - Python 3.10+, FastAPI, SQLAlchemy, Pytesseract (OCR), Pillow, PostgreSQL, httpx
Frontend - React 18, Vite, Tailwind CSS, Axios, Recharts
APIs - ExchangeRate-API for currency conversion
