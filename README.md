# coordinaid

A platform for NGOs and big support groups to better coordinate their donations and humanitarian aid.

## 🛠 Tech Stack

*   **Frontend:** React (scaffolded with Vite)
*   **Backend:** Python (FastAPI)
*   **AI Integration:** Google Gemini (`google-genai` SDK)
*   **Database:** Persistent JSON file (`needs_database.json`)

---

## 🚀 Getting Started

Follow these instructions to set up the project from absolute scratch on your local machine.

### Prerequisites

Make sure you have the following installed:
*   [Node.js](https://nodejs.org/) (which includes `npm`)
*   [Python 3.8+](https://www.python.org/downloads/)
*   Git

### 1. Clone the Repository
```bash
git clone https://github.com/revaldihansya/coordinaid.git
cd coordinaid
```

### 2. Setup backend
#### Navigate to the backend
```bash
cd backend
```

#### Create activate your virtual environment
```bash
# on Windows
python -m venv venv
.\venv\Scripts\activate

# on Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install dependencies
```bash
python -m pip install requirements.txt
```

#### Setuing up the AI API Key
You should have a .env.example file in your backend
Replace the placeholder your_actual_api_key_here with your own API Key then rename it to .env
.env is included in .gitignore so you don't have to worry about pushing your key to your repository

#### Running the backend
```bash
uvicorn main:app --reload
```

### 3. Setup frontend
#### Open a second, separate terminal window and navigate to the frontend
```bash
cd frontend
```

#### Install dependencies
```bash
npm install
```

#### Running the frontend
```bash
npm run dev
```

### 4. Opening the program
Check your terminal for the local URL and open it in your browser.