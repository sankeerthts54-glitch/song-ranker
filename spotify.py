# spotify.py
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

MOCK_ALBUMS = {
    "scorpion": {
        "artist": "Drake", "album": "Scorpion", "image_url": None,
        "songs": [
            "Nonstop", "Elevate", "Emotionless", "God's Plan",
            "I'm Upset", "8 Out of 10", "Talk Up", "Is There More",
            "Peak", "Summer Games", "Jaded", "Nice for What",
            "Finesse", "In My Feelings", "Blue Tint",
            "After Dark", "Final Fantasy", "March 14"
        ]
    },
    "midnights": {
        "artist": "Taylor Swift", "album": "Midnights", "image_url": None,
        "songs": [
            "Lavender Haze", "Marjorie", "Anti-Hero",
            "Snow on the Beach", "Midnight Rain", "Question...?",
            "Vigilante Shit", "Bejeweled", "Labyrinth",
            "Karma", "Sweet Nothing", "Mastermind"
        ]
    },
    "igor": {
        "artist": "Tyler, the Creator", "album": "IGOR", "image_url": None,
        "songs": [
            "IGOR'S THEME", "EARFQUAKE", "I THINK",
            "EXACTLY WHAT YOU RUN FROM YOU END UP CHASING",
            "RUNNING OUT OF TIME", "NEW MAGIC WAND",
            "A BOY IS A GUN*", "PUPPET", "WHAT'S GOOD",
            "GONE, GONE / THANK YOU", "I DON'T LOVE YOU ANYMORE",
            "ARE WE STILL FRIENDS?"
        ]
    },
    "after_hours": {
        "artist": "The Weeknd", "album": "After Hours", "image_url": None,
        "songs": [
            "Alone Again", "Too Late", "Hardest To Love", "Scared To Live",
            "Snowchild", "Escape From LA", "Heartless", "Faith",
            "Blinding Lights", "In Your Eyes", "Save Your Tears",
            "Repeat After Me", "After Hours"
        ]
    },
    "slim_shady_lp": {
        "artist": "Eminem", "album": "The Slim Shady LP", "image_url": None,
        "songs": [
            "My Name Is", "Guilty Conscience", "Brain Damage", "Paul",
            "If I Had", "97 Bonnie & Clyde", "Bitch", "Role Model",
            "Lounge", "My Fault", "Ken Kaniff", "Cum On Everybody",
            "Rock Bottom", "Just Don't Give a F***", "Soap",
            "As the World Turns", "I'm Shady", "Bad Meets Evil", "Still Don't Give a F***"
        ]
    },
}

MOCK_TOP_TRACKS = {
    "drake": ["God's Plan", "One Dance", "Hotline Bling", "In My Feelings", "Nice for What", "Started From the Bottom", "Hold On, We're Going Home", "Nonstop", "HYFR", "Take Care"],
    "the weeknd": ["Blinding Lights", "Save Your Tears", "Starboy", "Can't Feel My Face", "The Hills", "Often", "Earned It", "In Your Eyes", "Die For You", "Call Out My Name"],
    "eminem": ["Lose Yourself", "Without Me", "The Real Slim Shady", "Rap God", "Love The Way You Lie", "Not Afraid", "Stan", "My Name Is", "Mockingbird", "Slim Shady"],
    "taylor swift": ["Anti-Hero", "Shake It Off", "Blank Space", "Love Story", "Bad Blood", "Style", "You Belong With Me", "Wildest Dreams", "cardigan", "Cruel Summer"],
    "tyler, the creator": ["EARFQUAKE", "See You Again", "Bye Bye", "NEW MAGIC WAND", "Smuckers", "Who Dat Boy", "IFHY", "Yonkers", "I THINK", "A BOY IS A GUN*"],
    "kendrick lamar": ["HUMBLE.", "DNA.", "All The Stars", "Swimming Pools (Drank)", "Alright", "Money Trees", "m.A.A.d city", "Bitch, Don't Kill My Vibe", "King Kunta", "Not Like Us"],
    "kanye west": ["Stronger", "Gold Digger", "Heartless", "All Falls Down", "POWER", "Runaway", "FML", "Flashing Lights", "Can't Tell Me Nothing", "Jesus Walks"],
    "billie eilish": ["bad guy", "Happier Than Ever", "ocean eyes", "Therefore I Am", "lovely", "when the party's over", "No Time To Die", "everything i wanted", "bury a friend", "Bellyache"],
    "ariana grande": ["7 rings", "thank u, next", "positions", "God is a woman", "Into You", "Problem", "No Tears Left To Cry", "Break Free", "Side to Side", "One Last Time"],
    "post malone": ["Circles", "Sunflower", "rockstar", "Congratulations", "Better Now", "White Iverson", "I Fall Apart", "Go Flex", "Psycho", "Saint-Tropez"],
    "sleep token": ["The Summoning", "The Chokehold", "The Love You Want", "The Riddle", "Thread the Needle", "Are You Really Okay?", "Give", "Sugar", "Chokehold", "Aqua Regia"],
    "sabrina carpenter": ["Espresso", "Please Please Please", "Taste", "Feather", "because i liked a boy", "Read Your Mind", "Nonsense", "Fast Times", "Skinny Dipping", "Sue Me"],
    "bad bunny": ["Tití Me Preguntó", "Me Porto Bonito", "Ojitos Lindos", "Callaíta", "Dakiti", "Yonaguni", "Después de la Playa", "Moscow Mule", "El Apagón", "La Corriente"],
    "bring me the horizon": ["Can You Feel My Heart", "Throne", "Shadow Moses", "Drown", "Follow You", "Mantra", "TEARDROPS", "Obey", "Ludens", "Die4u"],
    "erra": ["Pale Iris", "Breach", "Nigh", "Remnant", "Snowblood", "Expanse", "Drift", "Scorpion", "Disarray", "White Noise"],
    "periphery": ["Icarus Lives!", "The Walk", "Stranger Things", "Blood Eagle", "Scarlet", "Omega", "Make Total Destroy", "Lune", "Satellites", "Reptile"],
    "architects": ["Animals", "Doomsday", "Gone With the Wind", "Hereafter", "Phantom Fear", "Hollow Crown", "Black Lungs", "Memento Mori", "Seeing Red", "All Our Gods Have Abandoned Us"],
    "linkin park": ["In the End", "Numb", "Crawling", "What I've Done", "Somewhere I Belong", "Faint", "Breaking the Habit", "New Divide", "Burn It Down", "Waiting for the End"],
    "coldplay": ["Yellow", "The Scientist", "Clocks", "Fix You", "Viva la Vida", "A Sky Full of Stars", "Speed of Sound", "In My Place", "Paradise", "Magic"],
}


def _get_sp_client_credentials():
    """Returns a Spotipy client using Client Credentials (no user login)."""
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    ))


def _get_sp_oauth():
    """
    Returns a Spotipy client using OAuth (user login).
    Handles the Streamlit OAuth callback flow via query params.
    Returns None if the user hasn't authenticated yet.
    """
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth

    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8501")

    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-read-private",
        cache_path=".spotify_token_cache",
        open_browser=False,
    )

    # Check if we already have a valid cached token
    token_info = auth_manager.get_cached_token()
    if token_info and not auth_manager.is_token_expired(token_info):
        return spotipy.Spotify(auth=token_info["access_token"])

    # Check if Spotify just redirected back with an auth code
    query_params = st.query_params
    code = query_params.get("code")

    if code:
        # Exchange the code for a token
        token_info = auth_manager.get_access_token(code, as_dict=True)
        # Clear the code from the URL
        st.query_params.clear()
        if token_info:
            return spotipy.Spotify(auth=token_info["access_token"])

    # No token yet — show login button and stop
    auth_url = auth_manager.get_authorize_url()
    st.warning("🔐 Spotify login required to fetch top tracks for any artist.")
    st.markdown(
        f'<a href="{auth_url}" target="_self">'
        f'<button style="background: linear-gradient(135deg,#1DB954,#1aa34a); border: none; '
        f'border-radius: 10px; color: white; font-size: 16px; font-weight: 700; '
        f'padding: 14px 28px; cursor: pointer; width: 100%;">'
        f'🎵 Log in with Spotify</button></a>',
        unsafe_allow_html=True
    )
    return None


def get_songs(artist: str, album: str):
    """Fetch songs for a specific album. Returns (songs, image_url)."""
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        return _get_mock_songs(artist, album)

    try:
        sp = _get_sp_client_credentials()
        results = sp.search(q=f"album:{album} artist:{artist}", type="album", limit=1)

        if not results["albums"]["items"]:
            return None, None

        album_data = results["albums"]["items"][0]
        tracks = sp.album_tracks(album_data["id"])
        songs = [track["name"] for track in tracks["items"]]
        image_url = album_data["images"][0]["url"] if album_data["images"] else None

        return songs, image_url

    except Exception as e:
        print(f"Spotify API error: {e}. Falling back to mock.")
        return _get_mock_songs(artist, album)


def get_top_tracks(artist: str):
    """
    Fetch top 10 most popular songs for an artist.
    Uses Client Credentials only — no OAuth/login needed.
    Searches tracks by artist and sorts by Spotify popularity score.
    """
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        return _get_mock_top_tracks(artist)

    try:
        sp = _get_sp_client_credentials()

        # Step 1: Find exact artist
        artist_results = sp.search(q=f"artist:{artist}", type="artist", limit=1, market="US")
        if not artist_results["artists"]["items"]:
            return None, None

        artist_data = artist_results["artists"]["items"][0]
        artist_id = artist_data["id"]
        exact_name = artist_data["name"]
        image_url = artist_data["images"][0]["url"] if artist_data["images"] else None

        # Step 2: Run multiple searches to gather enough tracks
        seen = set()
        filtered = []

        for offset in [0, 10, 20, 30]:
            try:
                track_results = sp.search(
                    q=f"artist:{exact_name}",
                    type="track",
                    limit=10,
                    offset=offset,
                    market="US"
                )
                tracks = track_results["tracks"]["items"]
                for track in tracks:
                    # Include track if artist appears anywhere in artist list
                    artist_ids = [a["id"] for a in track["artists"]]
                    if artist_id in artist_ids:
                        name = track["name"]
                        if name not in seen:
                            seen.add(name)
                            filtered.append((track.get("popularity", 0), name))
            except Exception:
                break

            if len(filtered) >= 20:
                break

        filtered.sort(key=lambda x: x[0], reverse=True)
        songs = [name for _, name in filtered[:10]]

        if not songs:
            return _get_mock_top_tracks(artist)

        return songs, image_url

    except Exception as e:
        print(f"Spotify API error: {e}. Falling back to mock.")
        return _get_mock_top_tracks(artist)


def _get_mock_songs(artist, album):
    key = album.lower().replace(" ", "").replace("'", "")
    if key in MOCK_ALBUMS:
        data = MOCK_ALBUMS[key]
        return data["songs"], data["image_url"]
    return [f"Track {i+1}" for i in range(10)], None


def _get_mock_top_tracks(artist):
    key = artist.lower().strip()
    if key in MOCK_TOP_TRACKS:
        return MOCK_TOP_TRACKS[key], None
    return [f"Top Track {i+1}" for i in range(10)], None
