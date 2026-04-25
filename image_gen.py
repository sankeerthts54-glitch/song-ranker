# image_gen.py
from PIL import Image, ImageDraw, ImageFont
import io


def generate_ranking_image(songs, album_name, artist_name):
    """
    Creates a shareable ranking image as PNG bytes.
    
    songs       = list of song names in ranked order (best first)
    album_name  = string e.g. "Scorpion"
    artist_name = string e.g. "Drake"
    
    Returns BytesIO object — Streamlit can display and download this directly.
    """
    # Canvas dimensions
    W = 800  # width in pixels
    # Height depends on number of songs — 80px header + 52px per song + 60px footer
    H = max(600, 80 + len(songs) * 52 + 60)
    
    # Create blank image with dark background
    # "#0d1117" is GitHub's dark background color — looks clean
    img = Image.new("RGB", (W, H), color="#0d1117")
    draw = ImageDraw.Draw(img)
    
    # Load fonts — try system fonts first, fall back to default
    # On Windows, Arial is always available
    try:
        font_title  = ImageFont.truetype("arial.ttf", 28)
        font_sub    = ImageFont.truetype("arial.ttf", 18)
        font_song   = ImageFont.truetype("arial.ttf", 20)
        font_num    = ImageFont.truetype("arial.ttf", 16)
        font_footer = ImageFont.truetype("arial.ttf", 13)
    except:
        # Fallback if arial.ttf not found
        font_title  = ImageFont.load_default()
        font_sub    = font_title
        font_song   = font_title
        font_num    = font_title
        font_footer = font_title
    
    # ── Header ──────────────────────────────────────
    # Artist name (smaller, muted)
    draw.text((40, 24), artist_name.upper(),
              font=font_sub, fill="#666666")
    # Album name (larger, white)
    draw.text((40, 50), album_name,
              font=font_title, fill="#ffffff")
    
    # Divider line under header
    draw.line([(40, 96), (W - 40, 96)],
              fill="#222222", width=1)
    
    # ── Songs ────────────────────────────────────────
    # Medal colors for top 3
    medal_colors = {
        0: "#FFD700",  # gold
        1: "#C0C0C0",  # silver
        2: "#CD7F32",  # bronze
    }
    
    for i, song in enumerate(songs):
        y = 110 + i * 52  # vertical position for this row
        
        # Color for the rank indicator
        circle_color = medal_colors.get(i, "#2a2a2a")
        text_color   = "#000000" if i < 3 else "#888888"
        
        # Draw rank circle
        # draw.ellipse takes (x0, y0, x1, y1) — top-left and bottom-right corners
        draw.ellipse(
            [(40, y + 2), (66, y + 28)],
            fill=circle_color
        )
        # Rank number inside circle
        rank_text = str(i + 1)
        # Center the number — single digits need more x padding
        rx = 47 if i < 9 else 43
        draw.text((rx, y + 5), rank_text,
                  font=font_num, fill=text_color)
        
        # Song name
        # Truncate if too long (> 45 chars would overflow the canvas)
        display_name = song if len(song) <= 45 else song[:42] + "..."
        draw.text((80, y + 4), display_name,
                  font=font_song, fill="#ffffff")
        
        # Subtle separator between songs
        draw.line(
            [(80, y + 46), (W - 40, y + 46)],
            fill="#1a1a1a", width=1
        )
    
    # ── Footer ───────────────────────────────────────
    draw.text(
        (40, H - 28),
        "ranked with song-ranker · github.com/sankeerthts54-glitch/song-ranker",
        font=font_footer,
        fill="#333333"
    )
    
    # ── Convert to bytes ─────────────────────────────
    # Streamlit's st.image() and st.download_button() both accept BytesIO
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)  # rewind to start — important, otherwise read returns empty
    return buf


def add_album_art(img_bytes, image_url):
    """
    Optional enhancement — downloads album art from Spotify
    and adds it to the top-right corner of the ranking image.
    
    Only works when Spotify API is available (image_url is not None).
    """
    if not image_url:
        return img_bytes
    
    try:
        import requests
        from io import BytesIO
        
        # Download the album art image from Spotify's CDN
        response = requests.get(image_url, timeout=5)
        album_art = Image.open(BytesIO(response.content))
        
        # Open our ranking image
        ranking_img = Image.open(img_bytes)
        W, H = ranking_img.size
        
        # Resize album art to 120x120
        album_art = album_art.resize((120, 120))
        
        # Paste into top-right corner with 20px margin
        ranking_img.paste(album_art, (W - 140, 16))
        
        # Convert back to bytes
        buf = BytesIO()
        ranking_img.save(buf, format="PNG")
        buf.seek(0)
        return buf
        
    except Exception as e:
        print(f"Could not add album art: {e}")
        return img_bytes  # return original if art fails