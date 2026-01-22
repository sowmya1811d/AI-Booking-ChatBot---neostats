import sqlite3
from datetime import datetime

DB_NAME = "bookings.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        booking_type TEXT,
        date TEXT,
        time TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_booking(name, email, phone, booking_type, date, time):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO bookings (name, email, phone, booking_type, date, time)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, email, phone, booking_type, date, time))
    conn.commit()
    bid = cursor.lastrowid
    conn.close()
    return bid

def init_extended_schema():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings_v2 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        booking_type TEXT,
        date TEXT,
        time TEXT,
        status TEXT,
        created_at TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    )
    """)

    conn.commit()
    conn.close()

def save_booking_v2(details):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO customers(name,email,phone) VALUES(?,?,?)",
        (details["name"], details["email"], details["phone"])
    )
    cid = cursor.lastrowid

    cursor.execute("""
    INSERT INTO bookings_v2(customer_id, booking_type, date, time, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        cid,
        details["booking_type"],
        details["date"],
        details["time"],
        "confirmed",
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()
