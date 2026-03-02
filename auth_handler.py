import streamlit as st
from data_handler import DataHandler
from icons import svg as icon_svg

class AuthHandler:
    def __init__(self):
        self.data_handler = DataHandler()
    
    def login_page(self):
        """Display login page"""
        # Custom CSS for auth page
        st.markdown("""
        <style>
        .auth-container {
            max-width: 450px;
            margin: 0 auto;
            padding: 40px;
            background: linear-gradient(145deg, #1a1a2e, #16213e);
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }
        .auth-title {
            text-align: center;
            font-size: 2.5em;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .auth-subtitle {
            text-align: center;
            color: #888;
            margin-bottom: 30px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        st.markdown(f'<h1 class="auth-title">{icon_svg("book",20)} StudyConnect</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="auth-subtitle">{icon_svg("globe",14)} The LinkedIn for Students</p>', unsafe_allow_html=True)
        
        # Tab for Login/Register
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Login", use_container_width=True):
                    if self.data_handler.verify_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Invalid username or password!")
            
            st.markdown("---")
            st.info("Demo: Register a new account to explore!")
        
        with tab2:
            new_user = st.text_input("Choose Username", key="reg_user")
            new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
            name = st.text_input("Full Name", key="reg_name")
            
            col1, col2 = st.columns(2)
            with col1:
                country = st.selectbox("Country", [
                    "India", "USA", "UK", "Canada", "Australia", 
                    "Germany", "France", "Japan", "Singapore", 
                    "China", "South Korea", "UAE", "Other"
                ])
            with col2:
                exam = st.selectbox("Target Exam", [
                    "JEE", "NEET", "UPSC", "SAT", "GRE", "GMAT",
                    "GCSE", "A-Levels", "IB", "Boards", "Gaokao",
                    "Baccalaureate", "Other"
                ])
            
            grade = st.selectbox("Grade/Class", [
                "Class 6", "Class 7", "Class 8", "Class 9", "Class 10",
                "Class 11", "Class 12", "College 1st Year", "College 2nd Year",
                "College 3rd Year", "College Final Year", "Post Graduate"
            ])
            
            subjects = st.multiselect("Subjects of Interest", [
                "Mathematics", "Physics", "Chemistry", "Biology",
                "English", "History", "Geography", "Economics",
                "Computer Science", "Literature", "Philosophy",
                "Political Science", "Commerce"
            ])
            
            bio = st.text_area("Short Bio (optional)")
            
            if st.button("Create Account", use_container_width=True):
                if new_user and new_pass and name and country and exam and grade and subjects:
                    if self.data_handler.create_user(new_user, new_pass, name, country, exam, grade, subjects, bio):
                        st.success("Account created! Please login.")
                    else:
                        st.error("Username already exists!")
                else:
                    st.warning("Please fill all required fields!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Stats at bottom
        stats = self.data_handler.get_stats()
        st.markdown(f"""
        <div style='text-align: center; margin-top: 30px; color: #666;'>
            <p>{icon_svg('globe',12)} {stats['total_users']} Students | {icon_svg('comment',12)} {stats['total_posts']} Posts | {icon_svg('mentor',12)} {stats['total_mentors']} Mentors</p>
        </div>
        """, unsafe_allow_html=True)