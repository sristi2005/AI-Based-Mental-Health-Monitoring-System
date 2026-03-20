# Mental Health Assessment Web Application

A Flask-based web application designed to help users assess, monitor, and understand their mental well-being. The application provides interactive tests to evaluate depression, anxiety, and stress levels through questionnaires, sentiment analysis, and behavioral tracking.

## Features

- **Depression Test**: A 10-question assessment to help identify the severity of depression symptoms (ranging from Minimal to Severe).
- **Anxiety Test**: A 7-question assessment for evaluating anxiety levels.
- **Daily Check-ins**: Users can log their thoughts and feelings. The system calculates a stress score using Rule-Based Sentiment Analysis combined with auto-captured behavioral metrics (session duration, typing delay, click rate).
- **Stress Prediction API**: Uses a pre-trained Machine Learning model (`stress_model.pkl`) to predict stress levels based on user interactions.
- **Weekly Dashboard**: Tracks and visualizes user stress data over the past 7 days, allowing users to monitor trends in their mental health.

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript (Jinja2 templates)
- **Database**: SQLite (`checkins.db`)
- **Machine Learning**: Scikit-Learn (`pickle` for model loading), Pandas
- **Deployment**: Configured with a `Procfile` (likely for Heroku or similar platforms).

## Project Structure

```text
Mental-Health/
│
├── app.py                  # Main Flask application and routes
├── database.py             # SQLite database connections and setup
├── run.py                  # Script to run the application
├── checkins.db             # SQLite database for storing check-in data
│
├── model/                  # Contains pre-trained ML models
│   └── stress_model.pkl    
├── anxiety_model.pkl       # Pre-trained ML model for anxiety prediction
│
├── templates/              # HTML templates (landing, forms, tests, dashboard)
├── static/                 # CSS/JS and static assets
│
└── Procfile                # Deployment configuration
```

## Installation & Setup

1. **Clone or Download the repository**
   Navigate to the project directory in your terminal.
   ```bash
   cd Mental-Health
   ```

2. **Create a Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   ```
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. **Install Dependencies**
   Make sure you have installed the required Python packages (e.g., via `pip install -r requirements.txt` if available, or install manually):
   ```bash
   pip install Flask pandas scikit-learn
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```
   *(Alternatively, you can run `python run.py`)*

5. **Access the Application**
   Open your web browser and navigate to `http://127.0.0.1:5000/`.

## How It Works

- **Tests**: When you submit a test (like the Depression or Anxiety test), the app evaluates your scores against standard medical thresholds.
- **Check-ins**: The app captures both your text input and how you interact with the form. It searches for predefined positive and negative keywords inside your text and maps a combined final score into a metric of "Low", "Moderate", or "High" Stress. This result is then stored in the local SQLite database.
- **Analytics**: The dashboard route (`/weekly-data`) fetches your previous check-ins to present your stress trends as a graph directly on the dashboard page.
