import re

FIELDS = ["name", "email", "phone", "booking_type", "date", "time"]

def is_booking_intent(text):
    triggers = ["book", "appointment", "schedule", "doctor", "consultation"]
    return any(word in text.lower() for word in triggers)

def validate(field, value):
    value = value.strip()

    if field == "name":
        return len(value) >= 2

    if field == "email":
        return re.match(r"[^@]+@[^@]+\.[^@]+", value)

    if field == "phone":
        return value.isdigit() and len(value) >= 8

    if field == "booking_type":
        return len(value) > 0

    if field == "date":
        return re.match(r"\d{4}-\d{2}-\d{2}", value)

    if field == "time":
        return len(value) > 0   # allows "10am", "3:30pm", "evening", etc.

    return True
