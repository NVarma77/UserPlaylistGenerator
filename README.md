# Playlist Generator

## Overview
The **Playlist Generator** is a Flask-based web application that curates personalized music recommendations based on user input. By analyzing a user's mood and three favorite songs, the app generates a list of ten additional tracks that match the specified vibe and compiles them into a custom playlist. This tool leverages external APIs and intelligent recommendation algorithms to enhance the listening experience.

## Features
- **Personalized Recommendations:** Users enter their vibe description along with three songs, and the app suggests ten additional tracks that align with their musical preferences.
- **Playlist Generation:** The recommended tracks are compiled into a dynamic playlist that users can explore.
- **Music Data Integration:** The application fetches track metadata, genres, and related music from external APIs to ensure accurate recommendations.
- **Flask-Based Backend:** The core of the application is powered by Flask, providing a lightweight yet scalable architecture.
- **Interactive Frontend:** A simple and intuitive interface built with HTML, CSS, and JavaScript allows seamless user interaction.

## Technology Stack
### Backend:
- **Flask (Python):** Handles HTTP requests, processes user input, and communicates with external music recommendation APIs.
- **Flask-Restful:** Supports API request handling and modular development.
- **SQLite (Optional):** If user preferences and playlists need to be stored persistently, SQLite provides a lightweight database solution.
- **Requests Library:** Facilitates external API calls for fetching song data and recommendations.

### Frontend:
- **HTML, CSS, JavaScript:** Provides the structure, styling, and interactivity of the user interface.
- **Bootstrap (Optional):** Used for responsive design and improved UI elements.

### APIs and External Services:
- **Spotify API (or Alternative Music API):** Retrieves song metadata, recommendations, and audio features for more accurate playlist curation.
- **OAuth Authentication (if applicable):** Allows users to connect their accounts to streaming services for direct playlist integration.
- **Machine Learning (Future Enhancement):** A potential addition where recommendation accuracy can be improved using collaborative filtering or deep learning models.

## Installation Guide
### Prerequisites:
Ensure the following dependencies are installed:
- Python 3.x
- Flask (`pip install Flask`)
- Requests (`pip install requests`)
- Other API-specific dependencies (e.g., Spotipy for Spotify API interactions)

### Setup Steps:
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/playlist-generator.git
   cd playlist-generator
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API keys:**
   - Obtain API credentials (e.g., from Spotify Developer Dashboard).
   - Set up authentication tokens in a `.env` file or environment variables.
   ```bash
   export API_KEY='your_api_key_here'
   ```
4. **Run the Flask application:**
   ```bash
   python app.py
   ```
5. **Access the app in your browser:**
   Navigate to `http://127.0.0.1:5000/`.

## Usage Instructions
1. Enter a brief description of your **vibe** (e.g., "chill and relaxing").
2. Provide three **seed songs** that represent the mood you want.
3. Click **"Generate Playlist"** to receive ten additional song suggestions.
4. Explore the curated list and optionally save the playlist.
5. If integrated with a streaming service, export the playlist to Spotify or another platform.

## Future Enhancements
- **AI-Based Recommendation Engine:** Implementing machine learning models for smarter recommendations beyond API-driven results.
- **Streaming Service Integration:** Directly export playlists to Spotify, Apple Music, or YouTube Music.
- **User Profiles & Customization:** Allow users to save preferences, revisit past playlists, and fine-tune recommendation parameters.
- **Enhanced UI/UX:** A more polished frontend with advanced animations and visualizations.

## Notes
- **Spotify API Key** and **OpenAI** API key stored in .env file, the user must obtain independently

---

