title: Song Ranker
emoji: 🎵
colorFrom: purple
colorTo: pink
sdk: streamlit
sdk_version: "1.43.0"
app_file: app.py
pinned: false

# 🎵 Song Ranker

> Rank any Spotify album or artist's top songs using head-to-head comparisons — powered by a **Binary Insertion Sort** algorithm for maximum accuracy with minimum clicks.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Spotify](https://img.shields.io/badge/Spotify_API-1DB954?style=flat&logo=spotify&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## ✨ Features

- 🔍 **Live autocomplete** — search artists and albums as you type, powered by the Spotify API
- 🎯 **Two ranking modes** — rank a full album, or an artist's top 10 most streamed songs
- ✏️ **Custom songs mode** — paste in any list of songs or items to rank
- ⚡ **Binary Insertion Sort** — ~30% fewer clicks than merge sort, 100% accurate results
- 🎨 **Cyberpunk dark UI** — custom CSS with animated buttons and glassmorphism
- 📸 **Shareable image** — auto-generates a downloadable ranking card when you're done

---

## 🧠 How the Algorithm Works

Most ranking apps use **merge sort** — accurate but slow (~33 clicks for 10 songs).

This app uses **Binary Insertion Sort** instead:

1. The first song is placed automatically
2. Each new song is compared against the **midpoint** of the already-ranked list
3. Your answer halves the search space — just like binary search
4. The song is inserted at its exact position, then the next one begins

| Songs | Merge Sort | **Binary Insertion** | Swiss Tournament |
|-------|-----------|----------------------|-----------------|
| 10    | ~33 clicks | **~23 clicks**      | ~15 clicks (inaccurate) |
| 13    | ~46 clicks | **~30 clicks**      | ~19 clicks (inaccurate) |
| 15    | ~58 clicks | **~36 clicks**      | ~22 clicks (inaccurate) |

Result: **100% accurate ranking in ~30% fewer clicks.**

---

## 📁 Project Structure

```
song-ranker/
├── app.py              # Main Streamlit app — all 3 screens
├── sorter.py           # Binary insertion sort algorithm
├── spotify.py          # Spotify API integration + mock fallback data
├── image_gen.py        # Generates the shareable ranking image
├── requirements.txt    # Python dependencies
├── .env                # Your Spotify credentials (never committed)
├── .gitignore          # Excludes .env, venv, cache files
└── .streamlit/
    └── config.toml     # Dark theme configuration
```

---

## 🚀 Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/song-ranker.git
cd song-ranker
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Spotify API credentials

1. Go to [developer.spotify.com](https://developer.spotify.com/dashboard)
2. Click **Create App**
3. Fill in any name and description
4. Add `http://localhost:8501` as a Redirect URI and save
5. Copy your **Client ID** and **Client Secret**

### 5. Create your `.env` file

Create a file called `.env` in the project root:

```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

### 6. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🎮 How to Use

**Album Ranking mode:**
1. Type an artist name → live suggestions appear
2. Type an album name → suggestions filtered to that artist
3. Click **Initialize Ranking**
4. Pick your preferred song in each head-to-head comparison
5. Download your ranking image when done

**Artist Top 10 mode:**
1. Type only the artist name, leave album blank
2. Click **Initialize Ranking**
3. The app fetches their 10 most streamed Spotify songs
4. Rank them head-to-head

**Custom Songs mode:**
1. Switch to Custom Songs tab
2. Paste any list of songs, one per line
3. Rank them

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Streamlit | Web app framework |
| Spotipy | Spotify Web API wrapper |
| Pillow | Ranking image generation |
| python-dotenv | Environment variable management |
| streamlit-searchbox | Live autocomplete search inputs |

---

## 📦 Requirements

```
streamlit
spotipy
python-dotenv
Pillow
streamlit-searchbox
requests
```

Generate your own with:
```bash
pip freeze > requirements.txt
```

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs via Issues
- Suggest features
- Submit pull requests

## 👤 Author

**Sankeerth TS**
- GitHub: [@sankeerthts54-glitch](https://github.com/sankeerthts54-glitch)
- LinkedIn: [sankeerth-ts](https://linkedin.com/in/sankeerth-ts)
- HuggingFace: [@Vader26](https://huggingface.co/Vader26)

---

Built with 🎵 by a CS undergrad in Bangalore exploring algorithms, APIs, and interactive UIs.