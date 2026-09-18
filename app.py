import os

from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from openai import OpenAI

load_dotenv()
# =========================================================
# CONFIG
# =========================================================

DATA_FILE = "Pakistan_Flight_Routes_Dataset.csv"
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # set OPENAI_MODEL to override
MAX_TABLE_ROWS = 50
MAX_CONTEXT_ROWS = 30

EXAMPLE_QUESTIONS = [
    "What flights operate from Islamabad to Jeddah?",
    "Which airlines fly to Karachi?",
    "Show me the shortest route to Dubai.",
]

PREFERRED_COLUMNS = [
    "AIRLINE",
    "FLIGHT NO",
    "ROUTE",
    "DEPARTURE CITY",
    "DEPARTURE IATA CODE",
    "ARRIVAL CITY",
    "ARRIVAL IATA CODE",
    "FLIGHT DURATION",
]


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Pakistan Flight Routes Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

        :root {
            --accent: #1e3a8a;
            --accent-light: #3b82f6;
            --ink: #0f172a;
            --muted: #64748b;
            --border: #e2e8f0;
            --surface: #ffffff;
            --bg: #f7f9fc;
            --success-bg: #e0e7ff;
            --success-ink: #3730a3;
        }

        /* ---------- GLOBAL ---------- */

        .stApp {
            background: var(--bg);
        }

        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background: var(--surface);
            border-right: 1px solid var(--border);
        }

        /* ---------- HERO ---------- */

        .hero {
            background: linear-gradient(135deg, #0f172a, var(--accent));
            padding: 42px 45px;
            border-radius: 24px;
            color: white;
            margin-bottom: 28px;
            box-shadow: 0 12px 35px rgba(15, 23, 42, 0.15);
        }

        .hero-title {
            font-size: 36px;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .hero-subtitle {
            font-size: 16px;
            color: #dbeafe;
            margin-bottom: 22px;
            max-width: 620px;
        }

        .status {
            display: inline-block;
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 8px 15px;
            border-radius: 30px;
            font-size: 13px;
        }

        .status-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #4ade80;
            margin-right: 6px;
        }

        /* ---------- SECTION HEADERS ---------- */

        .section-title {
            font-size: 21px;
            font-weight: 750;
            color: var(--ink);
            margin-bottom: 6px;
        }

        .section-subtitle {
            color: var(--muted);
            font-size: 14px;
            margin-bottom: 14px;
        }

        /* ---------- RESULT HEADER ---------- */

        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 26px;
            margin-bottom: 12px;
        }

        .result-count {
            background: var(--success-bg);
            color: var(--success-ink);
            padding: 6px 13px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }

        /* ---------- STAT CARDS ---------- */

        .info-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
        }

        .info-number {
            font-size: 26px;
            font-weight: 800;
            color: var(--ink);
        }

        .info-label {
            color: var(--muted);
            font-size: 13px;
            margin-top: 2px;
        }

        /* ---------- FOOTER ---------- */

        .footer {
            text-align: center;
            color: #94a3b8;
            font-size: 13px;
            margin-top: 45px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
        }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# API CLIENT
# =========================================================

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error(
        "OPENAI_API_KEY was not found. Set it as an environment variable "
        "before running the app (e.g. `export OPENAI_API_KEY=sk-...`)."
    )
    st.stop()

client = OpenAI(api_key=api_key)


# =========================================================
# LOAD DATASET (cached so it's read from disk only once)
# =========================================================

@st.cache_data(show_spinner=False)
def load_dataset(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    data.columns = data.columns.str.strip()
    return data


try:
    df = load_dataset(DATA_FILE)
except FileNotFoundError:
    st.error(
        f"`{DATA_FILE}` was not found. Make sure the CSV file is in the "
        "same folder as app.py."
    )
    st.stop()

display_columns = [c for c in PREFERRED_COLUMNS if c in df.columns]


# =========================================================
# SEARCH FUNCTION
# =========================================================

def search_flights(
    query: str,
    airline: str = "All airlines",
    city: str = "All cities",
) -> pd.DataFrame:
    """Filter the dataset by free-text query plus optional dropdown filters."""
    result = df.copy()

    if airline != "All airlines" and "AIRLINE" in result.columns:
        result = result[result["AIRLINE"] == airline]

    if city != "All cities":
        city_cols = [c for c in ["DEPARTURE CITY", "ARRIVAL CITY"] if c in result.columns]
        if city_cols:
            mask = pd.Series(False, index=result.index)
            for col in city_cols:
                mask |= result[col] == city
            result = result[mask]

    query = (query or "").strip().lower()
    if query:
        mask = result.astype(str).apply(
            lambda column: column.str.lower().str.contains(query, na=False)
        ).any(axis=1)
        result = result[mask]

    return result.copy()


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# =========================================================
# SIDEBAR — FILTERS
# =========================================================

with st.sidebar:
    st.markdown("### 🔧 Filters")

    airline_options = ["All airlines"] + (
        sorted(df["AIRLINE"].dropna().unique().tolist()) if "AIRLINE" in df.columns else []
    )

    city_pool = set()
    for col in ["DEPARTURE CITY", "ARRIVAL CITY"]:
        if col in df.columns:
            city_pool.update(df[col].dropna().unique().tolist())
    city_options = ["All cities"] + sorted(city_pool)

    selected_airline = st.selectbox("Airline", airline_options)
    selected_city = st.selectbox("City (departure or arrival)", city_options)

    st.markdown("---")
    st.markdown(f"**Dataset:** {len(df):,} total flights")

    if st.button("🗑️ Clear chat history", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# =========================================================
# HERO HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">✈️ Pakistan Flight Routes Assistant</div>
        <div class="hero-subtitle">
            Search airline routes by city, airline or airport code, and ask
            follow-up questions using an AI-powered flight information assistant.
        </div>
        <div class="status"><span class="status-dot"></span>AI Assistant Online</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SEARCH SECTION
# =========================================================

st.markdown('<div class="section-title">🔍 Find a Flight</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Combine the sidebar filters with free-text search '
    'by airline, route, city or airport code.</div>',
    unsafe_allow_html=True,
)

search_query = st.text_input(
    "Search",
    placeholder="Try: Islamabad, ISB, Jeddah, PIA, ISB-JED...",
    label_visibility="collapsed",
)

filtered_df = search_flights(search_query, selected_airline, selected_city)
has_active_filters = bool(search_query) or selected_airline != "All airlines" or selected_city != "All cities"

st.markdown(
    f"""
    <div class="result-header">
        <div class="section-title" style="margin-bottom:0;">Available Routes</div>
        <div class="result-count">{len(filtered_df):,} flights found</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not has_active_filters:
    st.info("Use the search box above or the sidebar filters to view matching flights.")
elif len(filtered_df) == 0:
    st.warning("No matching flights found. Try another airline, city, route or airport code.")
else:
    st.dataframe(
        filtered_df[display_columns].head(MAX_TABLE_ROWS),
        use_container_width=True,
        hide_index=True,
        height=300,
    )
    if len(filtered_df) > MAX_TABLE_ROWS:
        st.caption(f"Showing the first {MAX_TABLE_ROWS} of {len(filtered_df):,} matching flights.")

    col1, col2, col3 = st.columns(3)
    unique_airlines = filtered_df["AIRLINE"].nunique() if "AIRLINE" in filtered_df.columns else 0
    unique_routes = filtered_df["ROUTE"].nunique() if "ROUTE" in filtered_df.columns else 0

    for col, number, label in (
        (col1, len(filtered_df), "Matching Flights"),
        (col2, unique_airlines, "Airlines"),
        (col3, unique_routes, "Routes"),
    ):
        with col:
            st.markdown(
                f"""
                <div class="info-card">
                    <div class="info-number">{number:,}</div>
                    <div class="info-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# =========================================================
# CHAT SECTION
# =========================================================

st.markdown('<div class="section-title">💬 Ask the Flight Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Ask questions about airlines, routes, cities and '
    'flights — the assistant remembers this conversation.</div>',
    unsafe_allow_html=True,
)

# Quick-start suggestion chips (only before the first message)
if not st.session_state.messages:
    chip_cols = st.columns(len(EXAMPLE_QUESTIONS))
    for col, question in zip(chip_cols, EXAMPLE_QUESTIONS):
        with col:
            if st.button(question, use_container_width=True, key=f"chip_{question}"):
                st.session_state.pending_question = question

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

typed_question = st.chat_input("Example: What flights operate from Islamabad to Jeddah?")
user_question = st.session_state.pending_question or typed_question
st.session_state.pending_question = None

if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    # Ground the answer in whatever the search/filters currently show,
    # falling back to a fresh search on the question text itself.
    relevant_data = filtered_df if len(filtered_df) > 0 else search_flights(user_question)
    relevant_data = relevant_data.head(MAX_CONTEXT_ROWS)
    flight_context = (
        relevant_data.to_csv(index=False) if len(relevant_data) > 0 else "No matching flight data found."
    )

    conversation = [
        {
            "role": "system",
            "content": (
                "You are Pakistan Flight Routes Assistant.\n\n"
                "You answer questions using only the provided flight dataset.\n\n"
                "Rules:\n"
                "- Use only the provided dataset.\n"
                "- Never invent flight numbers, airlines, routes or airports.\n"
                "- If information is not available, say so clearly.\n"
                "- Keep answers professional and concise.\n"
                "- Use previous conversation context for follow-up questions.\n"
                "- Mention relevant airline, flight number, route, departure city, "
                "arrival city and duration when available."
            ),
        }
    ]
    conversation.extend(st.session_state.messages[:-1])
    conversation.append({"role": "system", "content": f"Relevant flight dataset:\n\n{flight_context}"})
    conversation.append({"role": "user", "content": user_question})

    with st.chat_message("assistant"):
        with st.spinner("Finding flight information..."):
            try:
                response = client.responses.create(model=MODEL_NAME, input=conversation)
                answer = response.output_text
            except Exception as e:
                answer = f"Unable to connect to AI: {e}"
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Pakistan Flight Routes Assistant · Python · Pandas · OpenAI API · Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
