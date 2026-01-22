# Quick Start Guide - AI Booking Assistant

## 🚀 Getting Started (2 minutes)

### 1. ✅ Email is Already Configured
- **Sender**: divijanandanadavire@gmail.com
- **Status**: ✅ TESTED & WORKING
- **Last Test**: January 21, 2026 - Email sent successfully!

### 2. 🔗 Access the App
**URL**: http://localhost:8501

### 3. 💬 Chat Features

#### Try Booking
```
You: "I want to book an appointment"
Bot: "Great! Let's book... What's your name?"
(Follow the prompts to complete booking)
```

#### Try RAG (Q&A)
```
1. Click "PDF UPLOAD" on left sidebar
2. Upload a PDF document
3. Ask a question about the document
Bot: Answers based on the PDF content
```

#### View Admin Dashboard
```
1. Click "📊 Admin Dashboard" button in chat
2. Enter password: admin123
3. View all bookings, analytics, filters
```

---

## 📋 What's Implemented

### Booking Flow (One at a time)
- ✅ Customer Name (text)
- ✅ Email (validated)
- ✅ Phone (8-15 digits)
- ✅ Service Type (predefined)
- ✅ Date (📅 calendar picker)
- ✅ Time (⏰ time picker)
- ✅ Confirmation (yes/no)
- ✅ Email sent (if configured)
- ✅ Booking saved to database

### Admin Dashboard
- ✅ View all bookings
- ✅ Search by name/email
- ✅ Filter by date, service, status
- ✅ Analytics & charts
- ✅ Edit/cancel/delete bookings
- ✅ Export to CSV

### RAG System
- ✅ Upload PDFs
- ✅ Extract & chunk text
- ✅ Embed with OpenAI
- ✅ Retrieve & answer questions
- ✅ Multiple documents supported

### Email Notifications
- ✅ Sends after booking confirmation
- ✅ Includes booking details
- ✅ Gmail with 2FA app password
- ✅ Error messages if fails

### Database
- ✅ SQLite storage
- ✅ Customer & Booking tables
- ✅ Relationships & integrity
- ✅ Query by email, date, ID

---

## 🧪 Testing the System

### Test Email
```bash
cd c:\Users\dell\Desktop\AI_UseCase
python test_email_simple.py
# Should show: SUCCESS: Email is working!
```

### Test Booking Flow
1. Open http://localhost:8501
2. Say "I want to book"
3. Enter: John Doe
4. Enter: john@example.com
5. Enter: 1234567890
6. Enter: Medical Consultation
7. Pick date from calendar
8. Pick time from clock
9. Say "yes" to confirm
10. See booking saved ✅
11. Check admin dashboard for booking

### Test Admin Dashboard
1. Click "📊 Admin Dashboard"
2. Password: admin123
3. View your bookings
4. Try filters
5. View charts

### Test RAG
1. Click "Browse files" under PDF UPLOAD
2. Upload a PDF
3. Ask "What services are available?"
4. Bot answers from PDF

---

## ⚙️ Configuration

### Email
File: `.streamlit/secrets.toml`
```toml
OPENAI_API_KEY = "sk-proj-..." (configured ✅)
EMAIL_SENDER = "divijanandanadavire@gmail.com" (configured ✅)
EMAIL_PASSWORD = "vhxxoddokgvohxje" (configured ✅)
```

### OpenAI
- Using GPT-4-turbo-preview for complex responses
- Using gpt-3.5-turbo for simple queries
- API key: Pre-configured in secrets

### Database
- File: `booking_assistant.db`
- Auto-creates on first run
- SQLite (no setup needed)

---

## 📊 Key Features Checklist

| Feature | Status | Location |
|---------|--------|----------|
| Chat Interface | ✅ | Left side of screen |
| PDF Upload | ✅ | Left sidebar |
| Booking Form | ✅ | Main chat area |
| Admin Dashboard | ✅ | Sidebar button |
| Email Confirmation | ✅ | After booking |
| Conversation Memory | ✅ | Last 25 messages |
| Error Messages | ✅ | Chat responses |
| Data Validation | ✅ | All forms |

---

## 🆘 Troubleshooting

### Email not sending?
```
Check:
1. Is the app running? (http://localhost:8501)
2. Check app logs for error message
3. Run: python test_email_simple.py
4. Result shows error details
```

### Admin Dashboard not loading?
```
Check:
1. Password correct? (admin123)
2. Any bookings in database?
3. Browser console for errors (F12)
```

### PDF not uploading?
```
Check:
1. File is .pdf format?
2. File size < 200MB?
3. Try different PDF
```

### Booking not saved?
```
Check:
1. All fields filled?
2. Clicked "yes" to confirm?
3. Check database: booking_assistant.db
```

---

## 🎯 Next Steps

### Deploy to Streamlit Cloud
```
1. Push code to GitHub
2. Go to streamlit.io/cloud
3. Connect repository
4. Add secrets:
   - OPENAI_API_KEY
   - EMAIL_SENDER
   - EMAIL_PASSWORD
5. Deploy!
```

### Customize for Your Domain
Edit `app/config.py`:
```python
SERVICE_TYPES = [
    "Salon/Haircut",
    "Medical Consultation",
    "Hotel Booking",
    "Event Reservation",
    "Class/Training",
    "Your Custom Service"
]
```

### Add More Features
- STT for voice input
- TTS for voice output
- SMS notifications
- Payment integration
- Calendar sync
- Booking reminders

---

## 📞 Support

### Email Issue?
The test script shows exactly what's wrong:
```bash
python test_email_simple.py
```

### Database Issue?
Delete the database to reset:
```bash
rm booking_assistant.db
```
It will recreate on next run.

### Want to Debug?
Check the terminal where Streamlit is running:
```
Local URL: http://localhost:8501
```
Logs appear there in real-time.

---

## 🎉 You're All Set!

Your AI Booking Assistant is:
- ✅ Fully functional
- ✅ Email tested & working
- ✅ Admin dashboard ready
- ✅ Database initialized
- ✅ RAG system active
- ✅ Ready for deployment

**Start using it now**: http://localhost:8501

**Questions?** Check IMPLEMENTATION_CHECKLIST.md for detailed specs.

