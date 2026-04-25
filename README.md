# 🎵 Song Ranker

An interactive web app that ranks songs from any album using **merge sort** — guaranteeing the minimum number of comparisons possible for accurate rankings.

![Song Ranker Demo](assets/preview.png)

## 🚀 Live Demo

Try it here: [HuggingFace Space](https://huggingface.co/spaces/Vader26/song-ranker)

## ✨ Features

- **Smart ranking algorithm**: Uses merge sort to rank n songs in only ~n×log₂(n) comparisons
  - 10 songs = ~33 clicks (vs 45 naive comparisons)
  - 12 songs = ~43 clicks (vs 66 naive comparisons)
  - 20 songs = ~86 clicks (vs 190 naive comparisons)

- **Three ranking modes**:
  - 🎵 **Album mode**: Enter artist + album name to fetch all tracks
  - 🔥 **Top tracks mode**: Enter just artist name to rank their top 10 most streamed songs
  - ✍️ **Custom mode**: Add your own songs line by line

- **Real-time Spotify search**: Dropdown suggestions appear as you type (2-3 characters)

- **Shareable results**: Download a polished ranking image with album art

- **Polished UI**: Dark theme with smooth animations and gradient accents

## 🛠️ Tech Stack

- **Python 3.12** — Core language
- **Streamlit** — Web UI framework
- **Spotipy** — Spotify API wrapper (OAuth Client Credentials flow)
- **Pillow** — Image generation for shareable rankings
- **Merge Sort** — O(n log n) optimal comparison-based sorting

## 📊 How It Works

### The Algorithm

Merge sort is mathematically proven to be the most efficient comparison-based sorting algorithm. Instead of comparing every song to every other song (which takes n² comparisons), merge sort:

1. Splits the song list in half recursively
2. Shows you two songs at a time and records your preference
3. Merges sorted sublists back together

The result: **complete ranking in minimum clicks possible**.

## 🎨 Example Usage

### Rank an album
1. Type artist name (e.g., "Sleep Token")
2. Dropdown suggestions appear — select your artist
3. Type album name (e.g., "Take Me Back to Eden")
4. Click "Initialize Ranking →"
5. Click your preferred song each round
6. Download your ranking image

### Rank top tracks
1. Type artist name only
2. Leave album field blank
3. App fetches their top 10 most streamed songs from Spotify
4. Start ranking

### Custom songs
1. Select "Custom Songs" mode
2. Type song names (one per line)
3. Start ranking

## 🧠 Why This Project?

Most song ranking tools use naive pairwise comparisons (every song vs every other song), requiring n×(n-1)/2 clicks. For a 20-song album that's **190 clicks**.

This app uses merge sort which is **mathematically optimal** for comparison-based sorting — guaranteed to finish in at most n×log₂(n) comparisons. Same 20 songs: **only 86 clicks**.

The difference gets bigger as the list grows — and merge sort is proven to be the best you can do without additional information about the songs.

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
