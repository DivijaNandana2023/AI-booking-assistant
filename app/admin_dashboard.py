"""
Admin Dashboard - View and filter bookings
(Meets assignment requirement: view + filter/search bookings)
"""

import streamlit as st
import pandas as pd
from db.database import DatabaseManager
from config import DATABASE_PATH


def run_admin_dashboard():
    st.set_page_config(page_title="Admin Dashboard", layout="wide")

    st.title("📊 Admin Dashboard")
    st.markdown("### Manage and monitor all bookings")

    db = DatabaseManager(DATABASE_PATH)
    all_bookings = db.get_all_bookings()

    if not all_bookings:
        st.info("📭 No bookings found yet.")
        return

    # Build dataframe safely
    rows = []
    for b in all_bookings:
        rows.append({
            "Booking ID": b.id,
            "Name": b.customer.name if b.customer else "",
            "Email": b.customer.email if b.customer else "",
            "Phone": b.customer.phone if b.customer else "",
            "Service": b.booking_type,
            "Date": b.date,
            "Time": b.time,
            "Status": b.status,
        })

    df = pd.DataFrame(rows)

    # ============ FILTERS ============
    st.markdown("## 🔍 Search & Filters")

    col1, col2, col3 = st.columns(3)

    with col1:
        name_filter = st.text_input("Search by Name")

    with col2:
        email_filter = st.text_input("Search by Email")

    with col3:
        date_filter = st.text_input("Search by Date (YYYY-MM-DD)")

    filtered_df = df.copy()

    if name_filter:
        filtered_df = filtered_df[filtered_df["Name"].str.contains(name_filter, case=False, na=False)]

    if email_filter:
        filtered_df = filtered_df[filtered_df["Email"].str.contains(email_filter, case=False, na=False)]

    if date_filter:
        filtered_df = filtered_df[filtered_df["Date"].str.contains(date_filter, case=False, na=False)]

    st.markdown("---")

    st.success(f"Showing {len(filtered_df)} booking(s)")

    # ============ TABLE ============
    st.dataframe(filtered_df, use_container_width=True)

    # ============ EXPORT ============
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        "📥 Download CSV",
        csv,
        "bookings.csv",
        "text/csv",
        use_container_width=True
    )


if __name__ == "__main__":
    run_admin_dashboard()
