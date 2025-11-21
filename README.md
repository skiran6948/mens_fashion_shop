Men's Fashion E-Commerce Website (Django)

A fully functional Men's Fashion E-Commerce web application built using Django, featuring:
Product listings & categories
Product detail pages
Cart system
Order checkout
User authentication
Search with suggestions
Admin dashboard
PostgreSQL support
Fully structured APIs (Django REST Framework)
This project is designed for production-level e-commerce workflows and integrates both server-side rendered pages and REST APIs for mobile/React apps.

🚀 Features
🛍 User Features

Browse products by category
Product detail pages with images
Add to cart / remove from cart
Update quantity
Place orders
Track order history
Search with live suggestions
Authentication (login/register)

🛒 Cart

Add/Remove products
Auto-update quantities
Session-based cart management
Checkout page

📦 Orders

Store customer info
Order summary page
User order history

📊 Admin Features

Add/Edit products
Manage categories
View orders
Update order status
Custom analytics dashboard:
Sales timeline
Top-selling products
Revenue charts

🔥 API Features (DRF)
/api/products/
/api/products/<slug>/
/api/categories/
/api/category/<slug>/
/api/search/
/api/search/suggestions/
/api/cart/
/api/cart/add/
/api/cart/remove/
/api/orders/
/api/auth/login/
/api/auth/register/

🛠️ Tech Stack
Layer	Technology
Backend	Django 5, Django REST Framework
Database	PostgreSQL
Frontend	HTML, CSS, JS
Auth	Django Auth + JWT
API	DRF ViewSets, JWT
Dev Tools	Git, Postman, pgAdmin



📁 Project Structure
mens_fashion_shop/
│ manage.py
│ requirements.txt
├── mensshop/        # Main project settings
├── store/           # Products, categories, orders
├── cart/            # Cart functionality
├── accounts/        # Login/register
├── media/           # Uploaded images
└── templates/       # HTML templates

