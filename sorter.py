# sorter.py
import streamlit as st

def init_sort(songs):
    """
    Called once when user starts ranking.
    Sets up the entire sort state in session_state.
    
    songs = list of song name strings e.g. ["Nonstop", "God's Plan", ...]
    """
    st.session_state.original = songs.copy()
    
    # We represent the sort as a list of "runs"
    # A run is a sorted sublist
    # We start with runs of size 1 — each song is its own sorted list
    # e.g. [["Nonstop"], ["God's Plan"], ["HYFR"], ["Forever"]]
    st.session_state.runs = [[s] for s in songs]
    
    st.session_state.sorted = False
    st.session_state.result = []
    st.session_state.comparisons = 0
    
    # Set up the first merge
    _prepare_next_merge()


def _prepare_next_merge():
    """
    Looks at current runs and sets up the next merge.
    Takes the first two runs and prepares to merge them.
    If only one run remains, sorting is complete.
    """
    runs = st.session_state.runs
    
    if len(runs) == 1:
        # Only one sorted list left — we're done
        st.session_state.sorted = True
        st.session_state.result = runs[0]
        return
    
    # Take the first two runs to merge
    # e.g. runs = [["God's Plan", "Nonstop"], ["Forever", "HYFR"], ["Jaded"]]
    # left = ["God's Plan", "Nonstop"]
    # right = ["Forever", "HYFR"]
    # remaining_runs = [["Jaded"]]
    st.session_state.left = runs[0]
    st.session_state.right = runs[1]
    st.session_state.remaining_runs = runs[2:]
    st.session_state.merged = []
    st.session_state.li = 0  # pointer — our current position in left list
    st.session_state.ri = 0  # pointer — our current position in right list


def get_current_pair():
    """
    Returns the two songs currently needing comparison.
    Returns None if no comparison needed (one side exhausted).
    
    The li and ri pointers track where we are in each list.
    left[li] is the current candidate from the left list.
    right[ri] is the current candidate from the right list.
    """
    if st.session_state.get("sorted", False):
        return None
    
    left = st.session_state.left
    right = st.session_state.right
    li = st.session_state.li
    ri = st.session_state.ri
    
    # If we've gone past the end of either list, no comparison needed
    if li >= len(left) or ri >= len(right):
        return None
    
    return (left[li], right[ri])


def record_choice(winner):
    """
    Called when user clicks a song button.
    winner = the song name string they clicked.
    
    Adds winner to the merged list, advances the winner's pointer,
    and checks if the current merge is complete.
    """
    left = st.session_state.left
    right = st.session_state.right
    li = st.session_state.li
    ri = st.session_state.ri
    
    # Add the winner to our growing merged list
    st.session_state.merged.append(winner)
    
    # Advance the pointer for whichever side won
    if winner == left[li]:
        st.session_state.li += 1  # move forward in left list
    else:
        st.session_state.ri += 1  # move forward in right list
    
    st.session_state.comparisons += 1
    
    # Re-read the updated pointers
    li = st.session_state.li
    ri = st.session_state.ri
    
    # Check if one side is now fully exhausted
    if li >= len(left) or ri >= len(right):
        # Append all remaining elements from the non-exhausted side
        # These don't need comparison — they're already in order
        st.session_state.merged += left[li:]
        st.session_state.merged += right[ri:]
        
        # This merge is complete — add result to remaining runs
        # e.g. remaining_runs was [["Jaded"]]
        # now runs = [["God's Plan","Forever","Nonstop","HYFR"], ["Jaded"]]
        new_runs = [st.session_state.merged] + st.session_state.remaining_runs
        st.session_state.runs = new_runs
        
        # Set up the next merge
        _prepare_next_merge()


def get_progress():
    """
    Returns (comparisons_done, estimated_total) for the progress bar.
    estimated_total = n * log2(n) which is the theoretical maximum.
    """
    import math
    n = len(st.session_state.original)
    estimated = int(n * math.log2(n)) if n > 1 else 1
    done = st.session_state.comparisons
    return done, estimated