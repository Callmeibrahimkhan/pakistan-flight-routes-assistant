# ✈️ Pakistan Flight Routes Assistant

**Pakistan Flight Routes Assistant** is an AI-powered flight route search and question-answering application built with **Python, Streamlit, Pandas, and Groq AI**.

The project combines a structured flight-route dataset with an AI assistant so users can search flight routes using traditional filters or ask questions in natural language.

Users can search by departure and arrival cities, filter by airline and city, and ask the AI assistant detailed questions about available routes, airlines, flight numbers, airports, and flight durations.

---

## 🚀 Project Overview

Finding flight-route information across a structured dataset can require users to understand the underlying data structure.

This project provides a simple interface where users can interact with the dataset in two ways:

### 1. Flight Route Search

Users can enter:

* Departure city
* Arrival city
* Airline
* City

The application searches the flight dataset and displays matching flight routes.

### 2. AI Flight Assistant

Users can ask questions using natural language.

For example:

> I want to travel from Islamabad to Jeddah. Which airlines operate this route? Please provide the flight number, destination airport and flight duration.

The AI assistant processes the question, identifies relevant flight records from the dataset, and generates an easy-to-understand response.

---

# 🤖 AI Flight Assistant

The AI component is powered by **Groq API** and uses the flight dataset as the information source.

The assistant is designed to answer questions using the available dataset rather than inventing flight information.

### Example questions

```text
Which flights operate from Islamabad to Jeddah?
```

```text
What airlines operate from Karachi to Dubai?
```

```text
Which airline operates this route and what is the flight duration?
```

```text
Tell me the flight number and arrival airport for flights from Lahore to Jeddah.
```

Users can also write a complete paragraph containing multiple questions.

---

# ⚡ Quick Questions

The application also provides predefined quick-question options for common searches.

Examples include:

* Flights from Islamabad to Jeddah
* Flights from Islamabad to Dubai
* Flights from Karachi to Dubai
* Flights from Lahore to Jeddah
* Flights from Islamabad to Doha
* Flights from Karachi to Riyadh
* Flights from Lahore to Dubai
* International flight operators

This provides a faster way to interact with the AI assistant without manually writing a question.

---

# 🔎 Flight Route Search

The application includes a dedicated route-search interface.

Users can enter:

**From**

```text
Islamabad
```

**To**

```text
Jeddah
```

The application searches the dataset and displays the matching records.

Each flight card provides important information such as:

* Airline name
* Airline IATA code
* Flight number
* Departure city
* Departure IATA code
* Arrival city
* Arrival IATA code
* Flight duration
* Flight type

---

# ✈️ Airline Information

The application displays the airline's full name together with its IATA code.

Example:

```text
PK
Pakistan International Airlines
```

```text
EK
Emirates
```

```text
QR
Qatar Airways
```

```text
SV
Saudia
```

This makes the flight cards easier to understand and more useful for users.

---

# 📊 Dataset

The project uses a structured Pakistan flight-route dataset containing **597 flight records**.

The dataset contains information about airlines, flight numbers, routes, airports, cities, countries, IATA codes, and flight duration.

### Dataset Columns

| Column              | Description                 |
| ------------------- | --------------------------- |
| SERIAL NO           | Unique serial number        |
| AIRLINE             | Airline name                |
| AIRLINE IATA CODE   | Airline's IATA code         |
| FLIGHT NO           | Flight number               |
| FLIGHT TYPE         | Type of flight              |
| ROUTE               | Flight route                |
| DEPARTURE COUNTRY   | Departure country           |
| DEPARTURE CITY      | Departure city              |
| DEPARTURE AIRPORT   | Departure airport           |
| DEPARTURE IATA CODE | Departure airport IATA code |
| ARRIVAL COUNTRY     | Arrival country             |
| ARRIVAL CITY        | Arrival city                |
| ARRIVAL AIRPORT     | Arrival airport             |
| ARRIVAL IATA CODE   | Arrival airport IATA code   |
| FLIGHT DURATION     | Flight duration             |

---

# 🏗️ Application Architecture

The application follows a simple data-driven architecture:

```text
                    User
                      │
                      ▼
             Streamlit Interface
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
   Flight Search             AI Assistant
          │                       │
          ▼                       ▼
      Pandas                  Groq API
          │                       │
          └───────────┬───────────┘
                      │
                      ▼
             Flight Route Dataset
                      │
                      ▼
                Search Results
```

### Workflow

```text
User Question
      ↓
Question / Route Processing
      ↓
Dataset Search
      ↓
Relevant Flight Records
      ↓
Groq AI
      ↓
Natural Language Response
```

---

# 🛠️ Technology Stack

## Programming Language

**Python**

Used for application logic, data processing, searching, and API integration.

## Data Processing

**Pandas**

Used for:

* Loading the CSV dataset
* Cleaning column names
* Filtering records
* Searching flight information
* Preparing relevant records for the AI assistant

## Web Application

**Streamlit**

Used to build the interactive web interface.

## AI

**Groq API**

Used to provide natural-language responses through the AI Flight Assistant.

## Environment Management

**python-dotenv**

Used to load the Groq API key securely from the `.env` file.

## Data Storage

**CSV**

The flight-route dataset is stored as a structured CSV file.

---

# 📁 Project Structure

```text
pakistan-flight-routes-assistant/
│
├── app.py
│
├── Pakistan_Flight_Routes_Dataset.csv
│
├── requirements.txt
│
├── README.md
│
└── .gitignore
```

### `app.py`

Main Streamlit application containing:

* User interface
* Flight search
* Filters
* Airline mapping
* Dataset processing
* Groq AI integration
* AI question handling

### `Pakistan_Flight_Routes_Dataset.csv`

Structured flight-route dataset used by the application.

### `requirements.txt`

Contains the Python dependencies required to run the project.

### `.gitignore`

Prevents sensitive and unnecessary files such as `.env` and Python cache files from being uploaded.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Callmeibrahimkhan/pakistan-flight-routes-assistant.git
```

## 2. Open the Project

```bash
cd pakistan-flight-routes-assistant
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The main dependencies are:

```text
streamlit
pandas
groq
python-dotenv
```

---

# 🔐 API Configuration

The application requires a Groq API key.

Create a file named:

```text
.env
```

inside the project directory.

Add:

```text
GROQ_API_KEY=your_groq_api_key
```

The API key should remain private.

**Never upload `.env` to GitHub.**

The `.gitignore` file should contain:

```text
.env
__pycache__/
*.pyc
```

---

# ▶️ Run the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

The application will open locally in your web browser.

Typical local address:

```text
http://localhost:8501
```

---

# 🔍 Search Examples

### Route Search

```text
From: Islamabad
To: Jeddah
```

The application searches for matching flight records.

### AI Question

```text
Which airlines operate from Islamabad to Jeddah?
```

### Detailed Question

```text
I want to travel from Islamabad to Jeddah.
Please tell me which airlines operate this route,
their flight numbers, arrival airports and flight duration.
```

The assistant uses the available dataset records to construct the response.

---

# 🎯 Project Objectives

The main objectives of this project are:

* Build an interactive flight-route search application
* Work with structured aviation data
* Practice Python data processing
* Use Pandas for dataset filtering and searching
* Integrate an external AI API
* Build a natural-language question interface
* Combine traditional data search with AI
* Create a practical portfolio project
* Practice building data-driven applications

---

# 💡 Key Learning Outcomes

Through this project, the following practical skills were developed:

### Python

* Functions
* Conditional logic
* Regular expressions
* String processing
* Environment variables
* API integration

### Data Processing

* CSV data loading
* Data cleaning
* Column normalization
* Filtering
* Searching
* Data transformation

### AI Integration

* Groq API integration
* Prompt design
* Dataset-based context
* Natural-language question handling
* AI response generation

### Streamlit

* Interactive forms
* Text areas
* Buttons
* Select boxes
* Sidebar filters
* Columns
* Containers
* Dynamic results

### Software Development

* Project organization
* Dependency management
* Environment variables
* `.gitignore`
* GitHub version control

---

# 🧠 Data + AI Approach

A key concept demonstrated by this project is combining **structured data search with generative AI**.

Instead of allowing the AI assistant to freely generate flight information, the application first searches the available dataset for relevant records.

The relevant records are then provided to the AI model as context.

Conceptually:

```text
User Question
      ↓
Search Flight Dataset
      ↓
Relevant Records
      ↓
Groq AI
      ↓
Natural Language Answer
```

This approach helps keep the assistant focused on the information available in the project's dataset.

---

# 📌 Project Scope

This project is primarily a **portfolio and learning project** demonstrating:

* Data handling
* Search functionality
* AI integration
* Streamlit development
* Dataset-driven question answering

It is not intended to replace official airline booking systems or provide real-time flight availability.

Flight schedules, availability, prices, delays, and booking information should be verified through official airline or airport sources.

---

# 🔒 Security

The project follows basic API-key security practices.

Sensitive credentials are stored in:

```text
.env
```

and excluded from GitHub using:

```text
.gitignore
```

The API key should never be hard-coded inside `app.py` or committed to a public repository.

---

# 🚀 Future Improvements

Possible future improvements include:

* Real-time flight information
* Flight availability integration
* Airport lookup
* Advanced route matching
* Multi-city route search
* More detailed airline information
* Database integration
* ETL pipeline for automated dataset updates
* Cloud deployment
* Advanced AI retrieval architecture
* Vector database / RAG implementation
* Flight schedule updates

---

# 👨‍💻 Author

## Ibrahim Khan

Computer Science Student | Data Engineering Enthusiast

Interested in:

* Data Engineering
* Big Data
* ETL Pipelines
* Data Analytics
* Python
* SQL
* AI-powered Data Applications

### GitHub

https://github.com/Callmeibrahimkhan

### Project Repository

https://github.com/Callmeibrahimkhan/pakistan-flight-routes-assistant

---

# ⭐ Project

If you find this project useful for learning or reference, you can star the repository on GitHub.

**Built with Python, Streamlit, Pandas and Groq AI.**
