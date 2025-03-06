import requests
from flask import session
from datetime import datetime

AUTH_URL = 'https://accounts.spotify.com/authorize'
API_BASE_URL = 'https://api.spotify.com/v1/'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

def get_token(client_id, client_secret, code, redirect_uri):
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(TOKEN_URL, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get token: {response.text}")
    
def get_spotify_headers(access_token):
    return {'Authorization': f'Bearer {access_token}'}

def create_playlist(access_token, user_id, playlist_name='new-playlist'):
    url = f"{API_BASE_URL}users/{user_id}/playlists"
    data = {'name': playlist_name, 'public': True}
    response = requests.post(url, headers=get_spotify_headers(access_token), json=data)
    return response.json()

def add_tracks_to_playlist(access_token, playlist_id, track_uris):
    url = f"{API_BASE_URL}playlists/{playlist_id}/tracks"
    data = {'uris': track_uris}
    response = requests.post(url, headers=get_spotify_headers(access_token), json=data)
    success = response.status_code == 201
    return success


def get_user_profile(access_token):
    url = f"{API_BASE_URL}me"
    response = requests.get(url, headers=get_spotify_headers(access_token))
    return response.json()

def search_track(access_token, query):
    """
    Searches Spotify for a track matching the query and returns the track's URI.
    """
    url = f"https://api.spotify.com/v1/search"
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'q': query,
        'type': 'track',
        'limit': 1  # Get only the top match
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    try:
        track_uri = data['tracks']['items'][0]['uri']
        return track_uri
    except (KeyError, IndexError):
        return None