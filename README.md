# Career Path Predictor

This repository contains the **Final Career Path Predictor**, a Django-based web application designed to help users predict and explore potential career paths based on their preferences and skills.

## Features
- **User Authentication**: Login and signup functionality.
- **Career Prediction**: Predicts career paths based on user input.
- **Roadmaps**: Provides detailed roadmaps for selected careers.
- **Comparison Tool**: Compare different career options.
- **History**: Tracks user predictions and history.

## Project Structure
```
final Career Path Predictor/
├── core/                # Django project settings and configurations
├── ml_pipeline/         # Machine learning pipeline for career prediction
├── predictor/           # Django app for career prediction logic
├── static/              # Static files (CSS, JS, images)
├── templates/           # HTML templates for the frontend
├── db.sqlite3           # SQLite database (for development)
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
└── seed_db.py           # Script to seed the database
```

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd final Career Path Predictor
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run database migrations:
   ```bash
   python manage.py migrate
   ```
6. Seed the database (optional):
   ```bash
   python seed_db.py
   ```
7. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage
- Access the application at `http://127.0.0.1:8000/`.
- Use the navigation bar to explore features like career prediction, roadmaps, and history.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
