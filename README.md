# 🤖 Woloo AI WhatsApp Chatbot 🚻  
**"Find a Loo & More" – directly on WhatsApp**

This AI-powered WhatsApp chatbot helps users locate the nearest Woloo washrooms across India by sharing their live location. Built using Python (Flask), MySQL, Twilio, and Google Maps, the bot provides directions, ratings, and estimated walking times – all from within WhatsApp.
![Preview]![Screenshot 2024-09-18 191257](https://github.com/user-attachments/assets/5c04f3e7-3b82-406e-9e59-f503f5d0ed25)
 ![Screenshot 2025-05-09 151327](https://github.com/user-attachments/assets/ef3ee394-e875-4dd4-b1c3-0915209ac259)
 ![Screenshot 2025-05-09 150925](https://github.com/user-attachments/assets/61d1ffe5-3aff-4a4e-8fa7-cfb3aa0d7baf)
 ![Screenshot 2025-05-09 151258](https://github.com/user-attachments/assets/073c6b0d-e38c-4bf8-8158-6554f61b2181)
 ![Screenshot 2025-05-09 151639](https://github.com/user-attachments/assets/c38c030d-1fa1-4c9d-b927-4f88242e155e)

 




---

## 📲 How It Works

1. User sends a message like **"Hi"** to the chatbot.
2. The bot replies with a welcome message and menu options:
    - Find Nearest Woloo’s
    - Learn More
    - Download App
    - Contact Support
3. When the user shares their location, the bot:
    - Fetches and ranks nearby Woloo washrooms from a database
    - Calculates distances and estimated walking times using Haversine formula
    - Sends clickable location links with ratings and directions
    - Includes download and support links

---

## 🧠 Key Features

- ✅ AI WhatsApp chatbot built with **Twilio**
- 📍 Real-time location support
- 🔍 Finds nearest 4 washroom locations
- 📊 Displays distance, rating & estimated walking time
- 🌐 Sends Google Maps view link with route
- 🧼 Curated list of 25000+ Woloo washrooms
- 💬 Simple command-based interaction
- 🗃️ Data stored in MySQL and updated as users return

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Chat API:** Twilio WhatsApp
- **Frontend (Map View):** HTML, CSS, JS, Google Maps API
- **Database:** MySQL (MySQL Workbench)
- **Other:** Flask-CORS, Twilio SDK, Haversine formula for geolocation

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- MySQL server
- Google Maps JavaScript API key
- Twilio account (with WhatsApp sandbox enabled)

---
## Preview
