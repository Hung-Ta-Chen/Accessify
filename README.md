# Accessify

Accessify is a map-based accessibility application designed to help users find and review places based on their accessibility features. The app allows users to search for locations, apply filters for different place types (e.g., restaurants, parks, parking, hospitals), and view/accessibility-related details and reviews.

## Features

- **Search and Filter**: Search for specific locations and apply filters for different place types.
- **Place Details**: View detailed information about places, including accessibility features.
- **User Reviews**: Read and submit reviews about places.
- **Accessibility Summarization**: AI-generated summarization of place reviews based on accessibility.
- **Ranking System**: Ranking of places based on accessibility features.
- **Chatbot Integration**: Interactive chatbot for querying local services and information.

## Installation

### Prerequisites

- Node.js and npm
- Python 3.x and pip
- PostgreSQL
- MongoDB Atlas account
- Google Maps API key
- OpenAI API key

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/Accessify.git
    cd Accessify
    ```

### Frontend

2. Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

3. Create a `.env` file in the `frontend` directory with the following content:
    ```plaintext
    REACT_APP_MAPS_API_KEY=your-google-maps-api-key
    REACT_APP_BACKEND_URL=http://127.0.0.1:5000
    ```

4. Install dependencies:
    ```bash
    npm install
    ```

5. Start the development server:
    ```bash
    npm start
    ```

### Backend

6. Navigate to the `backend` directory:
    ```bash
    cd ../backend
    ```

7. Create and activate a virtual environment:
    ```bash
    python -m venv accessify_venv
    source accessify_venv/bin/activate   # On Windows use `accessify_venv\Scripts\activate`
    ```

8. Create a `.env` file in the `backend` directory with the following content:
    ```plaintext
    SECRET_KEY=your-secret-key
    SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost/accessify_db
    FLASK_ENV=development
    MONGO_URI=your-mongo-uri
    OPENAI_API_KEY=your-openai-api-key
    MAPS_API_KEY=your-google-maps-api-key
    ```

9. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

10. Set up your PostgreSQL database:
    ```bash
    # Ensure PostgreSQL is running and create the database
    createdb accessify_db
    ```

11. Run the Flask application:
    ```bash
    flask run
    ```

## Usage

1. Open your web browser and go to `http://localhost:3000` to access the frontend.
2. Use the search bar and filters to find accessible places.
3. Click on markers to view detailed information and reviews.
4. Interact with the chatbot for more information.
