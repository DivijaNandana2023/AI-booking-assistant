"""
AI Booking Assistant - FINAL WORKING VERSION (UI ENHANCED)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from datetime import datetime
from config import OPENAI_API_KEY, DATABASE_PATH, SERVICE_TYPES
from chat_logic import ChatLogic, ConversationMemory
from booking_flow import BookingFlow
from rag_pipeline import RAGPipeline
from db.database import DatabaseManager
from openai import OpenAI

# ================== PAGE CONFIG ==================
st.set_page_config(page_title="AI Booking Assistant", layout="wide")

# ================== INIT ==================
client = OpenAI(api_key=OPENAI_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = ConversationMemory(max_length=25)

if "chat_logic" not in st.session_state:
    st.session_state.chat_logic = ChatLogic()

if "booking_flow" not in st.session_state:
    st.session_state.booking_flow = BookingFlow(st.session_state.chat_logic)

if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = RAGPipeline()

if "db_manager" not in st.session_state:
    st.session_state.db_manager = DatabaseManager(DATABASE_PATH)

if "show_admin" not in st.session_state:
    st.session_state.show_admin = False

# ================== HEADER ==================
st.title("🤖 AI Booking Assistant")
st.markdown("**Smart booking system with RAG, conversational booking, database storage, and admin dashboard**")

# ================== SIDEBAR ==================
with st.sidebar:
    st.markdown("### 🎮 Navigation")

    if st.button("📊 Admin Dashboard", use_container_width=True):
        st.session_state.show_admin = True
        st.rerun()

    if st.button("🔄 New Chat", use_container_width=True):
        st.session_state.show_admin = False
        st.session_state.messages = []
        st.session_state.conversation_memory.clear()
        st.session_state.chat_logic.reset_booking_context()
        st.rerun()

    st.markdown("---")

    st.markdown("### 📚 Upload PDFs (RAG)")
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        for pdf in uploaded_files:
            try:
                st.session_state.rag_pipeline.add_pdf(pdf)
                st.success(f"✅ {pdf.name} indexed")
            except Exception as e:
                st.error(f"❌ {pdf.name}: {str(e)}")

    st.markdown("---")
    st.caption(f"📖 Documents: {st.session_state.rag_pipeline.get_document_count()}")

# ================== ADMIN DASHBOARD ==================
if st.session_state.show_admin:
    from app.admin_dashboard import run_admin_dashboard
    run_admin_dashboard()
    st.stop()

# ================== CHAT UI ==================
st.markdown("---")
st.subheader("💬 Chat")

if not st.session_state.messages:
    st.info("👋 Say **I want to book** or ask a question about uploaded PDFs.")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.write(f"**👤 You:** {msg['content']}")
    else:
        st.write(f"**🤖 Assistant:** {msg['content']}")

st.markdown("---")

# ================== SMART INPUT UI ==================
current_field = None
if st.session_state.chat_logic.is_booking_in_progress():
    missing = st.session_state.chat_logic.get_missing_fields()
    if missing:
        current_field = st.session_state.booking_flow.get_next_required_field()

user_input = None
send_clicked = False

# ---------- SERVICE DROPDOWN ----------
if current_field == "booking_type":
    st.write("🛎️ **Select Service Type:**")
    selected = st.selectbox("Choose service", SERVICE_TYPES)
    send_clicked = st.button("Confirm Service")
    if send_clicked:
        user_input = selected

# ---------- DATE PICKER ----------
elif current_field == "date":
    st.write("📅 **Select Date:**")
    selected_date = st.date_input("Pick a date", min_value=datetime.now().date())
    send_clicked = st.button("Confirm Date")
    if send_clicked:
        user_input = selected_date.strftime("%Y-%m-%d")

# ---------- TIME PICKER ----------
elif current_field == "time":
    st.write("⏰ **Select Time:**")
    selected_time = st.time_input("Pick a time")
    send_clicked = st.button("Confirm Time")
    if send_clicked:
        user_input = selected_time.strftime("%H:%M")

# ---------- NORMAL TEXT INPUT ----------
else:
    user_input = st.text_input("Type your message:")
    send_clicked = st.button("Send")

# ================== MESSAGE HANDLER ==================
if send_clicked and user_input:

    st.session_state.messages.append({"role": "user", "content": str(user_input)})
    st.session_state.conversation_memory.add_message("user", str(user_input))

    response = None
    user_lower = str(user_input).lower()

    # ================== BOOKING FLOW CONTINUE ==================
    if st.session_state.chat_logic.is_booking_in_progress():

        missing = st.session_state.chat_logic.get_missing_fields()

        # Collecting fields
        if missing:
            field = st.session_state.booking_flow.get_next_required_field()
            ok, msg = st.session_state.booking_flow.process_field_response(field, str(user_input))

            if ok:
                missing = st.session_state.chat_logic.get_missing_fields()
                if missing:
                    next_field = st.session_state.booking_flow.get_next_required_field()
                    response = "✅ " + msg + "\n\n" + st.session_state.booking_flow.get_field_prompt(next_field)
                else:
                    response = st.session_state.booking_flow.get_confirmation_message()
            else:
                response = "❌ " + msg + "\n\n" + st.session_state.booking_flow.get_field_prompt(field)

        # Waiting for confirmation
        else:
            if user_lower in ["yes", "y", "ok", "confirm", "sure"]:
                db = st.session_state.db_manager
                booking_state = st.session_state.chat_logic.get_booking_state()

                customer = db.add_or_get_customer(
                    booking_state["name"],
                    booking_state["email"],
                    booking_state["phone"]
                )

                booking = db.create_booking(
                    customer_id=customer.customer_id,
                    booking_type=booking_state["booking_type"],
                    date=booking_state["date"],
                    time=booking_state["time"],
                    notes="Booked via Chat"
                )

                success, msg = db.send_email(
                    booking_state["email"],
                    f"Booking Confirmation #{booking.id}",
                    f"""
Hello {booking_state['name']},

Your booking is confirmed.

Booking ID: {booking.id}
Service: {booking_state['booking_type']}
Date: {booking_state['date']}
Time: {booking_state['time']}
"""
                )

                email_status = "📧 Email sent!" if success else f"⚠️ Email failed: {msg}"

                response = f"""
🎉 **BOOKING CONFIRMED!**

Booking ID: #{booking.id}
Service: {booking_state['booking_type']}
Date: {booking_state['date']}
Time: {booking_state['time']}

{email_status}
"""

                st.session_state.chat_logic.reset_booking_context()

            elif user_lower in ["no", "cancel", "stop"]:
                st.session_state.chat_logic.reset_booking_context()
                response = "❌ Booking cancelled. Say **I want to book** to start again."

            else:
                response = st.session_state.booking_flow.get_confirmation_message()

    # ================== START BOOKING ==================
    elif "book" in user_lower or "appointment" in user_lower or "reserve" in user_lower:
        st.session_state.chat_logic.start_booking_flow()
        response = "🎯 Let's start your booking!\n\n" + st.session_state.booking_flow.get_field_prompt("name")

    # ================== RAG ==================
    elif st.session_state.rag_pipeline.get_document_count() > 0:
        response = st.session_state.rag_pipeline.ask(str(user_input))

    # ================== FALLBACK ==================
    else:
        response = "I can help you **book an appointment** or **answer questions from PDFs**."

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.conversation_memory.add_message("assistant", response)

    st.rerun()

# ================== FOOTER ==================
st.markdown("---")
st.caption(f"📚 Bookings in DB: {st.session_state.db_manager.get_booking_count()}")
