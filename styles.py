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
        /* Cooler Instagram-like Light theme */
        --bg: #ffffff; /* page background */
        --surface: #fafafa; /* card / surfaces */
        --muted: #8e8e8e; /* subtle labels */
        --text: #262626; /* primary text */
        --border: #dbdbdb; /* light subtle border */
        --accent: #0095f6; /* Instagram blue */
        --accent-secondary: #e1306c; /* Instagram pink */
        --shadow: 0 1px 6px rgba(0,0,0,0.08);
    }

    /* Dark theme via system preference (Instagram-like dark) */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg: #000000; /* very dark background */
            --surface: #111111; /* panel surfaces */
            --muted: #9aa4b2;
            --text: #ffffff;
            --border: #1f1f1f;
            --accent: #0095f6; /* same blue accent */
            --accent-secondary: #e1306c; /* same pink */
            --shadow: 0 2px 8px rgba(0,0,0,0.6);
        }
    }

    /* Explicit theme classes (useful if you implement a toggle) */
    .light-theme {
        --bg: #ffffff;
        --surface: #fafafa;
        --muted: #8e8e8e;
        --text: #262626;
        --border: #dbdbdb;
        --accent: #0095f6;
        --accent-secondary: #e1306c;
        --shadow: 0 1px 6px rgba(0,0,0,0.08);
    }
    .dark-theme {
        --bg: #000000;
        --surface: #111111;
        --muted: #9aa4b2;
        --text: #ffffff;
        --border: #1f1f1f;
        --accent: #0095f6;
        --accent-secondary: #e1306c;
        --shadow: 0 2px 8px rgba(0,0,0,0.6);
    }

    /* gradient text helper using Instagram colors */
    .gradient-text {
        background: linear-gradient(90deg, var(--accent), var(--accent-secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
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
        position: relative; /* for custom toggle placement */
    }

    /* hide Streamlit's default collapse/expand arrow icon but keep the button
       itself for accessibility/toggle logic */
    button[aria-label="Collapse sidebar"],
    button[aria-label="Expand sidebar"] {
        color: transparent !important;
        background: transparent !important;
        width: 24px !important;
        height: 24px !important;
        padding: 0 !important;
        border: none !important;
        position: absolute !important;
        top: 8px !important;
        /* default right offset; adjusted per state below */
        right: 8px !important;
    }
    /* when sidebar is collapsed, shift the expand arrow outside the narrow
       row so no empty strip appears inside the content area */
    button[aria-label="Expand sidebar"] {
        right: -20px !important; /* pulls the arrow to the left of the sidebar */
    }
    /* when sidebar is open the collapse button stays inside */
    button[aria-label="Collapse sidebar"] {
        right: 8px !important;
    }
    /* use pseudo-element to draw our custom arrow/cross */
    button[aria-label="Collapse sidebar"]::before,
    button[aria-label="Expand sidebar"]::before {
        content: '';
        display: inline-block;
        width: 0;
        height: 0;
        border-style: solid;
    }
    /* when sidebar is collapsed show a slim right-pointing arrowhead */
    button[aria-label="Expand sidebar"]::before {
        border-width: 6px 0 6px 10px;
        border-color: transparent transparent transparent var(--text);
    }
    /* when sidebar is open show a cross */
    button[aria-label="Collapse sidebar"]::before {
        content: '\00d7'; /* multiplication sign × */
        font-size: 18px;
        color: var(--text);
    }

    /* expand clickable swipe area by making the button larger than the icon */
    button[aria-label="Collapse sidebar"],
    button[aria-label="Expand sidebar"] {
        cursor: pointer;
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

    /* Buttons: Instagram blue by default; darker on hover/active with animation */
    .stButton>button {
        background: var(--accent) !important;
        color: #fff !important;
        border: none !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: background 0.15s ease;
    }
    .stButton>button:hover {
        background: #007acc !important; /* slightly darker blue */
        cursor: pointer;
    }
    .stButton>button:active {
        background: #005999 !important; /* even darker when clicked */
    }
    /* keep accent color when pressed (aria-pressed) but still animate */
    .stButton>button[aria-pressed="true"] {
        background: #005999 !important;
        color: #fff !important;
    }

    /* customize radio list labels so text is white on dark bg and a small
       colored dot is added via unicode; fallback if needed is handled in
       Python format_func. */
    .stRadio>div>div>label {
        color: var(--text) !important;
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

    /* Like control – we use a checkbox under the hood only because
       Streamlit buttons don't retain state easily.  The actual input is
       hidden and the label is styled to look exactly like a circular
       icon button.  There are no visible checkboxes to the user. */
    .stCheckbox>div>div>input[type="checkbox"] { 
        display: none !important;
    }
    .stCheckbox>div>div>label {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 36px !important;
        height: 36px !important;
        border-radius: 50% !important;
        border: 1px solid var(--border) !important;
        background: transparent !important;
        color: var(--text) !important;
        padding: 0 !important;
        font-size: 18px !important;
        line-height: 1 !important;
        cursor: pointer !important;
        transition: background 0.15s ease, border-color 0.15s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stCheckbox>div>div>input[type="checkbox"]:checked + label {
        background: var(--accent) !important;
        color: #fff !important;
        border-color: var(--accent) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .stCheckbox>div>div>label:hover {
        background: rgba(0,149,246,0.08) !important;
    }
    /* ensure no default checkmark marker appears anywhere */
    .stCheckbox>div>div>label::after { content: none !important; }

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

    /* status display in header */
    .status-display { display: inline-flex; align-items: center; gap: 4px; }
    .status-display strong { font-weight: bold; }

    /* base status emoji styling */
    .status-emoji { display: inline-block; vertical-align: middle; }
    .status-emoji svg { width: 12px; height: 12px; }

    /* studying state pulse animation */
    .status-emoji.studying {
        animation: pulse 4s infinite;
    }
    @keyframes pulse {
        0%   { opacity: 1; }
        8%   { opacity: 0; filter: drop-shadow(0 0 6px rgba(40,167,69,0.5)); }
        16%  { opacity: 1; filter: drop-shadow(0 0 6px rgba(40,167,69,0.5)); }
        20%  { filter: none; }
        100% { opacity: 1; }
    }

    /* highlight for newly added comments */
    .recent-comment {
        padding: 10px !important;
        border-radius: 8px !important;
        animation: comment-highlight 5s forwards;
    }
    @keyframes comment-highlight {
        0% { background: rgba(245,192,42,0.28); }
        100% { background: transparent; }
    }

    /* Empty states */
    .empty-state { text-align:center; padding:28px !important; color: var(--muted) !important; }

    /* Small helpers */
    .tag { background: transparent !important; border: 1px solid var(--border) !important; color: var(--muted) !important; padding: 4px 8px !important; border-radius: 6px !important; }
    /* highlight for new answers */
    .answer-highlight {
        animation: flash 5s ease-out;
        background: var(--accent) !important;
        opacity: 0.15 !important;
    }
    @keyframes flash {
        0% { opacity: 0.5; }
        100% { opacity: 0.15; }
    }

    /* Instagram-like post styles */
    .instagram-post {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        box-shadow: var(--shadow) !important;
        padding: 16px !important;
        margin-bottom: 16px !important;
        color: var(--text) !important;
    }
    .post-header {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
    }
    .post-user-info {
        margin-left: 12px;
    }
    .post-user-info strong {
        display: block;
        color: var(--text);
    }
    .post-meta {
        color: var(--muted);
        font-size: 0.8em;
    }
    .post-content {
        margin-bottom: 12px;
        line-height: 1.4;
    }
    .post-actions {
        margin-bottom: 12px;
    }
    .reaction-buttons {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    .reaction-buttons button {
        background: transparent !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        padding: 4px 8px !important;
        border-radius: 16px !important;
        font-size: 0.9em !important;
        transition: all 0.15s ease;
    }
    .reaction-buttons button:hover {
        background: rgba(0,149,246,0.1) !important;
        border-color: var(--accent) !important;
    }
    .comments-section {
        margin-top: 12px;
    }
    .comment, .reply {
        padding: 8px;
        border-radius: 8px;
        background: rgba(0,0,0,0.05);
        margin-bottom: 8px;
    }
    .reply {
        margin-left: 20px;
        background: rgba(0,0,0,0.03);
    }

    /* StackOverflow-like question styles */
    .question-summary {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 16px !important;
        margin-bottom: 12px !important;
        cursor: pointer;
    }
    .question-title {
        font-size: 1.1em;
        font-weight: 600;
        color: var(--text);
        display: block;
        margin-bottom: 8px;
    }
    .question-info {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: center;
    }
    .answers-count {
        color: var(--accent);
        font-weight: 600;
    }
    .question-detail {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
    }
    .question-meta {
        color: var(--muted);
        margin-bottom: 12px;
    }
    .question-body {
        line-height: 1.6;
        margin-bottom: 20px;
    }
    .answer-card {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 16px !important;
        margin-bottom: 16px !important;
    }
    .answer-header {
        margin-bottom: 8px;
        color: var(--muted);
    }
    .answer-body {
        line-height: 1.6;
        margin-bottom: 12px;
    }
    .answer-actions {
        display: flex;
        gap: 8px;
    }
    .answer-comments {
        margin-top: 12px;
        padding-left: 16px;
        border-left: 2px solid var(--border);
    }
    .answer-comment {
        background: rgba(0,0,0,0.05);
        padding: 8px;
        border-radius: 8px;
        margin-bottom: 8px;
    }

    </style>
    """