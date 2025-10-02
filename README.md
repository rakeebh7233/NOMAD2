# NOMAD 🌍✈️

### All-in-one collaborative travel planning and budgeting app with smart recommendations

## 📖 Overview

Planning a trip today often means juggling multiple apps for flights, hotels, activities, and budgeting. This can quickly become overwhelming. NOMAD solves this problem by bringing everything into one collaborative platform.

With NOMAD, users can:
* Build personalized itineraries
* Manage budgets and savings plans
* Get AI-driven recommendations for trips that fit their profile and finances
* Collaborate with friends and family on shared itineraries
* Redirect seamlessly to trusted booking providers (e.g., Booking.com, TripAdvisor) to finalize purchases

## 🚀 Features
**1. User Profiles & Authentication**
* Create a profile with secure login.
* Store preferences and travel origin for tailored recommendations.
  
**2. Itinerary Creation**
* Select travel dates, destination, accommodations, and activities.
* Confirm and customize itineraries with flexibility to add/remove items.
  
**3. Budgeting & Savings**
* Get a detailed trip cost breakdown (travel, lodging, activities).
* Create savings goals (weekly, biweekly, monthly).
* Track progress toward funding future trips.
  
**4. Recommendations**
* AI-driven travel suggestions based on savings, profile, and preferences.
* Filter itineraries that fit within a set budget.
  
**5. Collaboration**
* Share itineraries with other users.
* Plan trips together and keep all details in sync.

**6. External Integrations**
* Direct booking redirection to trusted travel providers.
* Powered by TripAdvisor and Booking.com APIs.
  
**7. Trip Feedback**
* Users can rate and review their trips within NOMAD.

## 🛠 Tech Stack
### Frontend
* React (UI)
* Node.js (runtime environment)
### Backend
* FastAPI (REST API framework)
* Uvicorn (ASGI server)
### Database
* PostgreSQL (relational database)
* SQLAlchemy (ORM)
* Alembic (migrations)
### Authentication & Security
* Passlib[bcrypt] (password hashing)
* PyJWT / python-jose (JWT handling for authentication)
### Configuration & Networking
* python-dotenv (environment configs)
* requests (API requests)
### Machine Learning (Recommendations)
* PyTorch (modeling)
* Pandas, scikit-learn (data processing & ML pipeline)
### External APIs
* TripAdvisor API
* Booking.com API

## ▶️ Usage
### Workflow 1: Itinerary Creation
```bash
User → Login/Register  
     → Select Destination + Dates  
     → Browse Flights/Hotels/Activities  
     → Build & Confirm Itinerary  
     → View Budget Breakdown + Savings Plan  
     → Redirect to Providers for Booking
```
### Workflow 2: Getting Recommendations
```
User → Login/Register  
     → Add Savings Progress (no fixed trip)  
     → AI Engine Suggests Itineraries  
     → User Selects & Customizes Recommendation  
     → Redirect to Providers for Booking
```
### Workflow 3: Finance & Budget Tracking
```
User → Login/Register  
     → Set Savings Goal (weekly/biweekly/monthly) OR Skip Goal  
     → Log Savings Progress  
     → Track Savings Toward Trip Budget  
     → (Optional) Receive Suggested Trips That Fit Current Savings
```
### Workflow 4: Trip Review
```
User → Login/Register  
     → View Past Trips (created or recommended)  
     → Rate Trip Experience  
     → Leave Optional Review/Feedback  
     → Submit Review (stored for future reference and improvements)
```
## ⚙️ Installation
### Prerequisites
* Node.js
* Python 3.10+
* PostgreSQL
### Steps

1. Clone the repository:
```bash
git clone <repo_url>
cd nomad
```
2. Set up the backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
3. Set up the frontend:
```bash
cd frontend
npm install
npm start
```
4. Configure environment variables (.env):
* Database connection (PostgreSQL)
* API keys (TripAdvisor, Booking.com)
---
### ✍️ Authors
**Rakeeb Hossain** | **Sunan Tajwar**| **Nihal Rahman**

  
