from flask import redirect, request, session, jsonify, render_template
from datetime import datetime
import requests 
import urllib.parse
import os
from dotenv import load_dotenv
import API as spotify
from openai import OpenAI
import openai

load_dotenv()

OPENAI_API_KEY = os.getenv("API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def configure_routes(app):

    # 1. Landing page
    @app.route('/')
    def index():
        return render_template('login.html')

    # 2. Initiates Spotify OAuth
    @app.route('/login')
    def login():
        scope = 'user-read-private user-read-email user-top-read playlist-modify-public playlist-modify-private'
        params = {
            'client_id': app.config['CLIENT_ID'],
            'response_type': 'code',
            'scope': scope,
            'redirect_uri': app.config['REDIRECT_URI'],
            'show_dialog': True
        }
        auth_url = f"{spotify.AUTH_URL}?{urllib.parse.urlencode(params)}"
        return redirect(auth_url)

    # 3. Handles Spotify's redirect after authentication
    @app.route('/redirect')
    def callback():
        code = request.args.get('code')
        if not code:
            return 'Error: Authorization failed.'

        try:
            token_info = spotify.get_token(
                app.config['CLIENT_ID'],
                app.config['CLIENT_SECRET'],
                code,
                app.config['REDIRECT_URI']
            )
            if 'access_token' in token_info:
                session['access_token'] = token_info['access_token']
                session['refresh_token'] = token_info.get('refresh_token')
                session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
                return redirect('/main')
            else:
                return 'Error: No access token received.'
        except Exception as e:
            return f"Token exchange failed: {str(e)}"

    # 4. Main route: Renders the form on GET, processes input on POST
    @app.route('/main', methods=['GET', 'POST'])
    def main():
        # Ensure the user is logged in with Spotify
        if 'access_token' not in session:
            return redirect('/login')  # Redirect if no token present

        # Handle POST request when user submits vibe + songs
        if request.method == 'POST':
            data = request.get_json()  # Expecting JSON data from the frontend
            vibe = data.get('vibe')
            first_song = data.get('firstsong')
            second_song = data.get('secsong')
            third_song = data.get('thirdsong')

            # Build the user prompt for ChatGPT
            userinput = (
                f"Vibe: {vibe}. "
                f"Songs: {first_song}, {second_song}, {third_song}."
            )

            try:
                # Call ChatGPT with a system instruction and the user input
                completion = client.chat.completions.create(
                    model="gpt-4o",  # Adjust to the correct model if needed
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a music expert with the best music knowledge in the world and across the internet. "
                                "When given the name of three songs and a word to describe the type of vibe the user feels, "
                                "it is your job to give the names of ten songs that are similar/would match the user's preferences. "
                                "Make sure to only give the list of song names and the artists alongside it and nothing else."
                            )
                        },
                        {
                            "role": "user",
                            "content": userinput
                        }
                    ]
                )

                # Extract ChatGPT's reply (using .message.content to get the text)
                chatgpt_reply = completion.choices[0].message.content
                print("ChatGPT reply received.")

                import re
                pattern = r'\d+\.\s*["“](.+?)["”]\s*-\s*(.+)'
                matches = re.findall(pattern, chatgpt_reply)
                track_uris = []

                access_token = session.get('access_token')
                for song, artist in matches:
                    # Create a query combining song and artist
                    query = f"{song} {artist}"
                    track_uri = spotify.search_track(access_token, query)
                    if track_uri:
                        track_uris.append(track_uri)
                
                print("Found track URIs:")
                print(track_uris)

                # 4B. Create a new playlist in Spotify.
                # First, get the user profile to obtain the user_id.
                user_profile = spotify.get_user_profile(access_token)
                user_id = user_profile.get('id')
                if not user_id:
                    return jsonify({"error": "Unable to get user profile from Spotify."}), 500

                # Create the playlist. You can customize the playlist name as needed.
                playlist_name = f"{vibe.capitalize()} Vibe Playlist"
                playlist = spotify.create_playlist(access_token, user_id, playlist_name=playlist_name)

                if 'id' not in playlist:
                    return jsonify({"error": "Failed to create playlist."}), 500

                playlist_id = playlist['id']
                # 4C. Add the tracks to the created playlist.
                success = spotify.add_tracks_to_playlist(access_token, playlist_id, track_uris)
                if not success:
                    return jsonify({"error": "Failed to add tracks to the playlist."}), 500

                # Return the playlist link and ChatGPT's text as confirmation.
                playlist_link = playlist.get('external_urls', {}).get('spotify', '')
                return jsonify({
                    "message": chatgpt_reply,
                    "playlist_link": playlist_link,
                    "status": "success"
                })

            except Exception as e:
                print(f"Error calling ChatGPT: {e}")
                return jsonify({"error": "Failed to get a response from ChatGPT."}), 500

        # For GET requests, render the input form page (index.html)
        return render_template('index.html')

