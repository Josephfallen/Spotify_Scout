import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Initialize Spotipy with user authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='620f7795d05444cf925bf5a9f3489d6b',
                                               client_secret='5387cebf436a42be9b2544b140c68289',
                                               redirect_uri='http://localhost:8080/callback',
                                               scope='playlist-modify-public'))

# Function to create a new playlist
def create_playlist(user_id, playlist_name, playlist_description):
    playlist = sp.user_playlist_create(user=user_id,
                                       name=playlist_name,
                                       public=False,
                                       description=playlist_description)
    return playlist['id']

# Function to add tracks to a playlist
def add_tracks_to_playlist(user_id, playlist_id, track_uris):
    sp.user_playlist_add_tracks(user=user_id,
                                playlist_id=playlist_id,
                                tracks=track_uris)

# Example usage:
if __name__ == '__main__':
    user_id = 'xbck9jw41x3l40bmlg5q5zvpa'
    playlist_name = 'My New Playlist'
    playlist_description = 'A playlist created using Spotipy!'
    track_uris = [
        'spotify:track:4iV5W9uYEdYUVa79Axb7Rh',  # Example track URI
        'spotify:track:2takcwOaAZWiXQijPHIx7B'   # Example track URI
    ]

    # Create a new playlist
    playlist_id = create_playlist(user_id, playlist_name, playlist_description)
    print(f'Playlist "{playlist_name}" created with ID: {playlist_id}')

    # Add tracks to the playlist
    add_tracks_to_playlist(user_id, playlist_id, track_uris)
    print(f'Tracks added to the playlist "{playlist_name}"')
