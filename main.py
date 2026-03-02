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
from styles import get_styles

# Initialize
st.set_page_config(
    page_title="StudyConnect",
    page_icon="SC",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply styles
st.markdown(get_styles(), unsafe_allow_html=True)

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
        
        current_index = status_options.index(current_status) if current_status in status_options else 3
        
        status_choice = st.radio(
            "Update your current activity:",
            status_options,
            format_func=lambda x: status_labels[x],
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
        
        if st.button("My Stats", use_container_width=True):
            st.session_state.active_tab = "stats"
            st.rerun()
        
        st.markdown("---")
        
        # Logout
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
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
            <span style='background: linear-gradient(90deg, #7b2cbf, #00d4ff); padding: 8px 16px; border-radius: 20px;'>
                {ui.status_emoji(user.get('status', 'chilling'))} {user.get('status', 'chilling').title()}
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
            post_content = st.text_area("Share something with your study mates:", height=100)
            
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
            ui.render_post_card(post)
            
            # Like and Comment buttons
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                likes = len(post.get("likes", []))
                if st.button(f"Like {likes}", key=f"like_{post['id']}"):
                    data_handler.like_post(post["id"], st.session_state.username)
                    st.rerun()
            with col2:
                st.write(f"{len(post.get('comments', []))} comments")
            with col3:
                pass
            
            # Show comments
            if post.get("comments"):
                with st.expander("View Comments"):
                    for comment in post["comments"]:
                        st.markdown(f"**{comment['user']}**: {comment['comment']}")
            
            # Add comment
            with st.form(f"comment_{post['id']}"):
                comment_text = st.text_input("Add a comment:", key=f"comment_input_{post['id']}")
                if st.form_submit_button("Submit"):
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
        st.markdown("""
        <div class="section-header">
            <h2>I Need Help</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Create help request
        with st.expander("Ask for Help", expanded=False):
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
            
            if st.button("Submit Help Request"):
                if help_question:
                    data_handler.create_help_request(
                        st.session_state.username, 
                        help_subject, 
                        help_question, 
                        help_exam, 
                        help_urgency
                    )
                    st.success("Help request posted! Someone will help you soon.")
                    st.rerun()
                else:
                    st.warning("Please describe your problem!")
        
        # Filter help requests
        col1, col2 = st.columns(2)
        with col1:
            help_filter_subject = st.selectbox("Filter by Subject", ["All"] + [
                "Mathematics", "Physics", "Chemistry", "Biology",
                "English", "History", "Geography", "Economics",
                "Computer Science", "Literature", "Philosophy", "Other"
            ])
        with col2:
            help_filter_exam = st.selectbox("Filter by Exam", ["All", "Any", "JEE", "NEET", "UPSC", "SAT", "GRE", "GMAT", "GCSE", "A-Levels", "IB", "Boards"])
        
        # Display help requests
        helps = data_handler.get_help_requests(help_filter_subject, help_filter_exam)
        
        for h in helps:
            ui.render_help_card(h)
            
            # Show answers
            if h.get("answers"):
                with st.expander(f"{len(h['answers'])} Answers"):
                    for ans in h["answers"]:
                        st.markdown(f"""
                        <div style='background: #161b22; padding: 12px; border-radius: 8px; margin: 8px 0;'>
                            <strong>{ans['user_name']}</strong> <small style='color: #8b949e;'>• {ui.time_ago(ans['time'])}</small>
                            <p style='margin: 5px 0;'>{ans['answer']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Answer form
            with st.form(f"answer_{h['id']}"):
                answer_text = st.text_input("Your answer:", key=f"answer_input_{h['id']}")
                if st.form_submit_button("Submit Answer"):
                    if answer_text:
                        data_handler.answer_help(h["id"], st.session_state.username, answer_text)
                        st.success("Answer submitted! +3 points earned!")
                        st.rerun()
            
            st.markdown("---")
        
        if not helps:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon"></div>
                <h3>No help requests</h3>
                <p>Need help with something? Ask the community!</p>
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
                if st.button(f"Connect", key=f"conn_{username}"):
                    data_handler.add_connection(st.session_state.username, username)
                    st.success(f"Connected with {username}!")
            
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