import streamlit as st
import sqlite3
import pandas as pd

def admin_panel():
    st.title("Admin Panel")

    # Connect to DB
    conn = sqlite3.connect("bookings.db")
    cursor = conn.cursor()

    # Fetch bookings
    cursor.execute("SELECT * FROM bookings")
    rows = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    if rows:
        df = pd.DataFrame(rows, columns=column_names)
        st.subheader("All Bookings")
        st.dataframe(df, hide_index=True)

    else:
        st.info("No bookings found.")

    # Clear all bookings button
    if st.button("Clear All Bookings"):
        cursor.execute("DELETE FROM bookings")
        conn.commit()
        st.success("All bookings cleared!")
        st.rerun()

    conn.close()
