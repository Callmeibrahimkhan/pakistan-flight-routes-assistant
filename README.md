# ✈️ Pakistan Flight Routes Assistant

An AI-powered flight information assistant built using **Python, Pandas, OpenAI API, and Streamlit**.

The application allows users to search Pakistan flight routes and ask natural-language questions about airlines, cities, airports, flight numbers, routes, and flight durations.

## 🚀 Features

* 🔍 Search flights by airline, city, route, or airport code
* ✈️ View available flight routes from the dataset
* 🤖 Ask questions using an AI-powered assistant
* 💬 Supports conversational follow-up questions
* 🎯 Airline and city filters
* 📊 Displays matching flight statistics
* 🔐 API key stored locally using environment variables
* ⚡ Streamlit-based interactive interface

## 🛠️ Technology Stack

| Technology    | Purpose                                |
| ------------- | -------------------------------------- |
| Python        | Application development                |
| Pandas        | Dataset processing and filtering       |
| OpenAI API    | Natural-language AI assistant          |
| Streamlit     | Interactive web interface              |
| CSV           | Flight route dataset                   |
| python-dotenv | Secure local environment configuration |

## 📂 Project Structure

```text
pakistan-flight-routes-assistant/
│
├── app.py
├── Pakistan_Flight_Routes_Dataset.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## 📊 Dataset

The project uses a custom Pakistan flight routes dataset containing information such as:

* Airline
* Airline IATA code
* Flight number
* Flight type
* Route
* Departure country
* Departure city
* Departure airport
* Departure IATA code
* Arrival country
* Arrival city
* Arrival airport
* Arrival IATA code
* Flight duration

## 🧠 How the Assistant Works

```text
User Question
      ↓
Streamlit Interface
      ↓
Pandas Dataset Search
      ↓
Relevant Flight Records
      ↓
OpenAI API
      ↓
Natural-Language Answer
```

The assistant is grounded in the provided flight dataset and is instructed not to invent flight information that is not present in the data.

## ▶️ Run Locally

### 1. Clone or download the repository

Download the project files to your computer.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env`

Create a `.env` file in the project folder:

```text
OPENAI_API_KEY=your_api_key_here
```

**Never upload `.env` or your API key to GitHub.**

### 4. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔐 Security

The OpenAI API key is stored in a local `.env` file and excluded from GitHub using `.gitignore`.

The API key should never be placed directly inside `app.py` or uploaded to a public repository.

## 🎯 Project Purpose

This project demonstrates practical skills in:

* Data processing
* Dataset filtering
* Python application development
* API integration
* LLM-based question answering
* Conversational interfaces
* Streamlit application development
* Secure environment-variable handling

## 👨‍💻 Author

**Ibrahim Khan**

GitHub: **Callmeibrahimkhan**

---

⭐ Built as a practical Data Engineering / AI portfolio project.
