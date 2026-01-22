# 🩺 DocAI – AI Health Assistant

DocAI is a Streamlit-based AI health assistant that allows users to chat with an AI, upload PDFs for question answering, and book medical appointments through a conversational interface. It also provides an admin dashboard to manage bookings and sends email confirmations to users.

---

## 🚀 Features

### 💬 Chat Assistant
- Interactive chat interface using Groq LLM  
- Maintains short-term conversation memory  

### 📄 PDF Question Answering
- Upload any PDF document  
- Text extraction using PyPDF  
- Chunking + retrieval-based answering  
- Responds only using document context  

### 📅 Appointment Booking
- Conversational booking flow:
  - Name  
  - Email  
  - Phone  
  - Booking type  
  - Date  
  - Time  
- Input validation (email, phone, date)  
- Confirmation step before saving  
- Stores data in SQLite database  

### 🧑‍💻 Admin Dashboard
- View all stored bookings  
- Clean table-based display  
- Persistent storage  

### 📧 Email Notification
- Sends confirmation email after booking  
- Handles failures gracefully without crashing  

---

## 🛠️ Tech Stack

- **Frontend / App Framework**: Streamlit  
- **LLM**: Groq (LLaMA 3)  
- **PDF Processing**: PyPDF  
- **Database**: SQLite  
- **Language**: Python  
- **Email Service**: SMTP (Gmail)  

---

## 📂 Project Structure

```text
medai project/
│
├── app.py              # Main Streamlit application
├── db.py               # Database logic
├── booking.py          # Booking intent + validation
├── admin.py            # Admin dashboard
├── emailer.py          # Email logic
│
├── raggpipeline.py     # RAG pipeline
├── tools.py            # Helper tools
│
├── bookings.db         # SQLite DB (local only)
├── appointments.db     # Secondary DB
│
├── requirements.txt    # Dependencies
├── README.md           # Documentation
├── test_import.py      # Debug utility
│
├── .streamlit/
│   └── secrets.toml    # Secrets (not pushed to GitHub)
│
├── docs/               # Sample PDFs
└── __pycache__/        # Python 
---

▶️ How to Run Locally

1. Install dependencies:

pip install -r requirements.txt

2. Add secrets in .streamlit/secrets.toml:

GROQ_API_KEY = "your_groq_api_key"
EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"

3. Run the app:

streamlit run app.py

🌐 Deployment

Push the project to GitHub

Go to https://streamlit.io/cloud

Select repository and deploy

Add secrets in Streamlit Cloud settings

🔮 Future Improvements (Healthcare-Focused)
🧠 Clinical Intelligence

Symptom-based intelligent triage

Medical knowledge integration (WHO, NHS, Mayo Clinic)

Drug interaction and safety checker

🏥 Hospital-Level Features

Doctor profiles and availability

Real-time slot booking system

Patient history and records

🔐 Security & Privacy

Patient authentication

Encrypted medical data

Privacy-first handling (HIPAA/GDPR inspired)

📱 Patient Experience

WhatsApp/SMS reminders

Voice-based assistant

Multilingual support

Prescription upload

Follow-up reminders

🤖 AI Enhancements

Embeddings-based semantic search

Personalized recommendations

Automatic appointment summaries

Doctor-side AI insights dashboard

👩‍💻 Author

Dasari Manasa Sowmya
Final-year B.Tech student (AI & ML)
SRM University AP