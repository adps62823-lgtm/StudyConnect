"""
StudyConnect - Main Application
The LinkedIn for Students
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from data_handler import DataHandler
from auth_handler import AuthHandler
from components import UIComponents
from icons import svg as icon_svg
from styles import get_styles

# import shadcn components (will be available after installing the package)
try:
    from shadcn_ui import Button, Card, Input
except ImportError:
    Button = None
    Card = None
    Input = None

# Initialize
st.set_page_config(
    page_title="StudyConnect",
    page_icon="SC",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply styles
st.markdown(get_styles(), unsafe_allow_html=True)

# floating theme toggle button (appears at top-right corner of viewport)
def render_theme_toggle():
    # logic mirrors sidebar toggle code but placed absolutely
    current = st.session_state.get("theme_choice", "System")
    is_dark = current == "Dark"
    # use the shared icon helper so the button stays consistent with rest of UI
    icon_html = icon_svg('moon', 22) if is_dark else icon_svg('sun', 22)
    next_theme = 'Light' if is_dark else 'Dark'
    template = '''<div style="position:fixed; top:8px; right:8px; z-index:1000;">
        <button id="theme-btn" style="background:transparent;border:none;cursor:pointer;padding:6px;border-radius:8px">__ICON__</button>
        <script>
        const btn = document.getElementById('theme-btn');
        btn.onclick = () => {
            const next = "__NEXT__";
            const search = new URLSearchParams(window.location.search);
            search.set('theme', next);
            window.location.search = search.toString();
        }
        </script>
    </div>'''
    html = template.replace('__ICON__', icon_html).replace('__NEXT__', next_theme)
    components.html(html, height=40)


# call it immediately so icon is always visible
render_theme_toggle()

if "theme_choice" not in st.session_state:
    st.session_state.theme_choice = "System"

with st.sidebar:
    # Theme can be set via query param so the HTML toggle below can change it.
    # query param access may not exist on older Streamlit versions
    if hasattr(st, "experimental_get_query_params"):
        params = st.experimental_get_query_params()
    else:
        params = {}
    if "theme" in params:
        t = params.get("theme", [st.session_state.theme_choice])[0]
        if t in ("Light", "Dark", "System"):
            st.session_state.theme_choice = t
            # clear query params to keep URLs clean if setter exists
            if hasattr(st, "experimental_set_query_params"):
                st.experimental_set_query_params()

    # Render SVG-based toggle button using components.html. Clicking the
    # icon will reload the page with ?theme=Light or ?theme=Dark which
    # the app reads above and applies.
    current = st.session_state.get("theme_choice", "System")
    is_dark = current == "Dark"
    svg_sun = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="4" fill="#f5c02a"/><g stroke="#f5c02a" stroke-width="1.2"><path d="M12 2v2"/><path d="M12 20v2"/><path d="M4.93 4.93l1.41 1.41"/><path d="M17.66 17.66l1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="M4.93 19.07l1.41-1.41"/><path d="M17.66 6.34l1.41-1.41"/></g></svg>'''
    svg_moon = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" fill="#f5c02a"/></svg>'''

    icon_html = svg_moon if is_dark else svg_sun
    next_theme = 'Light' if is_dark else 'Dark'

    template = '''<div style="padding:6px 0">
        <button id="theme-btn" style="background:transparent;border:none;cursor:pointer;padding:6px;border-radius:8px">__ICON__</button>
        <script>
        const btn = document.getElementById('theme-btn');
        btn.onclick = () => {
            const next = "__NEXT__";
            const search = new URLSearchParams(window.location.search);
            search.set('theme', next);
            window.location.search = search.toString();
        }
        </script>
    </div>'''

    html = template.replace('__ICON__', icon_html).replace('__NEXT__', next_theme)

    components.html(html, height=40)

# Inject a small script to add/remove theme classes on the app root.
if st.session_state.theme_choice == "Light":
    components.html(
        """
        <script>
        (function(){
            const root = document.querySelector('.stApp') || document.documentElement;
            root.classList.remove('light-theme','dark-theme');
            root.classList.add('light-theme');
        })();
        </script>
        """,
        height=0,
    )
elif st.session_state.theme_choice == "Dark":
    components.html(
        """
        <script>
        (function(){
            const root = document.querySelector('.stApp') || document.documentElement;
            root.classList.remove('light-theme','dark-theme');
            root.classList.add('dark-theme');
        })();
        </script>
        """,
        height=0,
    )
else:
    components.html(
        """
        <script>
        (function(){
            const root = document.querySelector('.stApp') || document.documentElement;
            root.classList.remove('light-theme','dark-theme');
        })();
        </script>
        """,
        height=0,
    )

# Initialize handlers
data_handler = DataHandler()
auth_handler = AuthHandler()
ui = UIComponents()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ==================== MAIN APP ====================
def main():
    if not st.session_state.logged_in:
        auth_handler.login_page()
    else:
        render_main_app()

# ==================== SIDEBAR ====================
def render_sidebar():
    with st.sidebar:
        user = data_handler.get_user(st.session_state.username)
        
        # Profile Section
        st.markdown(f"""
        <div style='text-align: center; padding: 20px 0;'>
            <img src="{user.get('avatar', f'https://api.dicebear.com/7.x/initials/svg?seed={st.session_state.username}')}" 
                 style='width: 80px; height: 80px; border-radius: 50%; border: 3px solid #00d4ff;'>
            <h3 style='margin: 10px 0 5px 0;'>{user.get('name', st.session_state.username)}</h3>
            <p style='color: #8b949e; margin: 0;'>@{st.session_state.username}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Points", user.get('points', 0))
        with col2:
            st.metric("Streak", user.get('streak', 0))
        
        st.markdown("---")
        
        # Status Update
        st.markdown("### Quick Links")
        current_status = user.get("status", "chilling")
        
        status_options = ["studying", "break", "sleeping", "chilling"]
        status_labels = {
            "studying": "Studying",
            "break": "Taking Break", 
            "sleeping": "Sleeping",
            "chilling": "Chilling"
        }
        status_emojis = {
            "studying": "🟢",
            "break": "🟡",
            "sleeping": "🔴",
            "chilling": "⚪"
        }
        
        current_index = status_options.index(current_status) if current_status in status_options else 3
        
        status_choice = st.radio(
            "Update your current activity:",
            status_options,
            format_func=lambda x: f"{status_emojis.get(x, '')} {status_labels[x]}",
            index=current_index,
            label_visibility="collapsed"
        )
        
        if st.button("Update Status", use_container_width=True):
            data_handler.update_status(st.session_state.username, status_choice)
            st.success(f"Status updated to {status_labels[status_choice]}!")
            st.rerun()
        
        st.markdown("---")
        
        # Quick Links
        st.markdown("### Quick Links")
        
        if st.button("My Profile", use_container_width=True):
            st.session_state.active_tab = "profile"
            st.rerun()
        
        # add a chat link so the user can open the chats page
        if st.button("My Chats", use_container_width=True):
            st.session_state.active_tab = "chats"
            st.rerun()
        
        if st.button("My Stats", use_container_width=True):
            st.session_state.active_tab = "stats"
            st.rerun()
        
        st.markdown("---")
        
        # Logout
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()


    def render_profile_page():
        """Show a profile page for either the current user or another student.

        The sidebar and other navigation buttons set ``st.session_state.viewing_profile``
        when the user clicks on a student.  If that key is absent we show the
        logged-in user's own profile (allowing them to edit their information).
        """
        # determine whose profile to display
        username = st.session_state.get("viewing_profile", st.session_state.username)
        user = data_handler.get_user(username)

        st.markdown(f"""
        <div class="section-header">
            <h2>{'Your' if username == st.session_state.username else user.get('name','Profile')}</h2>
        </div>
        """, unsafe_allow_html=True)

        # render card for aesthetics
        ui.render_user_card(user, username)

        # if it's the current user, allow editing
        if username == st.session_state.username:
            with st.form("edit_profile"):
                name = st.text_input("Name", value=user.get("name", ""))
                country = st.text_input("Country", value=user.get("country", ""))
                exam = st.text_input("Exam", value=user.get("exam", ""))
                grade = st.text_input("Grade", value=user.get("grade", ""))
                subjects = st.text_input("Subjects (comma separated)", value=", ".join(user.get("subjects", [])))
                bio = st.text_area("Bio", value=user.get("bio", ""))
                if st.form_submit_button("Save Changes"):
                    data_handler.update_profile(
                        username,
                        name=name,
                        country=country,
                        exam=exam,
                        grade=grade,
                        subjects=[s.strip() for s in subjects.split(",") if s.strip()],
                        bio=bio
                    )
                    st.success("Profile updated!")
                    st.rerun()

        # navigation
        if st.button("Back to Feed"):
            st.session_state.active_tab = "feed"
            # clear any viewing_profile flag so future visits default to own
            if "viewing_profile" in st.session_state:
                del st.session_state["viewing_profile"]
            st.rerun()


    def render_chats_page():
        """Display the list of chats and the selected conversation."""
        st.markdown("""
        <div class="section-header">
            <h2>My Chats</h2>
        </div>
        """, unsafe_allow_html=True)

        username = st.session_state.username
        chats = data_handler.get_chats_for_user(username)

        # list chat partners
        if chats:
            st.markdown("**Conversations:**")
            for c in chats:
                other = [u for u in c.get("users", []) if u != username][0]
                if st.button(other, key=f"open_chat_{c['id']}"):
                    st.session_state.open_chat = c["id"]
                    st.rerun()
        else:
            st.write("You haven't started any chats yet. Connect with classmates to chat!")

        chat_id = st.session_state.get("open_chat")
        if chat_id:
            # show the selected conversation
            chat_obj = next((c for c in chats if c.get("id") == chat_id), None)
            if chat_obj:
                st.markdown("---")
                st.markdown(f"**Chat with { [u for u in chat_obj.get('users') if u!=username][0] }**")
                for msg in chat_obj.get("messages", []):
                    st.markdown(f"**{msg['user']}**: {msg['text']}")
                with st.form("send_msg"):
                    msg_text = st.text_input("Message", key="msg_input")
                    if st.form_submit_button("Send"):
                        if msg_text:
                            data_handler.send_message(chat_id, username, msg_text)
                            st.rerun()

        # back button
        if st.button("Back to Feed"):
            st.session_state.active_tab = "feed"
            if "open_chat" in st.session_state:
                del st.session_state["open_chat"]
            st.rerun()

# ==================== MAIN CONTENT ====================
def render_main_app():
    render_sidebar()
    
    # Initialize active tab
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "feed"
    
    user = data_handler.get_user(st.session_state.username)
    
    # Header
    st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;'>
        <div>
            <h1 style='margin: 0;'>Welcome back, <span class='gradient-text'>{user.get('name', 'Student')}</span>!</h1>
            <p style='color: #8b949e; margin: 5px 0 0 0;'>
                Country: {user.get('country', 'Earth')} | Exam: {user.get('exam', 'Preparing')} | Grade: {user.get('grade', 'Learning')}
            </p>
        </div>
        <div style='text-align: right;'>
            <!-- simpler status badge: dot + bold text, aligned center -->
            <span class='status-display'>
                {ui.status_emoji(user.get('status', 'chilling'))}
                <strong>{user.get('status', 'chilling').title()}</strong>
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Tabs
    tab_names = ["Feed", "Need Help", "Find Mentor", "Students", "Stats"]
    tab1, tab2, tab3, tab4, tab5 = st.tabs(tab_names)
    
    # ==================== FEED TAB ====================
    with tab1:
        st.markdown("""
        <div class="section-header">
            <h2>Global Student Feed</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Create Post
        with st.expander("Create New Post", expanded=False):
            if Card:
                with Card():
                    post_content = st.text_area("Share something with your study mates:", height=100, placeholder="What's on your mind?")
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        post_type = st.selectbox("Post Type", ["normal", "achievement", "motivation", "question"])
                    with col2:
                        if Button and Button("Post", full_width=True).clicked():
                            if post_content:
                                data_handler.create_post(st.session_state.username, post_content, post_type)
                                st.success("Posted successfully!")
                                st.rerun()
                            else:
                                st.warning("Please write something first!")
            else:
                post_content = st.text_area("Share something with your study mates:", height=100, placeholder="What's on your mind?")
                col1, col2 = st.columns([1, 4])
                with col1:
                    post_type = st.selectbox("Post Type", ["normal", "achievement", "motivation", "question"])
                with col2:
                    if st.button("Post", use_container_width=True):
                        if post_content:
                            data_handler.create_post(st.session_state.username, post_content, post_type)
                            st.success("Posted successfully!")
                            st.rerun()
                        else:
                            st.warning("Please write something first!")
        
        # Filter posts
        col1, col2 = st.columns([3, 1])
        with col1:
            filter_exam = st.selectbox("Filter by Exam", ["All"] + sorted(list(set(p.get("user_exam", "") for p in data_handler.get_posts()))))
        with col2:
            filter_country = st.selectbox("Filter by Country", ["All"] + sorted(list(set(p.get("user_country", "") for p in data_handler.get_posts()))))
        
        # Display posts
        posts = data_handler.get_posts()
        
        # Apply filters
        if filter_exam != "All":
            posts = [p for p in posts if p.get("user_exam") == filter_exam]
        if filter_country != "All":
            posts = [p for p in posts if p.get("user_country") == filter_country]
        
        for post in posts:
            # Instagram-like post card
            st.markdown(f"""
            <div class="instagram-post">
                <div class="post-header">
                    <img src="https://api.dicebear.com/7.x/initials/svg?seed={post['user']}" class="post-avatar">
                    <div class="post-user-info">
                        <strong>{post['user']}</strong>
                        <span class="post-meta">{ui.time_ago(post.get('time', ''))}</span>
                    </div>
                </div>
                <div class="post-content">
                    {post.get('content', '')}
                </div>
                <div class="post-actions">
                    <div class="reaction-buttons">
            """, unsafe_allow_html=True)
            
            # Like/Dislike buttons
            col1, col2 = st.columns([1, 1])
            with col1:
                likes = len(post.get('likes', []))
                if st.button(f"❤️ {likes}", key=f"like_{post['id']}"):
                    data_handler.like_post(post['id'], st.session_state.username)
                    st.rerun()
            with col2:
                dislikes = len(post.get('dislikes', []))
                if st.button(f"👎 {dislikes}", key=f"dislike_{post['id']}"):
                    data_handler.dislike_post(post['id'], st.session_state.username)
                    st.rerun()
            
            # Emoji reactions
            reaction_emojis = ["😂", "😍", "😮", "😢", "😡", "👍", "👏"]
            reactions = post.get('reactions', {})
            for emoji in reaction_emojis:
                count = len(reactions.get(emoji, []))
                if st.button(f"{emoji} {count}", key=f"react_{post['id']}_{emoji}"):
                    data_handler.react_to_post(post['id'], st.session_state.username, emoji)
                    st.rerun()
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            # Comments section
            comments = post.get('comments', [])
            if comments:
                st.markdown(f"<div class='comments-section'><h4>{len(comments)} Comments</h4>", unsafe_allow_html=True)
                for i, comment in enumerate(comments):
                    st.markdown(f"""
                    <div class='comment'>
                        <strong>{comment['user']}</strong>: {comment['comment']}
                        <small>{ui.time_ago(comment.get('time', ''))}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Reactions on comment
                    for emoji in ["❤️", "😂", "😮"]:
                        count = len(comment.get('reactions', {}).get(emoji, []))
                        if st.button(f"{emoji} {count}", key=f"comment_react_{post['id']}_{i}_{emoji}"):
                            data_handler.react_to_comment(post['id'], i, st.session_state.username, emoji)
                            st.rerun()
                    
                    # Replies
                    replies = comment.get('replies', [])
                    if replies:
                        for reply in replies:
                            st.markdown(f"""
                            <div class='reply'>
                                <strong>{reply['user']}</strong>: {reply['reply']}
                                <small>{ui.time_ago(reply.get('time', ''))}</small>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Reply form
                    with st.expander(f"Reply to {comment['user']}", expanded=False):
                        reply_text = st.text_input("Your reply:", key=f"reply_{post['id']}_{i}")
                        if st.button("Reply", key=f"submit_reply_{post['id']}_{i}"):
                            if reply_text:
                                data_handler.reply_to_comment(post['id'], i, st.session_state.username, reply_text)
                                st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Add comment
            with st.form(f"comment_{post['id']}"):
                comment_text = st.text_input("Add a comment:", key=f"comment_input_{post['id']}")
                if st.form_submit_button("Comment"):
                    if comment_text:
                        data_handler.comment_post(post["id"], st.session_state.username, comment_text)
                        st.rerun()
            
            st.markdown("---")
        
        if not posts:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">{}</div>
                <h3>No posts yet</h3>
                <p>Be the first to share something with the community!</p>
            </div>
            """.format("") , unsafe_allow_html=True)
    
    # ==================== NEED HELP TAB ====================
    with tab2:
        if "selected_question" not in st.session_state:
            st.session_state.selected_question = None
        
        if st.session_state.selected_question:
            # Detailed question view
            help_req = next((h for h in data_handler.get_help_requests() if h['id'] == st.session_state.selected_question), None)
            if help_req:
                st.markdown(f"""
                <div class="question-detail">
                    <h2>{help_req.get('question', '')}</h2>
                    <p class="question-meta">Asked by {help_req.get('user_name', '')} • {ui.time_ago(help_req.get('time', ''))} • {help_req.get('subject', '')} • {help_req.get('exam', '')}</p>
                    <p class="question-body">{help_req.get('question', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Sort options
                sort_by = st.selectbox("Sort answers by:", ["upvotes", "downvotes", "time_latest", "time_oldest"])
                
                answers = help_req.get('answers', [])
                if sort_by == "upvotes":
                    answers = sorted(answers, key=lambda x: len(x.get('upvotes', [])), reverse=True)
                elif sort_by == "downvotes":
                    answers = sorted(answers, key=lambda x: len(x.get('downvotes', [])), reverse=True)
                elif sort_by == "time_latest":
                    answers = sorted(answers, key=lambda x: x.get('time', ''), reverse=True)
                elif sort_by == "time_oldest":
                    answers = sorted(answers, key=lambda x: x.get('time', ''))
                
                for idx, ans in enumerate(answers):
                    upvotes = len(ans.get('upvotes', []))
                    downvotes = len(ans.get('downvotes', []))
                    st.markdown(f"""
                    <div class="answer-card">
                        <div class="answer-header">
                            <strong>{ans['user_name']}</strong> • {ui.time_ago(ans['time'])}
                        </div>
                        <div class="answer-body">
                            {ans['answer']}
                        </div>
                        <div class="answer-actions">
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button(f"👍 {upvotes}", key=f"upvote_{help_req['id']}_{idx}"):
                            data_handler.upvote_answer(help_req['id'], idx, st.session_state.username)
                            st.rerun()
                    with col2:
                        if st.button(f"👎 {downvotes}", key=f"downvote_{help_req['id']}_{idx}"):
                            data_handler.downvote_answer(help_req['id'], idx, st.session_state.username)
                            st.rerun()
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Comments on answer
                    comments = ans.get('comments', [])
                    if comments:
                        st.markdown("<div class='answer-comments'>", unsafe_allow_html=True)
                        for c_idx, comment in enumerate(comments):
                            st.markdown(f"""
                            <div class='answer-comment'>
                                <strong>{comment['user']}</strong>: {comment['comment']}
                                <small>{ui.time_ago(comment.get('time', ''))}</small>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Reactions on comment
                            for emoji in ["❤️", "😂", "😮"]:
                                count = len(comment.get('reactions', {}).get(emoji, []))
                                if st.button(f"{emoji} {count}", key=f"ans_comment_react_{help_req['id']}_{idx}_{c_idx}_{emoji}"):
                                    data_handler.react_to_answer_comment(help_req['id'], idx, c_idx, st.session_state.username, emoji)
                                    st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Add comment on answer
                    with st.form(f"comment_answer_{help_req['id']}_{idx}"):
                        comment_text = st.text_input("Comment on this answer:", key=f"comment_ans_input_{help_req['id']}_{idx}")
                        if st.form_submit_button("Comment"):
                            if comment_text:
                                data_handler.comment_on_answer(help_req['id'], idx, st.session_state.username, comment_text)
                                st.rerun()
                
                # Answer form
                with st.form(f"answer_{help_req['id']}"):
                    answer_text = st.text_area("Your answer:", height=100)
                    if st.form_submit_button("Submit Answer"):
                        if answer_text:
                            data_handler.answer_help(help_req["id"], st.session_state.username, answer_text)
                            st.success("Answer submitted! +3 points earned!")
                            st.rerun()
                
                if st.button("← Back to Questions"):
                    st.session_state.selected_question = None
                    st.rerun()
            else:
                st.session_state.selected_question = None
        else:
            # Questions list
            st.markdown("""
            <div class="section-header">
                <h2>Questions</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Create help request
            with st.expander("Ask a Question", expanded=False):
                if Card:
                    with Card():
                        help_subject = st.selectbox("Subject", [
                            "Mathematics", "Physics", "Chemistry", "Biology",
                            "English", "History", "Geography", "Economics",
                            "Computer Science", "Literature", "Philosophy", "Other"
                        ])
                        help_question = st.text_area("Describe your problem in detail:", height=100)
                        help_exam = st.selectbox("Related Exam", [
                            "Any", "JEE", "NEET", "UPSC", "SAT", "GRE", "GMAT",
                            "GCSE", "A-Levels", "IB", "Boards", "Gaokao", "Other"
                        ])
                        help_urgency = st.selectbox("Urgency", ["low", "normal", "high"])
                        if Button and Button("Submit Question", full_width=True).clicked():
                            if help_question:
                                data_handler.create_help_request(
                                    st.session_state.username, 
                                    help_subject, 
                                    help_question, 
                                    help_exam, 
                                    help_urgency
                                )
                                st.success("Question posted!")
                                st.rerun()
                            else:
                                st.warning("Please describe your problem!")
                else:
                    help_subject = st.selectbox("Subject", [
                        "Mathematics", "Physics", "Chemistry", "Biology",
                        "English", "History", "Geography", "Economics",
                        "Computer Science", "Literature", "Philosophy", "Other"
                    ])
                    help_question = st.text_area("Describe your problem in detail:", height=100)
                    help_exam = st.selectbox("Related Exam", [
                        "Any", "JEE", "NEET", "UPSC", "SAT", "GRE", "GMAT",
                        "GCSE", "A-Levels", "IB", "Boards", "Gaokao", "Other"
                    ])
                    help_urgency = st.selectbox("Urgency", ["low", "normal", "high"])
                    
                    if st.button("Submit Question"):
                        if help_question:
                            data_handler.create_help_request(
                                st.session_state.username, 
                                help_subject, 
                                help_question, 
                                help_exam, 
                                help_urgency
                            )
                            st.success("Question posted!")
                            st.rerun()
                        else:
                            st.warning("Please describe your problem!")
            
            # Filter questions
            col1, col2 = st.columns(2)
            with col1:
                help_filter_subject = st.selectbox("Filter by Subject", ["All"] + [
                    "Mathematics", "Physics", "Chemistry", "Biology",
                    "English", "History", "Geography", "Economics",
                    "Computer Science", "Literature", "Philosophy", "Other"
                ])
            with col2:
                help_filter_exam = st.selectbox("Filter by Exam", ["All", "Any", "JEE", "NEET", "UPSC", "SAT", "GRE", "GMAT", "GCSE", "A-Levels", "IB", "Boards"])
            
            # Display questions
            helps = data_handler.get_help_requests(help_filter_subject, help_filter_exam)
            
            for h in helps:
                answers_count = len(h.get('answers', []))
                urgency_color = {"high": "#ff4757", "normal": "#ffa502", "low": "#2ed573"}.get(h.get("urgency", "normal"), "#ffa502")
                if st.button(f"{h.get('question', '')[:100]}...", key=f"select_q_{h['id']}", use_container_width=True):
                    st.session_state.selected_question = h['id']
                    st.rerun()
                
                st.markdown(f"""
                <div class="question-summary">
                    <span class="question-title">{h.get('question', '')}</span>
                    <div class="question-info">
                        <span class="tag" style="background: {urgency_color};">{h.get('urgency', 'normal').upper()}</span>
                        <span class="tag">{h.get('subject', '')}</span>
                        <span class="tag">{h.get('exam', '')}</span>
                        <span class="answers-count">{answers_count} answers</span>
                        <small>Asked by {h.get('user_name', '')} • {ui.time_ago(h.get('time', ''))}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if not helps:
                st.markdown("""
                <div class="empty-state">
                    <div class="empty-state-icon"></div>
                    <h3>No questions yet</h3>
                    <p>Be the first to ask a question!</p>
                </div>
                """, unsafe_allow_html=True)
    
    # ==================== FIND MENTOR TAB ====================
    with tab3:
        st.markdown("""
        <div class="section-header">
            <h2>Find a Mentor</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Become a mentor
        with st.expander("Become a Mentor", expanded=False):
            mentor_subject = st.selectbox("Your Subject Expertise", [
                "Mathematics", "Physics", "Chemistry", "Biology",
                "English", "History", "Geography", "Economics",
                "Computer Science", "Literature", "Philosophy"
            ])
            mentor_exp = st.text_area("Your experience & achievements:", height=80)
            mentor_avail = st.selectbox("Availability", ["Weekdays", "Weekends", "Anytime"])
            
            if st.button("Register as Mentor"):
                if mentor_exp:
                    data_handler.register_mentor(
                        st.session_state.username,
                        mentor_subject,
                        mentor_exp,
                        mentor_avail
                    )
                    st.success("You're now a mentor!")
                    st.rerun()
                else:
                    st.warning("Please describe your experience!")
        
        # Filter mentors
        col1, col2 = st.columns(2)
        with col1:
            mentor_filter_subject = st.selectbox("Filter by Subject", ["All"] + [
                "Mathematics", "Physics", "Chemistry", "Biology",
                "English", "History", "Geography", "Economics",
                "Computer Science", "Literature", "Philosophy"
            ])
        with col2:
            mentor_filter_exam = st.selectbox("Filter by Exam", ["All", "JEE", "NEET", "UPSC", "SAT", "GRE", "GMAT", "GCSE", "A-Levels", "IB"])
        
        # Display mentors
        mentors = data_handler.get_mentors(mentor_filter_subject, mentor_filter_exam)
        
        for mentor in mentors:
            ui.render_mentor_card(mentor)
            
            if st.button(f"Connect with {mentor['user']}", key=f"connect_{mentor['id']}"):
                st.success(f"Connection request sent to {mentor['user']}!")
            
            st.markdown("---")
        
        if not mentors:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon"></div>
                <h3>No mentors available</h3>
                <p>Be the first to become a mentor!</p>
            </div>
            """, unsafe_allow_html=True)
    
    # ==================== STUDENTS TAB ====================
    with tab4:
        st.markdown("""
        <div class="section-header">
            <h2>All Students</h2>
        </div>
        """, unsafe_allow_html=True)
        
        users = data_handler.get_user("")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_country = st.selectbox("Country", ["All"] + sorted(list(set(
                u.get("country", "") for u in data_handler.data["users"].values()
            ))))
        with col2:
            filter_exam = st.selectbox("Exam", ["All"] + sorted(list(set(
                u.get("exam", "") for u in data_handler.data["users"].values()
            ))))
        with col3:
            filter_grade = st.selectbox("Grade", ["All"] + sorted(list(set(
                u.get("grade", "") for u in data_handler.data["users"].values()
            ))))
        
        # Display users
        for username, u in data_handler.data["users"].items():
            # Apply filters
            if filter_country != "All" and u.get("country") != filter_country:
                continue
            if filter_exam != "All" and u.get("exam") != filter_exam:
                continue
            if filter_grade != "All" and u.get("grade") != filter_grade:
                continue
            
            if username == st.session_state.username:
                continue  # Skip current user
            
            ui.render_user_card(u, username)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"View Profile", key=f"view_{username}"):
                    st.session_state.viewing_profile = username
                    st.rerun()
            with col2:
                # if we are already connected a chat may exist; always open
                # a chat when the user clicks this button. also establish
                # a connection record so that "My Connections" (if added)
                # stays consistent.
                if st.button(f"Chat", key=f"chat_{username}"):
                    data_handler.add_connection(st.session_state.username, username)
                    chat_id = data_handler.create_chat(st.session_state.username, username)
                    st.session_state.open_chat = chat_id
                    st.session_state.active_tab = "chats"
                    st.rerun()
            
            st.markdown("---")
    
    # ==================== STATS TAB ====================
    with tab5:
        st.markdown("""
        <div class="section-header">
            <h2>Platform Statistics</h2>
        </div>
        """, unsafe_allow_html=True)
        
        stats = data_handler.get_stats()
        ui.render_stats_cards(stats)
        
        st.markdown("---")
        
        # User's personal stats
        st.markdown("### Your Personal Stats")
        
        user = data_handler.get_user(st.session_state.username)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Points", user.get("points", 0))
        with col2:
            st.metric("Current Streak", user.get("streak", 0))
        with col3:
            st.metric("Connections", len(user.get("connections", [])))
        with col4:
            st.metric("Badges", len(user.get("badges", [])))
        
        # Show badges
        if user.get("badges"):
            st.markdown("### Your Badges")
            badges_icons = {
                "mentor": "Mentor",
                "first_post": "First Post",
                "helper": "Helper",
                "streak_7": "7 Day Streak",
                "streak_30": "30 Day Streak"
            }
            for badge in user.get("badges", []):
                st.markdown(f"- {badges_icons.get(badge, badge)}")

# ==================== RUN APP ====================
if __name__ == "__main__":
    main()