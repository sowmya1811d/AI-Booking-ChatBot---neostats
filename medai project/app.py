import streamlit as st
from groq import Groq
from pypdf import PdfReader
import re
import os
from db import init_db, save_booking, init_extended_schema
from booking import is_booking_intent, FIELDS, validate
from admin import admin_panel
from emailer import send_email

# ---------------- Setup ----------------
init_db()
init_extended_schema()

st.set_page_config(page_title="DocAI", page_icon="🩺")

# ---- UI Styling ----
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #1f1b3a, #0e1117 60%);
}
.stButton>button {
    background-color: #6c63ff;
    color: white;
    border-radius: 10px;
}
[data-testid="stChatInput"] textarea {
    background-color: #1c1f26;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🩺 DocAI – Health Assistant")

api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.write("Groq key loaded:", bool(api_key))



# ---------------- Session State ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_chunks" not in st.session_state:
    st.session_state.pdf_chunks = []

if "booking" not in st.session_state:
    st.session_state.booking = {}

if "booking_active" not in st.session_state:
    st.session_state.booking_active = False

if "current_field" not in st.session_state:
    st.session_state.current_field = None

if "awaiting_confirmation" not in st.session_state:
    st.session_state.awaiting_confirmation = False


# ---------------- Prompts ----------------
field_prompts = {
    "name": "Please enter your name",
    "email": "Please enter your email",
    "phone": "Please enter your phone number",
    "booking_type": """Please choose booking type:
1. General Checkup
2. Dermatology
3. Cardiology
4. Dental
5. Pediatrics
6. Orthopedics
7. Gynecology
8. Other

You can type the name or the number.""",
    "date": "Please enter date (YYYY-MM-DD)",
    "time": "Please enter time"
}

booking_map = {
    "1": "General Checkup",
    "2": "Dermatology",
    "3": "Cardiology",
    "4": "Dental",
    "5": "Pediatrics",
    "6": "Orthopedics",
    "7": "Gynecology",
    "8": "Other"
}

# ---------------- Helpers ----------------
def chunk_text(text, chunk_size=500):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks, current = [], ""

    for s in sentences:
        if len(current) + len(s) < chunk_size:
            current += " " + s
        else:
            chunks.append(current.strip())
            current = s
    if current:
        chunks.append(current.strip())
    return chunks


def retrieve_chunks(query, chunks, top_k=3):
    query_words = set(query.lower().split())
    scored = []

    for chunk in chunks:
        score = sum(word in chunk.lower() for word in query_words)
        scored.append((score, chunk))

    ranked = sorted(scored, key=lambda x: x[0], reverse=True)
    return [c for s, c in ranked[:top_k] if s > 0]


def ask_groq(question, context):
    prompt = f"""
You are a helpful assistant.
Answer the question using ONLY the information below.
If the answer is not present, say "I couldn't find that in the document."

Context:
{context}

Question: {question}
Answer:
"""
    response = client.chat.completions.create(
       model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=400
    )
    return response.choices[0].message.content.strip()


# ---------------- Sidebar PDF Upload ----------------
st.sidebar.header("Upload PDF (optional)")
uploaded = st.sidebar.file_uploader("Upload PDF", type="pdf")

if uploaded:
    reader = PdfReader(uploaded)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    if full_text.strip():
        st.session_state.pdf_chunks = chunk_text(full_text)
        st.sidebar.success("PDF processed successfully")
    else:
        st.sidebar.error("Could not extract text from this PDF")


# ---------------- Tabs ----------------
tab1, tab2 = st.tabs(["Chat", "Admin"])
user_input = st.chat_input("Book appointment or upload a PDF to ask questions...")


# ---------------- Chat Tab ----------------
with tab1:
    for msg in st.session_state.messages[-25:]:
        st.chat_message(msg["role"]).write(msg["content"])

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        # -------- Confirmation --------
        if st.session_state.awaiting_confirmation:
            if user_input.lower() in ["yes", "y"]:
                details = st.session_state.booking

                try:
                    bid = save_booking(**details)
                    try:
                        send_email(
                            st.secrets["EMAIL"],
                            st.secrets["PASSWORD"],
                            details["email"],
                            f"""Booking confirmed!

Name: {details['name']}
Date: {details['date']}
Time: {details['time']}
Type: {details['booking_type']}
Booking ID: {bid}
"""
                        )
                        reply = f"Booking confirmed! Your ID is {bid}. Confirmation email sent."
                    except:
                        reply = f"Booking confirmed! Your ID is {bid}. Email could not be sent."
                except:
                    reply = "Booking failed due to database error."
            else:
                reply = "Booking cancelled."

            st.chat_message("assistant").write(reply)

            st.session_state.booking = {}
            st.session_state.booking_active = False
            st.session_state.current_field = None
            st.session_state.awaiting_confirmation = False
            st.stop()

        # -------- Booking Flow --------
        if is_booking_intent(user_input) or st.session_state.booking_active:
            st.session_state.booking_active = True

            if st.session_state.current_field is None:
                st.session_state.current_field = FIELDS[0]
                st.chat_message("assistant").write(field_prompts[FIELDS[0]])
                st.stop()

            field = st.session_state.current_field

            if not validate(field, user_input):
                st.chat_message("assistant").write(f"Invalid {field}. Please try again.")
                st.stop()

            # Handle number mapping for booking type
            if field == "booking_type" and user_input in booking_map:
                st.session_state.booking[field] = booking_map[user_input]
            else:
                st.session_state.booking[field] = user_input

            idx = FIELDS.index(field)

            if idx + 1 < len(FIELDS):
                st.session_state.current_field = FIELDS[idx + 1]
                st.chat_message("assistant").write(field_prompts[FIELDS[idx + 1]])
                st.stop()

            details = st.session_state.booking
            reply = f"""
Please confirm your appointment:

Name: {details['name']}
Email: {details['email']}
Phone: {details['phone']}
Type: {details['booking_type']}
Date: {details['date']}
Time: {details['time']}

Reply yes or no.
"""
            st.chat_message("assistant").write(reply)
            st.session_state.awaiting_confirmation = True
            st.stop()

        # -------- PDF Q&A --------
        if st.session_state.pdf_chunks:
            retrieved = retrieve_chunks(user_input, st.session_state.pdf_chunks)
            context = "\n".join(retrieved)

            if context.strip():
                answer = ask_groq(user_input, context)
            else:
                answer = "I couldn't find that in the document."
        else:
            answer = "You can book an appointment or upload a PDF to ask questions about it."

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)


# ---------------- Admin Tab ----------------
with tab2:
    admin_panel()
