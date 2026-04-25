import streamlit as st
from sorter import (init_sort, get_current_pair,
                    record_choice, get_progress, _prepare_next_merge)
from spotify import get_songs, get_top_tracks
from image_gen import generate_ranking_image, add_album_art

st.set_page_config(
    page_title="Song Ranker",
    page_icon="🎵",
    layout="centered"
)

# ── Custom CSS: Modern Minimalist / Cyberpunk Edge ────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

.stApp {
    background-image: url('https://t4.ftcdn.net/jpg/02/75/28/95/360_F_275289557_YptaQZDnGnDkcgm8b792ItXOqvvkTQAr.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background: rgba(8, 8, 12, 0.85);
    z-index: 0;
    pointer-events: none;
}
html, body, [class*="css"], .stMarkdown, .stText, p, span, label {
    font-family: 'Inter', sans-serif !important;
}
.block-container {
    padding-top: 3rem !important;
    max-width: 1100px !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
}
h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: clamp(40px, 7vw, 60px) !important;
    font-weight: 700 !important;
    letter-spacing: -0.04em !important;
    color: #ffffff !important;
    line-height: 1.1 !important;
    margin-bottom: 8px !important;
    text-transform: uppercase;
}
h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    color: #E2E2EB !important;
}
.stCaption, [data-testid="stCaptionContainer"] p, [data-testid="stMarkdownContainer"] p {
    color: #A0A0B0 !important;
    font-size: 16px !important;
    letter-spacing: 0.01em !important;
    font-weight: 400 !important;
}
b, strong { color: #ffffff !important; font-weight: 600 !important; }
.stTextInput input, .stTextArea textarea {
    background-color: rgba(15, 15, 20, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 8px !important;
    color: #05D9E8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 16px !important;
    padding: 14px 16px !important;
    transition: all 0.3s ease !important;
    backdrop-filter: blur(10px) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #FF2A6D !important;
    background-color: rgba(20, 20, 25, 0.9) !important;
    box-shadow: 0 0 15px rgba(255, 42, 109, 0.2) !important;
    outline: none !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: rgba(255,255,255,0.25) !important;
}
.stTextInput label, .stTextArea label, .stRadio label {
    color: rgba(255,255,255,0.5) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    margin-bottom: 6px !important;
}
.stButton > button[kind="primary"] {
    background: rgba(25, 20, 35, 0.6) !important;
    border: 1px solid rgba(184, 41, 234, 0.4) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    padding: 24px 20px !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    backdrop-filter: blur(12px) !important;
    width: 100% !important;
}
.stButton > button[kind="primary"]:hover {
    background: rgba(184, 41, 234, 0.15) !important;
    border-color: #05D9E8 !important;
    transform: translateY(-4px) !important;
    box-shadow: 0 10px 30px rgba(184, 41, 234, 0.4),
                0 0 15px rgba(5, 217, 232, 0.3) inset !important;
    color: #ffffff !important;
}
.stButton > button[kind="primary"]:active { transform: translateY(0) !important; }
.stButton > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    color: rgba(255, 255, 255, 0.4) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 10px 20px !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="secondary"]:hover {
    color: #ffffff !important;
    border-color: rgba(255, 255, 255, 0.5) !important;
    background: rgba(255, 255, 255, 0.05) !important;
}
.stRadio > div {
    background: rgba(15, 15, 20, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 8px !important;
    padding: 12px 18px !important;
    backdrop-filter: blur(10px) !important;
}
.stRadio p { color: #ffffff !important; font-weight: 500 !important; }
.stProgress > div > div {
    background: linear-gradient(90deg, #05D9E8, #B829EA, #FF2A6D) !important;
    border-radius: 99px !important;
}
.stProgress > div {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 99px !important;
    height: 4px !important;
}
hr { border-color: rgba(255,255,255,0.05) !important; margin: 30px 0 !important; }
[data-testid="column"] { padding: 0 10px !important; }
.stSpinner > div { border-top-color: #05D9E8 !important; }
.stAlert {
    background: rgba(255, 42, 109, 0.1) !important;
    border: 1px solid rgba(255, 42, 109, 0.3) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}
.stImage img {
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(184, 41, 234, 0.5); }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── SCREEN 1: Search ──────────────────────────────────────────────────
if "runs" not in st.session_state:

    st.markdown("""
    <div style="margin-bottom: 12px; font-size: 11px; font-weight: 700; letter-spacing: 0.3em;
                text-transform: uppercase; color: #05D9E8;">
        // Pairwise Ranking System
    </div>
    """, unsafe_allow_html=True)

    st.title("Song Ranker")
    st.markdown(
        '<p style="color: #A0A0B0; font-size: 16px; margin-bottom: 2rem;">'
        'Rank any album with the fewest clicks possible · '
        '<span style="color: #05D9E8; font-weight: 600;">(Ensure Artist or Album is on Spotify)</span>'
        '</p>',
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    st.subheader("Target Selection")

    # ── Tip banner ──
    st.markdown("""
    <div style="
        background: rgba(5, 217, 232, 0.06);
        border: 1px solid rgba(5, 217, 232, 0.2);
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 16px;
        font-size: 14px;
        color: #A0A0B0;
        font-family: 'Inter', sans-serif;
    ">
        💡 <strong style="color: #05D9E8;">Tip:</strong>
        Enter only the <strong style="color: #ffffff;">artist name</strong>
        and leave the album field blank to rank their
        <strong style="color: #ffffff;">top 10 most streamed songs</strong> on Spotify.
    </div>
    """, unsafe_allow_html=True)

    st.write("Try: **After Hours** by **The Weeknd**, or **The Slim Shady LP** by **Eminem**")

    from streamlit_searchbox import st_searchbox
    from spotify import _get_sp_client_credentials

    def search_artists(query: str):
        """Called on every keystroke — returns list of artist name suggestions."""
        if not query or len(query) < 2:
            return []
        try:
            sp = _get_sp_client_credentials()
            results = sp.search(q=query, type="artist", limit=6, market="US")
            return [a["name"] for a in results["artists"]["items"]]
        except Exception:
            return []

    def search_albums(query: str):
        """Called on every keystroke — returns album suggestions."""
        if not query or len(query) < 2:
            return []
        try:
            sp = _get_sp_client_credentials()
            # Use artist from session if available for better results
            artist_ctx = st.session_state.get("selected_artist", "")
            q = f"artist:{artist_ctx} album:{query}" if artist_ctx else f"album:{query}"
            results = sp.search(q=q, type="album", limit=8, market="US")
            seen = set()
            albums = []
            for a in results["albums"]["items"]:
                name = a["name"]
                if name not in seen:
                    seen.add(name)
                    albums.append(name)
            return albums
        except Exception:
            return []

    st.markdown("<label style='font-size:12px;font-weight:600;letter-spacing:0.15em;text-transform:uppercase;color:rgba(255,255,255,0.5)'>ARTIST NAME</label>", unsafe_allow_html=True)
    artist = st_searchbox(
        search_artists,
        placeholder="Sleep Token",
        key="artist_searchbox",
        clear_on_submit=False,
        default=None,
    )
    # Store selected artist for album search context
    if artist:
        st.session_state["selected_artist"] = artist
    artist = artist or ""

    st.markdown("<label style='font-size:12px;font-weight:600;letter-spacing:0.15em;text-transform:uppercase;color:rgba(255,255,255,0.5)'>ALBUM NAME (OPTIONAL)</label>", unsafe_allow_html=True)
    album = st_searchbox(
        search_albums,
        placeholder="Even In Arcadia",
        key="album_searchbox",
        clear_on_submit=False,
        default=None,
    )
    album = album or ""

    st.write("")

    mode = st.radio("Mode", ["Album ranking", "Custom songs"], horizontal=True)

    if mode == "Custom songs":
        custom = st.text_area(
            "Enter songs (one per line)",
            placeholder="Song 1\nSong 2\nSong 3",
            height=150
        )

    st.write("")

    if st.button("Initialize Ranking →", type="primary"):

        if mode == "Custom songs":
            songs = [s.strip() for s in custom.split("\n") if s.strip()]
            if len(songs) < 2:
                st.error("Please enter at least 2 songs")
            else:
                st.session_state.album_name = "Custom"
                st.session_state.artist_name = "My ranking"
                st.session_state.image_url = None
                init_sort(songs)
                st.rerun()

        else:
            if not artist:
                st.error("Please enter at least an artist name")

            # ── Artist only → top 10 tracks ──
            elif artist and not album:
                with st.spinner(f"Fetching top tracks for {artist}..."):
                    songs, image_url = get_top_tracks(artist)

                if songs:
                    st.session_state.album_name = f"Top 10 — {artist}"
                    st.session_state.artist_name = artist
                    st.session_state.image_url = image_url
                    init_sort(songs)
                    st.rerun()
                else:
                    st.error(
                        f"Could not find artist '{artist}' on Spotify. "
                        "Check the spelling and try again."
                    )

            # ── Artist + Album → album tracks ──
            else:
                with st.spinner("Fetching audio data..."):
                    songs, image_url = get_songs(artist, album)

                if songs:
                    st.session_state.album_name = album
                    st.session_state.artist_name = artist
                    st.session_state.image_url = image_url
                    init_sort(songs)
                    st.rerun()
                else:
                    st.error(
                        f"Could not find '{album}' by '{artist}'. "
                        "Try: After Hours (The Weeknd) or The Slim Shady LP (Eminem)"
                    )


# ── SCREEN 2: Compare ─────────────────────────────────────────────────
elif not st.session_state.get("sorted", False):

    done, total = get_progress()
    progress = min(done / max(total, 1), 1.0)

    st.caption(
        f"COMPUTING: {done} OF ~{total}  //  "
        f"{st.session_state.album_name.upper()} BY {st.session_state.artist_name.upper()}"
    )
    st.progress(progress)
    st.divider()

    pair = get_current_pair()

    if pair:
        song_a, song_b = pair
        st.subheader("Which track is superior?")
        st.write("")
        st.write("")

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"🎵  {song_a}", use_container_width=True, key="btn_a", type="primary"):
                record_choice(song_a)
                st.rerun()
        with col2:
            if st.button(f"🎵  {song_b}", use_container_width=True, key="btn_b", type="primary"):
                record_choice(song_b)
                st.rerun()
    else:
        _prepare_next_merge()
        st.rerun()

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Abort & Start Over", use_container_width=True, type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ── SCREEN 3: Results ─────────────────────────────────────────────────
else:
    result    = st.session_state.result
    album     = st.session_state.album_name
    artist    = st.session_state.artist_name
    image_url = st.session_state.get("image_url")
    done, _   = get_progress()

    st.markdown("""
    <div style="margin-bottom: 8px; font-size: 11px; font-weight: 700; letter-spacing: 0.3em;
                text-transform: uppercase; color: #B829EA;">
        // Ranking Complete
    </div>
    """, unsafe_allow_html=True)

    st.subheader(f"Final Output: {album}")
    st.caption(f"Processed in {done} comparisons · {len(result)} tracks ranked")
    st.divider()

    medals = {0: "🥇", 1: "🥈", 2: "🥉"}
    for i, song in enumerate(result):
        icon = medals.get(i, f"**{i+1}.**")
        st.write(f"{icon}  {song}")

    st.divider()

    with st.spinner("Rendering final image matrix..."):
        img_bytes = generate_ranking_image(result, album, artist)
        if image_url:
            img_bytes = add_album_art(img_bytes, image_url)

    st.image(img_bytes)
    st.write("")

    st.download_button(
        label="Download Output Graphic ↓",
        data=img_bytes,
        file_name=f"{album.replace(' ', '-')}-ranking.png",
        mime="image/png",
        type="primary",
        use_container_width=True
    )

    st.write("")

    if st.button("Rank Another Item", type="secondary", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
