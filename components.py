"""
UI Components Module - All UI rendering functions
"""

import streamlit as st
from datetime import datetime
from icons import svg as icon_svg

class UIComponents:
    @staticmethod
    def status_emoji(status: str) -> str:
        # return a small colored dot as SVG for statuses
        colors = {"studying": "#16a34a", "break": "#f59e0b", "sleeping": "#6b7280", "chilling": "#9ca3af"}
        c = colors.get(status, "#9ca3af")
        return f"<svg width=\"12\" height=\"12\" viewBox=\"0 0 12 12\" xmlns=\"http://www.w3.org/2000/svg\"><circle cx=\"6\" cy=\"6\" r=\"5\" fill=\"{c}\" /></svg>"
    
    @staticmethod
    def status_color(status: str) -> str:
        return {"studying": "#28a745", "break": "#ffc107", "sleeping": "#6c757d", "chilling": "#17a2b8"}.get(status, "#17a2b8")
    
    @staticmethod
    def render_user_card(user_data: dict, username: str, compact: bool = False):
        status = user_data.get("status", "chilling")
        status_emoji = UIComponents.status_emoji(status)
        status_color = UIComponents.status_color(status)
        
        if compact:
            st.markdown(f"""
            <div class="user-compact-card">
                {status_emoji}
                <strong>{username}</strong>
                <span style="color: var(--muted); font-size: 0.8em; margin-left:8px">{user_data.get('exam', '')}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="user-card">
                <div class="user-card-header">
                    <img src="{user_data.get('avatar', f'https://api.dicebear.com/7.x/initials/svg?seed={username}')}" 
                         class="user-avatar">
                    <div>
                        <h3>{username} {status_emoji}</h3>
                        <p style="margin:0">{user_data.get('name', 'Anonymous')}</p>
                    </div>
                    <div class="user-points">{icon_svg('stats',12)} {user_data.get('points', 0)}</div>
                </div>
                <div class="user-card-body">
                    <span class="tag">Country: {user_data.get('country', 'N/A')}</span>
                    <span class="tag">Exam: {user_data.get('exam', 'N/A')}</span>
                    <span class="tag">Grade: {user_data.get('grade', 'N/A')}</span>
                </div>
                <div class="user-card-footer">
                    <small>{', '.join(user_data.get('subjects', []))}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_post_card(post: dict):
        user = post.get("user", "Anonymous")
        status_emoji = UIComponents.status_emoji(post.get("user_status", "chilling"))
        status_color = UIComponents.status_color(post.get("user_status", "chilling"))
        
        time_ago = UIComponents.time_ago(post.get("time", ""))
        likes = len(post.get("likes", []))
        comments = len(post.get("comments", []))
        
        st.markdown(f"""
        <div class="post-card">
            <div class="post-header">
                <img src="https://api.dicebear.com/7.x/initials/svg?seed={user}" class="post-avatar">
                <div class="post-user-info">
                    <strong>{user}</strong> {status_emoji}
                    <span class="post-meta">{post.get('user_exam', '')} • {post.get('user_country', '')} • {time_ago}</span>
                </div>
            </div>
            <div class="post-content">
                {post.get('content', '')}
            </div>
            <div class="post-stats">
                <span>{icon_svg('heart',12)} {likes} likes</span>
                <span>{icon_svg('comment',12)} {comments} comments</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_help_card(help_req: dict):
        urgency_colors = {"high": "#ff4757", "normal": "#ffa502", "low": "#2ed573"}
        color = urgency_colors.get(help_req.get("urgency", "normal"), "#ffa502")
        
        st.markdown(f"""
        <div class="help-card">
            <div class="help-header">
                <span class="urgency-tag" style="background: {color};">{help_req.get('urgency', 'normal').upper()}</span>
                <span class="help-subject">Subject: {help_req.get('subject', '')}</span>
                <span class="help-exam">Exam: {help_req.get('exam', '')}</span>
            </div>
            <div class="help-body">
                <p class="help-question">{help_req.get('question', '')}</p>
                <p class="help-meta">Asked by {help_req.get('user_name', help_req.get('user', 'Anonymous'))} • {UIComponents.time_ago(help_req.get('time', ''))}</p>
            </div>
            <div class="help-stats">
                <span>{icon_svg('comment',12)} {len(help_req.get('answers', []))} answers</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_mentor_card(mentor: dict):
        st.markdown(f"""
        <div class="mentor-card">
            <div class="mentor-header">
                <img src="https://api.dicebear.com/7.x/initials/svg?seed={mentor.get('user', '')}" 
                     class="mentor-avatar">
                <div>
                    <h4>{mentor.get('user', '')}</h4>
                    <p style="margin:0">{mentor.get('name', '')}</p>
                </div>
                <div class="mentor-rating">{icon_svg('mentor',12)} {mentor.get('rating', 5.0)}</div>
            </div>
            <div class="mentor-body">
                <p><strong>Subject:</strong> {mentor.get('subject', '')}</p>
                <p><strong>Experience:</strong> {mentor.get('experience', '')}</p>
                <p><strong>Availability:</strong> {mentor.get('availability', '')}</p>
                <p><small>Country: {mentor.get('country', '')} | Exam: {mentor.get('exam', '')}</small></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def time_ago(time_str: str) -> str:
        try:
            dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            now = datetime.now()
            diff = now - dt
            
            minutes = diff.total_seconds() / 60
            if minutes < 1:
                return "Just now"
            elif minutes < 60:
                return f"{int(minutes)}m ago"
            elif minutes < 1440:
                return f"{int(minutes/60)}h ago"
            else:
                return f"{int(minutes/1440)}d ago"
        except:
            return time_str
    
    @staticmethod
    def render_stats_cards(stats: dict):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card" style="border-left: 4px solid #00d4ff;">
                <h2>{stats.get('total_users', 0)}</h2>
                <p>Students</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card" style="border-left: 4px solid #7b2cbf;">
                <h2>{stats.get('total_posts', 0)}</h2>
                <p>Posts</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card" style="border-left: 4px solid #ff6b6b;">
                <h2>{stats.get('total_helps', 0)}</h2>
                <p>Helps</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stat-card" style="border-left: 4px solid #2ed573;">
                <h2>{stats.get('total_mentors', 0)}</h2>
                <p>Mentors</p>
            </div>
            """, unsafe_allow_html=True)