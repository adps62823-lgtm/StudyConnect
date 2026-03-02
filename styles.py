"""
Minimalist, switchable light/dark styles for StudyConnect.

This stylesheet uses CSS variables and prefers-color-scheme. It also
exposes `.light-theme` and `.dark-theme` classes for explicit overrides
if you want to toggle themes in the app UI.
"""

def get_styles() -> str:
    return """
    <style>
    /* Minimal font and layout reset */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    :root {
        --font-sans: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
        --radius: 8px;
        --gap: 10px;
        /* Light theme defaults */
        --bg: #f7f7f8;
        --surface: #ffffff;
        --muted: #6b7280;
        --text: #0f1724;
        --border: #e6e6ea;
        --accent: #f5c02a; /* yellow */
        --shadow: 0 1px 6px rgba(16,24,40,0.04);
    }

    /* Dark theme via system preference */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg: #000000; /* truly black background */
            --surface: #0b0b0b;
            --muted: #9aa4b2;
            --text: #e6eef6;
            --border: #0b0b0b;
            --accent: #f5c02a; /* yellow */
            --shadow: 0 2px 8px rgba(0,0,0,0.6);
        }
    }

    /* Explicit theme classes (useful if you implement a toggle) */
    .light-theme {
        --bg: #f7f7f8;
        --surface: #ffffff;
        --muted: #6b7280;
        --text: #0f1724;
        --border: #e6e6ea;
        --accent: #f5c02a;
        --shadow: 0 1px 6px rgba(16,24,40,0.04);
    }
    .dark-theme {
        --bg: #000000;
        --surface: #0b0b0b;
        --muted: #9aa4b2;
        --text: #e6eef6;
        --border: #0b0b0b;
        --accent: #f5c02a;
        --shadow: 0 2px 8px rgba(0,0,0,0.6);
    }

    html, body, .stApp {
        background: var(--bg) !important;
        color: var(--text) !important;
        font-family: var(--font-sans);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--surface) !important;
        border-right: 1px solid var(--border) !important;
        padding: 16px 12px !important;
    }

    /* Cards / Panels */
    .user-card, .post-card, .help-card, .mentor-card, .stat-card, .feature-card, .auth-container {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        box-shadow: var(--shadow) !important;
        padding: 14px !important;
        color: var(--text) !important;
    }

    /* Headings and section headers */
    .section-header h2, .auth-title {
        margin: 0 0 6px 0 !important;
        color: var(--text) !important;
        font-weight: 600 !important;
    }

    /* Muted text */
    .help-meta, .post-meta, .user-card-footer, .empty-state, .stMarkdown p {
        color: var(--muted) !important;
    }

    /* Avatar sizes */
    .user-avatar, .mentor-avatar, .post-avatar {
        width: 44px !important;
        height: 44px !important;
        border-radius: 8px !important;
        object-fit: cover !important;
        border: 1px solid var(--border) !important;
    }

    /* Buttons: yellow filled on hover/active, minimal by default */
    .stButton>button {
        background: transparent !important;
        color: var(--text) !important;
        border: 1px solid rgba(0,0,0,0.06) !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .stButton>button:hover {
        background: rgba(245,192,42,0.08) !important;
        border-color: rgba(245,192,42,0.18) !important;
    }
    .stButton>button[aria-pressed="true"], .stButton>button:active {
        background: var(--accent) !important;
        color: #000 !important;
        border-color: var(--accent) !important;
    }

    /* Inputs */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div,
    .stNumberInput>div>div>input {
        background: transparent !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        padding: 8px !important;
        color: var(--text) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 8px !important; }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: 1px solid var(--border) !important;
        color: var(--muted) !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }
    .stTabs [aria-selected="true"] { color: var(--text) !important; border-color: rgba(37,99,235,0.16) !important; }

    /* Compact user list */
    .user-compact-card { display:flex; gap:12px; align-items:center; padding:8px !important; }

    /* Empty states */
    .empty-state { text-align:center; padding:28px !important; color: var(--muted) !important; }

    /* Small helpers */
    .tag { background: transparent !important; border: 1px solid var(--border) !important; color: var(--muted) !important; padding: 4px 8px !important; border-radius: 6px !important; }

    /* Make scrollbars unobtrusive */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-thumb { background: rgba(63,71,86,0.24); border-radius: 8px; }

    </style>
    """