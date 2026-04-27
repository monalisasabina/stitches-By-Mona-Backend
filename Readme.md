# 🧶 Stitches by Mona Backend API 🧶 

This is the backend for **Stitches by Mona**, a crochet and knitting business.
It is built using **Flask** and **Flask-RESTful**, providing APIs for products, orders, customers, custom orders, and a simple chatbot.

---

## 📁 Project Structure

```
├── chatbot 
│   └── chatbot_responses.py
├── config.py
├── instance
│   └── stitches_by_mona.db
├── migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── initial migration files...
├── models
│   ├── __init__.py
│   ├── custom_order.py
│   ├── customer.py
│   ├── order.py
│   └── product.py
├── routes
│   ├── __init__.py
│   ├── chat.py
│   ├── custom_order.py
│   ├── customers.py
│   ├── home.py
│   ├── order.py
│   └── products.py
├── run.py
└── seed.py
```

---

## 🚀 Features

* 🛍️ Product management (create, view, update)
* 📦 Order handling
* 👤 Customer management
* 🧵 Custom order requests
* 💬 Simple keyword-based chatbot
* 🗃️ Database migrations with Flask-Migrate

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd stitches-by-mona-backend
```

### 2. Install dependencies

Using pipenv:

```bash
pipenv install
pipenv shell
```

### 3. Set environment variables

```bash
export FLASK_APP=run.py
export FLASK_ENV=development
```

---

### 4. Run migrations

```bash
flask db upgrade
```

---

### 5. Seed the database 

```bash
python seed.py
```

---

### 6. Run the server

```bash
flask run
```

Server will run at:

```
http://127.0.0.1:5000
```

---

## 💬 Chatbot

The chatbot is a simple keyword-based system.

### Location

```
chatbot/chatbot_responses.py
```

### How it works

* User sends a message via `/chat` endpoint
* Message is matched against predefined keywords
* a corresponding response is returned
* If no match is found, a default fallback response is used

### Example Request

```json
{
  "message": "do you deliver"
}
```

### Example Response

```json
{
  "response": "Yes we do! 🚚 Nairobi deliveries take 1-2 days and countrywide takes 3-5 days via G4S."
}
```

---

## 📡 API Endpoints (Overview)

| Endpoint            | Description         |
| --------------------| ------------------- |
| `/`                 | Home route          |
| `/products`         | Product operations  |
| `/orders`           | Order management    |
| `/customers`        | Customer management |
| `/custom-orders`    | Custom orders       |
| `/chat`             | Chatbot interaction |

---

## 🧠 Future Improvements

* Upgrade chatbot to intent-based or AI-powered responses
* Add authentication (JWT)
* Improve error handling and validation
* Add image uploads for products
* Deploy to production (Render)

---

## 👩🏾‍💻 Author

Built by Mona 💛
Software developer & crochet enthusiast 🧶
