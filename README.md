# 🤖 AI Booking Assistant

A modern, conversational AI-powered booking assistant with RAG (Retrieval-Augmented Generation) capabilities, built with Streamlit, OpenAI, and SQLite.

## 🎯 Features

### Core Functionality
- **Chat-based Booking**: Natural conversational flow for booking collection
- **RAG (Retrieval-Augmented Generation)**: Upload PDFs and retrieve answers using semantic search
- **Intent Detection**: Automatically detects booking vs. general queries
- **Smart Collection**: Gathers required booking details (name, email, phone, service, date, time)
- **Email Confirmations**: Sends confirmation emails after successful bookings
- **Admin Dashboard**: Complete booking management with filtering and analytics

### Technical Features
- **Conversation Memory**: Maintains last 20-25 messages for context
- **Input Validation**: Email, phone, date, and time validation
- **Error Handling**: Graceful error messages and recovery
- **SQLite Database**: Persistent data storage
- **Modular Design**: Clean separation of concerns
- **Tool System**: RAG, Booking, Email, and Search tools

## 📋 Project Structure

```
AI_UseCase/
├── app/
│   ├── main.py                 # Streamlit entry point
│   ├── chat_logic.py           # Intent detection & conversation memory
│   ├── booking_flow.py         # Slot filling & confirmation logic
│   ├── rag_pipeline.py         # PDF processing & semantic search
│   ├── admin_dashboard.py      # Admin UI for booking management
│   ├── tools.py                # Tool implementations (RAG, Booking, Email, Search)
│   ├── config.py               # Configuration constants
│   └── __init__.py
│
├── db/
│   ├── database.py             # SQLite operations
│   ├── models.py               # SQLAlchemy ORM models
│   └── __init__.py
│
├── .streamlit/
│   └── config.toml            # Streamlit configuration
│
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── booking_assistant.db        # SQLite database (auto-created)
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- OpenAI API key (for LLM and embeddings)
- SMTP credentials (for email confirmations)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.streamlit/secrets.toml` file:

```toml
OPENAI_API_KEY = "your-openai-api-key"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password"
```

### 3. Run the Application
```bash
streamlit run app/main.py
```

The app will open at `http://localhost:8501`

## 📖 Usage Guide

### For Users (Booking)

1. **Start Chat**: Open the app and see the welcome message
2. **Book Appointment**: Say "I want to book" (Option 1)
3. **Auto-Redirect**: You'll be taken to the admin dashboard
4. **Login**: Enter password: `admin123`
5. **Create Booking**: Click "✨ New Booking" tab and fill the form
6. **Confirm**: Click "✅ Create Booking"
7. **Confirmation**: Receive email with booking details

### For Users (RAG)

1. **Upload PDFs**: Use PDF upload in sidebar (Option 2)
2. **Ask Questions**: Type your questions about the services
3. **Get Answers**: System retrieves relevant sections and generates answers

### For Admins

1. **Access Dashboard**: Click admin button (password: `admin123`)
2. **Navigate Tabs**:
   - **✨ New Booking**: Create new bookings
   - **📈 Overview**: View metrics and recent bookings
   - **📅 All Bookings**: See all bookings with search
   - **🔍 Advanced Filter**: Filter by service, status, date
   - **📊 Analytics**: Charts and timeline view

## ✨ Core Requirements Met

- ✅ **RAG Chatbot**: PDF upload + semantic search
- ✅ **Conversational Booking**: Multi-turn dialogue with slot filling
- ✅ **Data Storage**: SQLite with proper schema
- ✅ **Email Confirmation**: SMTP integration
- ✅ **Tool Calling**: RAG, Booking, Email, Search tools
- ✅ **Frontend & Backend**: Streamlit with admin dashboard
- ✅ **Short-Term Memory**: 20-25 message conversation history
- ✅ **Error Handling**: Comprehensive validation and recovery

## 🚀 Deployment

### Local Testing
```bash
streamlit run app/main.py
```

### Streamlit Cloud Deployment

1. Push code to GitHub
2. Go to share.streamlit.io
3. Connect GitHub repository
4. Select `app/main.py` as entry point
5. Add secrets in dashboard
6. Deploy!

## 📝 Troubleshooting

### "Email not sending"
- Check SMTP credentials in `.streamlit/secrets.toml`
- Booking still saves even if email fails (graceful degradation)

### "PDF not being processed"
- Ensure PDF is valid and not corrupted
- Check OpenAI API key is set correctly

## 🔐 Security Notes

- Never commit `.streamlit/secrets.toml` to Git
- Keep API keys secure in environment variables
- Input validation prevents SQL injection

## 📚 Dependencies

See `requirements.txt` for complete list

---

**Status**: ✅ Production Ready  
**Version**: 1.0
