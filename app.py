import os
import re
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from groq import Groq


# =========================================================
# CONFIG
# =========================================================

load_dotenv()

DATA_FILE = "Pakistan_Flight_Routes_Dataset.csv"
MODEL_NAME = "openai/gpt-oss-20b"
MAX_CONTEXT_ROWS = 40


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Pakistan Flight Routes Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f4f7fb;
    }

    #MainMenu,
    footer,
    header {
        visibility: hidden;
    }

    [data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e2e8f0;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .airline-code {
        background: #2563eb;
        color: white;
        width: 58px;
        height: 58px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# AIRLINE INFORMATION
# =========================================================

AIRLINE_INFO = {
    "PIA": ("Pakistan International Airlines", "PK"),
    "PAKISTAN INTERNATIONAL AIRLINE": (
        "Pakistan International Airlines", "PK"
    ),
    "PAKISTAN INTERNATIONAL AIRLINES": (
        "Pakistan International Airlines", "PK"
    ),

    "AIRBLUE": ("Airblue", "PA"),
    "AIRSIAL": ("AirSial", "PF"),
    "FLY JINNAH": ("Fly Jinnah", "9P"),

    "EMIRATES": ("Emirates", "EK"),
    "AIR ARABIA": ("Air Arabia", "G9"),
    "ETIHAD": ("Etihad Airways", "EY"),
    "ETIHAD AIRWAYS": ("Etihad Airways", "EY"),
    "FLYDUBAI": ("flydubai", "FZ"),

    "SALAM": ("SalamAir", "OV"),
    "SALAMAIR": ("SalamAir", "OV"),

    "KUWAIT": ("Kuwait Airways", "KU"),
    "KUWAIT AIRWAYS": ("Kuwait Airways", "KU"),

    "JAZEERA": ("Jazeera Airways", "J9"),
    "JAZEERA AIRWAYS": ("Jazeera Airways", "J9"),

    "SAUDIA": ("Saudia", "SV"),
    "FLYNAS": ("flynas", "XY"),
    "FLYADEAL": ("flyadeal", "F3"),
    "RIYADH AIR": ("Riyadh Air", "RX"),

    "QATAR": ("Qatar Airways", "QR"),
    "QATAR AIRWAYS": ("Qatar Airways", "QR"),

    "GULF": ("Gulf Air", "GF"),
    "GULF AIR": ("Gulf Air", "GF"),

    "OMAN": ("Oman Air", "WY"),
    "OMAN AIR": ("Oman Air", "WY"),

    "TURKISH": ("Turkish Airlines", "TK"),
    "TURKISH AIRLINES": ("Turkish Airlines", "TK"),

    "PEGASUS": ("Pegasus Airlines", "PC"),
    "PEGASUS AIRLINES": ("Pegasus Airlines", "PC"),

    "THAI": ("Thai Airways", "TG"),
    "THAI AIRWAYS": ("Thai Airways", "TG"),

    "MALINDO": ("Batik Air Malaysia", "OD"),
    "BATIK AIR MALAYSIA": ("Batik Air Malaysia", "OD"),

    "MAHAN": ("Mahan Air", "W5"),
    "MAHAN AIR": ("Mahan Air", "W5"),

    "KAM AIR": ("Kam Air", "RQ"),
    "KAM": ("Kam Air", "RQ"),

    "ARIANA": ("Ariana Afghan Airlines", "FG"),
    "ARIANA AFGHAN AIRLINES": (
        "Ariana Afghan Airlines", "FG"
    ),

    "CHINA SOUTHERN": (
        "China Southern Airlines", "CZ"
    ),
    "CHINA SOUTHERN AIRLINES": (
        "China Southern Airlines", "CZ"
    ),

    "AIR CHINA": ("Air China", "CA"),

    "UZBEKISTAN": (
        "Uzbekistan Airways", "HY"
    ),
    "UZBEKISTAN AIRWAYS": (
        "Uzbekistan Airways", "HY"
    ),

    "ETHIOPIAN": (
        "Ethiopian Airlines", "ET"
    ),
    "ETHIOPIAN AIRLINES": (
        "Ethiopian Airlines", "ET"
    ),

    "AZERBAIJAN": (
        "Azerbaijan Airlines", "J2"
    ),
    "AZERBAIJAN AIRLINES": (
        "Azerbaijan Airlines", "J2"
    ),

    "SRILANKAN": (
        "SriLankan Airlines", "UL"
    ),
    "SRILANKAN AIRLINES": (
        "SriLankan Airlines", "UL"
    )
}


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    data = pd.read_csv(DATA_FILE)

    data.columns = (
        data.columns
        .astype(str)
        .str.strip()
        .str.upper()
    )

    return data


try:

    df = load_data()

except Exception as e:

    st.error(
        f"Could not load dataset: {e}"
    )

    st.stop()


# =========================================================
# GROQ
# =========================================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:

    st.error(
        "GROQ_API_KEY was not found in your .env file."
    )

    st.stop()


client = Groq(
    api_key=api_key
)


# =========================================================
# AIRLINE DETAILS
# =========================================================

def get_airline_details(row):

    airline = str(
        row.get("AIRLINE", "")
    ).strip()

    key = airline.upper()

    if key in AIRLINE_INFO:

        return AIRLINE_INFO[key]

    dataset_code = str(
        row.get("AIRLINE IATA CODE", "")
    ).strip().upper()


    code_map = {

        "PK": "Pakistan International Airlines",
        "PA": "Airblue",
        "PF": "AirSial",
        "9P": "Fly Jinnah",
        "EK": "Emirates",
        "G9": "Air Arabia",
        "EY": "Etihad Airways",
        "FZ": "flydubai",
        "OV": "SalamAir",
        "KU": "Kuwait Airways",
        "J9": "Jazeera Airways",
        "SV": "Saudia",
        "XY": "flynas",
        "F3": "flyadeal",
        "RX": "Riyadh Air",
        "QR": "Qatar Airways",
        "GF": "Gulf Air",
        "WY": "Oman Air",
        "TK": "Turkish Airlines",
        "PC": "Pegasus Airlines",
        "TG": "Thai Airways",
        "OD": "Batik Air Malaysia",
        "W5": "Mahan Air",
        "RQ": "Kam Air",
        "FG": "Ariana Afghan Airlines",
        "CZ": "China Southern Airlines",
        "CA": "Air China",
        "HY": "Uzbekistan Airways",
        "ET": "Ethiopian Airlines",
        "J2": "Azerbaijan Airlines",
        "UL": "SriLankan Airlines"
    }


    if dataset_code in code_map:

        return (
            code_map[dataset_code],
            dataset_code
        )


    return (
        airline,
        dataset_code if dataset_code else "—"
    )


# =========================================================
# SEARCH
# =========================================================

def clean(text):

    return str(text).strip().lower()


def search_flights(
    query="",
    airline="All Airlines",
    city="All Cities"
):

    result = df.copy()


    # -----------------------------------------------------
    # AIRLINE FILTER
    # -----------------------------------------------------

    if airline != "All Airlines":

        result = result[
            result["AIRLINE"]
            .astype(str)
            .str.strip()
            .str.lower()
            == airline.lower()
        ]


    # -----------------------------------------------------
    # CITY FILTER
    # -----------------------------------------------------

    if city != "All Cities":

        city_value = city.lower()

        departure = (
            result["DEPARTURE CITY"]
            .astype(str)
            .str.lower()
        )

        arrival = (
            result["ARRIVAL CITY"]
            .astype(str)
            .str.lower()
        )

        result = result[
            (departure == city_value)
            |
            (arrival == city_value)
        ]


    query = clean(query)


    if not query:

        return result


    # -----------------------------------------------------
    # FROM / TO SEARCH
    # -----------------------------------------------------

    match = re.search(

        r"(?:from|between)\s+(.+?)\s+"
        r"(?:to|and|->|→)\s+(.+?)"
        r"(?:\?|$|\.|,)",

        query,
        re.IGNORECASE
    )


    if match:

        departure_query = clean(
            match.group(1)
        )

        arrival_query = clean(
            match.group(2)
        )


        departure_col = (
            result["DEPARTURE CITY"]
            .astype(str)
            .str.lower()
        )

        arrival_col = (
            result["ARRIVAL CITY"]
            .astype(str)
            .str.lower()
        )


        exact = result[
            departure_col.eq(
                departure_query
            )
            &
            arrival_col.eq(
                arrival_query
            )
        ]


        if not exact.empty:

            return exact


        partial = result[
            departure_col.str.contains(
                departure_query,
                na=False
            )
            &
            arrival_col.str.contains(
                arrival_query,
                na=False
            )
        ]


        if not partial.empty:

            return partial


        reverse = result[
            departure_col.str.contains(
                arrival_query,
                na=False
            )
            &
            arrival_col.str.contains(
                departure_query,
                na=False
            )
        ]


        if not reverse.empty:

            return reverse


    # -----------------------------------------------------
    # GENERAL SEARCH
    # -----------------------------------------------------

    stop_words = {

        "from",
        "to",
        "flight",
        "flights",
        "operate",
        "operating",
        "which",
        "what",
        "are",
        "is",
        "the",
        "a",
        "an",
        "and",
        "or",
        "of",
        "in",
        "on",
        "for",
        "me",
        "show",
        "list",
        "find",
        "need",
        "please",
        "can",
        "you",
        "tell",
        "about"
    }


    tokens = [

        token

        for token in re.findall(
            r"[a-z]+",
            query
        )

        if token not in stop_words
        and len(token) > 2
    ]


    if tokens:

        search_columns = [

            column

            for column in result.columns

            if any(

                keyword in column

                for keyword in [

                    "AIRLINE",
                    "FLIGHT",
                    "ROUTE",
                    "CITY",
                    "AIRPORT",
                    "IATA",
                    "COUNTRY"
                ]
            )
        ]


        mask = pd.Series(
            True,
            index=result.index
        )


        for token in tokens:

            token_mask = pd.Series(
                False,
                index=result.index
            )


            for column in search_columns:

                token_mask |= (
                    result[column]
                    .astype(str)
                    .str.contains(
                        token,
                        case=False,
                        na=False
                    )
                )


            mask &= token_mask


        return result[mask]


    return result


# =========================================================
# HEADER
# =========================================================

st.title(
    "✈️ Pakistan Flight Routes Assistant"
)

st.caption(
    "Search routes from the official dataset • Powered by AI"
)

st.divider()


# =========================================================
# AI FLIGHT ASSISTANT - TOP
# =========================================================

st.subheader(
    "🤖 AI Flight Assistant"
)

st.caption(
    "Ask a complete question or use a quick question."
)


# =========================================================
# AI TWO-SIDE LAYOUT
# =========================================================

ai_left, ai_right = st.columns(
    [3, 1]
)


# =========================================================
# LEFT: QUESTION BOX
# =========================================================

with ai_left:

    st.markdown(
        "**💬 Ask your question**"
    )

    question = st.text_area(

        "Question",

        placeholder=(
            "Example: I want to travel from Islamabad "
            "to Jeddah. Which airlines operate this "
            "route? Please give me the airline name, "
            "flight number, arrival airport and "
            "flight duration."
        ),

        height=170,

        label_visibility="collapsed"
    )


# =========================================================
# RIGHT: QUICK OPTION
# =========================================================

with ai_right:

    st.markdown(
        "### ⚡ Quick Questions"
    )

    quick_question = st.selectbox(

        "Choose",

        [

            "Select a question",

            "Flights from Islamabad to Jeddah",

            "Flights from Islamabad to Dubai",

            "Flights from Karachi to Dubai",

            "Flights from Lahore to Jeddah",

            "Flights from Islamabad to Doha",

            "Flights from Karachi to Riyadh",

            "Flights from Lahore to Dubai",

            "Which airlines operate international flights?"
        ],

        label_visibility="collapsed"
    )


    st.write("")


    use_quick = st.button(
        "Use This Question",
        use_container_width=True
    )


# =========================================================
# USE QUICK QUESTION
# =========================================================

if use_quick:

    if quick_question != "Select a question":

        st.session_state.ai_question = (
            quick_question
        )


# =========================================================
# ASK AI
# =========================================================

ask_ai = st.button(
    "🤖 Ask AI",
    type="primary"
)


# =========================================================
# AI ANSWER
# =========================================================

if ask_ai:

    if (
        "ai_question" in st.session_state
        and st.session_state.ai_question
    ):

        final_question = (
            st.session_state.ai_question
        )

        del st.session_state.ai_question

    else:

        final_question = question


    if not final_question.strip():

        st.warning(
            "Please write a question or select a quick question."
        )

    else:

        relevant = search_flights(
            final_question
        ).head(
            MAX_CONTEXT_ROWS
        )


        if relevant.empty:

            context = (
                "No matching records were found "
                "in the dataset."
            )

        else:

            context = relevant.to_string(
                index=False
            )


        system_prompt = """

You are Pakistan Flight Routes Assistant.

Answer ONLY using the provided Pakistan flight
routes dataset.

The user may write a complete paragraph with
multiple questions.

Understand the whole question and answer all
parts that can be answered from the dataset.

Never invent:

- airlines
- airline codes
- flight numbers
- airports
- routes
- cities
- flight durations

If information is not available in the dataset,
say:

"That information was not found in the dataset."

Use a professional and easy-to-understand style.

For multiple flights, use bullet points.

"""


        messages = [

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": (
                    "USER QUESTION:\n\n"
                    + final_question
                    + "\n\n"
                    + "RELEVANT DATASET RECORDS:\n\n"
                    + context
                )
            }
        ]


        with st.spinner(
            "🤖 Searching the flight dataset..."
        ):

            try:

                response = (
                    client
                    .chat
                    .completions
                    .create(
                        model=MODEL_NAME,
                        messages=messages,
                        temperature=0.2
                    )
                )


                answer = (
                    response
                    .choices[0]
                    .message
                    .content
                )


                st.success(
                    "AI Response"
                )

                st.markdown(
                    answer
                )


            except Exception as e:

                st.error(
                    f"Unable to get AI response: {e}"
                )


st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header(
        "⚙️ Filters"
    )

    st.caption(
        "Narrow down your flight results"
    )


    airlines = [
        "All Airlines"
    ]


    if "AIRLINE" in df.columns:

        airlines += sorted(

            df["AIRLINE"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )


    selected_airline = st.selectbox(
        "Airline",
        airlines
    )


    city_set = set()


    if "DEPARTURE CITY" in df.columns:

        city_set.update(

            df["DEPARTURE CITY"]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )


    if "ARRIVAL CITY" in df.columns:

        city_set.update(

            df["ARRIVAL CITY"]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )


    cities = [
        "All Cities"
    ] + sorted(city_set)


    selected_city = st.selectbox(
        "City",
        cities
    )


    st.divider()

    st.caption(
        "Dataset information is used internally "
        "for route matching."
    )


# =========================================================
# FLIGHT SEARCH
# =========================================================

st.subheader(
    "🔎 Search Flight Routes"
)

st.caption(
    "Select your departure and arrival cities "
    "to find available routes."
)


col1, col2, col3 = st.columns(
    [2, 2, 1]
)


with col1:

    from_city = st.text_input(
        "From",
        value="Islamabad",
        placeholder="Departure city"
    )


with col2:

    to_city = st.text_input(
        "To",
        value="Toronto",
        placeholder="Arrival city"
    )


with col3:

    st.write("")
    st.write("")

    search_button = st.button(
        "🔎 Search",
        type="primary",
        use_container_width=True
    )


# =========================================================
# SEARCH STATE
# =========================================================

if "last_search" not in st.session_state:

    st.session_state.last_search = (
        "from Islamabad to Toronto"
    )


if search_button:

    st.session_state.last_search = (
        f"from {from_city} to {to_city}"
    )


# =========================================================
# SEARCH RESULTS
# =========================================================

results = search_flights(

    st.session_state.last_search,

    selected_airline,

    selected_city

).head(25)


st.divider()


st.subheader(
    f"✈️ {len(results)} Flight Routes Found"
)


# =========================================================
# AVAILABLE CITY INFORMATION
# =========================================================

if search_button and not results.empty:

    departure_suggestions = sorted(

        results["DEPARTURE CITY"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    arrival_suggestions = sorted(

        results["ARRIVAL CITY"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    st.info(

        "📍 Available cities — "
        f"Departure: {', '.join(departure_suggestions)} | "
        f"Arrival: {', '.join(arrival_suggestions)}"
    )


# =========================================================
# NO RESULTS
# =========================================================

if results.empty:

    st.warning(
        "No matching route found. "
        "Try another city or change the filters."
    )


# =========================================================
# FLIGHT CARDS
# =========================================================

else:

    for _, row in results.iterrows():

        airline_name, airline_code = (
            get_airline_details(row)
        )


        flight_no = str(
            row.get(
                "FLIGHT NO",
                "—"
            )
        ).strip()


        departure_city = str(
            row.get(
                "DEPARTURE CITY",
                "—"
            )
        ).strip()


        departure_iata = str(
            row.get(
                "DEPARTURE IATA CODE",
                "—"
            )
        ).strip().upper()


        arrival_city = str(
            row.get(
                "ARRIVAL CITY",
                "—"
            )
        ).strip()


        arrival_iata = str(
            row.get(
                "ARRIVAL IATA CODE",
                "—"
            )
        ).strip().upper()


        duration = str(
            row.get(
                "FLIGHT DURATION",
                "—"
            )
        ).strip()


        flight_type = str(
            row.get(
                "FLIGHT TYPE",
                "FLIGHT"
            )
        ).strip()


        # =================================================
        # FLIGHT CARD
        # =================================================

        with st.container(
            border=True
        ):

            airline_col, route_col, type_col = (
                st.columns(
                    [2.2, 5, 1.6]
                )
            )


            # ---------------------------------------------
            # AIRLINE
            # ---------------------------------------------

            with airline_col:

                st.markdown(

                    f"""
                    <div class="airline-code">
                        {airline_code}
                    </div>
                    """,

                    unsafe_allow_html=True
                )


                st.markdown(
                    f"**{airline_name}**"
                )


                st.caption(
                    f"Flight {flight_no}"
                )


            # ---------------------------------------------
            # ROUTE
            # ---------------------------------------------

            with route_col:

                left, middle, right = st.columns(
                    [1, 2, 1]
                )


                with left:

                    st.markdown(
                        f"### {departure_iata}"
                    )

                    st.caption(
                        departure_city.upper()
                    )


                with middle:

                    st.markdown(
                        "### ✈️ ─────────"
                    )

                    st.caption(
                        duration.upper()
                    )


                with right:

                    st.markdown(
                        f"### {arrival_iata}"
                    )

                    st.caption(
                        arrival_city.upper()
                    )


            # ---------------------------------------------
            # FLIGHT TYPE
            # ---------------------------------------------

            with type_col:

                st.caption(
                    "FLIGHT TYPE"
                )

                st.info(
                    flight_type.upper()
                )
