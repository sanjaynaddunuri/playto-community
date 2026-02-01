# 🚀 Playto Community Feed

A **full-stack Community Feed prototype** with **threaded discussions**, **likes-based gamification**, and a **dynamic 24-hour leaderboard**, built using **Django REST Framework** and **React + Tailwind CSS**.

---

## ✨ Features

### 📰 Community Feed
- Text posts with author and content
- Scrollable feed (25+ demo posts)

### 💬 Threaded Comments
- Unlimited nested replies (Reddit-style)
- Optimized backend queries (no N+1 problem)

### ❤️ Likes & Gamification
- Post Like = **5 Karma**
- Comment Like = **1 Karma**
- DB-level protection against double likes

### 🏆 Leaderboard (Last 24 Hours)
- Top users by karma earned in last 24h
- Calculated dynamically from activity history
- No cached or stored karma fields

### 🎨 Professional Frontend
- React + Tailwind CSS
- Dark modern UI
- Loading skeletons
- Error-safe rendering
- Sticky leaderboard

---

## 🧠 Tech Stack

**Backend**
- Django
- Django REST Framework
- SQLite (dev)
- django-cors-headers

**Frontend**
- React (Vite)
- Tailwind CSS
- Axios

---

## 📁 Project Structure

```
playto-community/
├── backend/
│   ├── manage.py
│   ├── db.sqlite3
│   ├── backend/
│   └── community/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       └── management/commands/seed_data.py
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   └── src/
│       ├── api.js
│       ├── App.jsx
│       ├── main.jsx
│       ├── components/
│       └── styles/
│
└── README.md
```

---

## ⚙️ Setup Instructions

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install django djangorestframework django-cors-headers
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data
python manage.py runserver
```

Backend runs at:
```
http://127.0.0.1:8000
```

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:
```
http://localhost:5173
```

---

## 🧪 Verification Checklist

✔ Feed scrolls with 25 posts  
✔ Nested comments visible  
✔ Like buttons functional  
✔ Leaderboard populated (15–20 users)  
✔ No CORS errors  

---

## 👨‍💻 Author

**Naddunuri Sanjay**  
Computer Science Engineer | Full-Stack Developer

---

⭐ Built for the **Playto Engineering Challenge**
