import json
import os
from datetime import datetime
from typing import Dict, List, Any

DATA_FILE = "studyconnect_data.json"

class DataHandler:
    def __init__(self):
        self.data = self.load_data()
    
    def load_data(self) -> Dict:
        """Load data from JSON file"""
        if not os.path.exists(DATA_FILE):
            # initialize all expected top‑level collections, including chats
            return {
                "users": {},
                "posts": [],
                "helps": [],
                "mentors": [],
                "connections": [],
                "study_rooms": [],
                "chats": []
            }
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                # ensure backwards compatibility: older versions may not have
                # chats key
                if "chats" not in data:
                    data["chats"] = []
                return data
        except:
            return {
                "users": {},
                "posts": [],
                "helps": [],
                "mentors": [],
                "connections": [],
                "study_rooms": [],
                "chats": []
            }
    
    def save_data(self):
        """Save data to JSON file"""
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=2, default=str)
    
    # ==================== USER OPERATIONS ====================
    def create_user(self, username: str, password: str, name: str, country: str, 
                    exam: str, grade: str, subjects: List[str], bio: str = "") -> bool:
        """Create a new user"""
        if username in self.data["users"]:
            return False
        
        self.data["users"][username] = {
            "password": password,
            "name": name,
            "country": country,
            "exam": exam,
            "grade": grade,
            "subjects": subjects,
            "bio": bio,
            "status": "chilling",
            "status_time": str(datetime.now()),
            "points": 0,
            "streak": 0,
            "joined": str(datetime.now()),
            "avatar": f"https://api.dicebear.com/7.x/initials/svg?seed={username}",
            "connections": [],
            "badges": []
        }
        self.save_data()
        return True
    
    def get_user(self, username: str) -> Dict:
        """Get user by username"""
        return self.data["users"].get(username, {})
    
    def verify_user(self, username: str, password: str) -> bool:
        """Verify user credentials"""
        user = self.get_user(username)
        return bool(user and user.get("password") == password)
    
    def update_status(self, username: str, status: str) -> bool:
        """Update user status"""
        if username in self.data["users"]:
            old_status = self.data["users"][username].get("status", "chilling")
            self.data["users"][username]["status"] = status
            self.data["users"][username]["status_time"] = str(datetime.now())
            
            # Award points for studying
            if status == "studying" and old_status != "studying":
                self.data["users"][username]["points"] += 5
            elif status == "break" and old_status == "studying":
                self.data["users"][username]["streak"] += 1
            
            self.save_data()
            return True
        return False
    
    def update_profile(self, username: str, **kwargs) -> bool:
        """Update user profile"""
        if username in self.data["users"]:
            self.data["users"][username].update(kwargs)
            self.save_data()
            return True
        return False
    
    def add_connection(self, user1: str, user2: str):
        """Add connection between users"""
        if user1 not in self.data["users"][user1].get("connections", []):
            self.data["users"][user1]["connections"].append(user2)
        if user2 not in self.data["users"][user2].get("connections", []):
            self.data["users"][user2]["connections"].append(user1)
        self.save_data()
    
    # ==================== POST OPERATIONS ====================
    def create_post(self, username: str, content: str, post_type: str = "normal") -> bool:
        """Create a new post"""
        user = self.get_user(username)
        post = {
            "id": len(self.data["posts"]) + 1,
            "user": username,
            "user_name": user.get("name", username),
            "user_exam": user.get("exam", ""),
            "user_country": user.get("country", ""),
            "user_status": user.get("status", "chilling"),
            "content": content,
            "type": post_type,
            "time": str(datetime.now()),
            "likes": [],
            "dislikes": [],
            "reactions": {},  # emoji -> list of users
            "comments": []  # each comment: {"user":, "comment":, "time":, "replies": [], "reactions": {}}
        }
        self.data["posts"].append(post)
        self.save_data()
        return True
    
    def like_post(self, post_id: int, username: str):
        """Like a post"""
        for post in self.data["posts"]:
            if post["id"] == post_id:
                if username in post["likes"]:
                    post["likes"].remove(username)
                else:
                    post["likes"].append(username)
                    # remove dislike if present
                    if username in post.get("dislikes", []):
                        post["dislikes"].remove(username)
                self.save_data()
                break
    
    def dislike_post(self, post_id: int, username: str):
        """Dislike a post"""
        for post in self.data["posts"]:
            if post["id"] == post_id:
                dislikes = post.setdefault("dislikes", [])
                if username in dislikes:
                    dislikes.remove(username)
                else:
                    dislikes.append(username)
                    # remove like if present
                    if username in post["likes"]:
                        post["likes"].remove(username)
                self.save_data()
                break
    
    def react_to_post(self, post_id: int, username: str, emoji: str):
        """Add/remove emoji reaction to post"""
        for post in self.data["posts"]:
            if post["id"] == post_id:
                reactions = post.setdefault("reactions", {})
                if emoji not in reactions:
                    reactions[emoji] = []
                if username in reactions[emoji]:
                    reactions[emoji].remove(username)
                    if not reactions[emoji]:
                        del reactions[emoji]
                else:
                    reactions[emoji].append(username)
                self.save_data()
                break
    
    def comment_post(self, post_id: int, username: str, comment: str):
        """Comment on a post"""
        for post in self.data["posts"]:
            if post["id"] == post_id:
                post["comments"].append({
                    "user": username,
                    "comment": comment,
                    "time": str(datetime.now()),
                    "replies": [],
                    "reactions": {}
                })
                self.save_data()
                break
    
    def reply_to_comment(self, post_id: int, comment_index: int, username: str, reply: str):
        """Reply to a comment"""
        for post in self.data["posts"]:
            if post["id"] == post_id:
                if comment_index < len(post["comments"]):
                    post["comments"][comment_index]["replies"].append({
                        "user": username,
                        "reply": reply,
                        "time": str(datetime.now()),
                        "reactions": {}
                    })
                    self.save_data()
                break
    
    def react_to_comment(self, post_id: int, comment_index: int, username: str, emoji: str):
        """React to a comment"""
        for post in self.data["posts"]:
            if post["id"] == post_id:
                if comment_index < len(post["comments"]):
                    reactions = post["comments"][comment_index].setdefault("reactions", {})
                    if emoji not in reactions:
                        reactions[emoji] = []
                    if username in reactions[emoji]:
                        reactions[emoji].remove(username)
                        if not reactions[emoji]:
                            del reactions[emoji]
                    else:
                        reactions[emoji].append(username)
                    self.save_data()
                break
    
    def get_posts(self, filter_type: str = "all") -> List[Dict]:
        """Get posts with optional filters"""
        posts = self.data["posts"][::-1]
        
        if filter_type == "all":
            return posts
        return [p for p in posts if p.get("type") == filter_type]
    
    # ==================== HELP OPERATIONS ====================
    def create_help_request(self, username: str, subject: str, question: str, 
                           exam: str, urgency: str = "normal") -> bool:
        """Create a help request"""
        user = self.get_user(username)
        help_req = {
            "id": len(self.data["helps"]) + 1,
            "user": username,
            "user_name": user.get("name", username),
            "user_exam": user.get("exam", ""),
            "subject": subject,
            "question": question,
            "exam": exam,
            "urgency": urgency,
            "time": str(datetime.now()),
            "answers": [],
            "status": "open"
        }
        self.data["helps"].append(help_req)
        self.save_data()
        return True
    
    def answer_help(self, help_id: int, username: str, answer: str):
        """Answer a help request"""
        for h in self.data["helps"]:
            if h["id"] == help_id:
                h["answers"].append({
                    "user": username,
                    "user_name": self.get_user(username).get("name", username),
                    "answer": answer,
                    "time": str(datetime.now()),
                    "upvotes": [],
                    "downvotes": [],
                    "comments": []  # comments on this answer
                })
                # Award points for helping
                if username in self.data["users"]:
                    self.data["users"][username]["points"] += 3
                self.save_data()
                break
    
    def get_help_requests(self, subject: str = "all", exam: str = "all") -> List[Dict]:
        """Get help requests with filters
        The UI sends human-readable values like "All" so we normalize the
        inputs for comparison. Both filters are case-insensitive and treat
        the word "all" as meaning no filtering. This prevents the default
        "All" option from accidentally excluding everything.
        """
        helps = self.data["helps"][::-1]
        
        # normalize so that "All" or "all" both get treated as no filter
        if subject and subject.lower() != "all":
            helps = [h for h in helps if h.get("subject") == subject]
        if exam and exam.lower() != "all":
            helps = [h for h in helps if h.get("exam") == exam]
        
        return helps
    
    def upvote_answer(self, help_id: int, answer_index: int, username: str):
        """Toggle upvote on an answer"""
        for h in self.data.get("helps", []):
            if h.get("id") == help_id:
                ans = h.get("answers", [])[answer_index]
                if username in ans.get("upvotes", []):
                    ans["upvotes"].remove(username)
                else:
                    ans["upvotes"].append(username)
                    # remove downvote if present
                    if username in ans.get("downvotes", []):
                        ans["downvotes"].remove(username)
                self.save_data()
                return

    def downvote_answer(self, help_id: int, answer_index: int, username: str):
        """Toggle downvote on an answer"""
        for h in self.data.get("helps", []):
            if h.get("id") == help_id:
                ans = h.get("answers", [])[answer_index]
                if username in ans.get("downvotes", []):
                    ans["downvotes"].remove(username)
                else:
                    ans["downvotes"].append(username)
                    if username in ans.get("upvotes", []):
                        ans["upvotes"].remove(username)
                self.save_data()
                return

    # ==================== MENTOR OPERATIONS ====================
    def register_mentor(self, username: str, subject: str, experience: str, 
                       availability: str = "weekends") -> bool:
        """Register as a mentor"""
        user = self.get_user(username)
        mentor = {
            "id": len(self.data["mentors"]) + 1,
            "user": username,
            "name": user.get("name", username),
            "subject": subject,
            "experience": experience,
            "availability": availability,
            "exam": user.get("exam", ""),
            "country": user.get("country", ""),
            "rating": 5.0,
            "students_helped": 0,
            "time": str(datetime.now())
        }
        self.data["mentors"].append(mentor)
        
        # Add badge
        if "mentor" not in self.data["users"][username].get("badges", []):
            self.data["users"][username]["badges"].append("mentor")
        
        self.save_data()
        return True
    
    def get_mentors(self, subject: str = "all", exam: str = "all") -> List[Dict]:
        """Get mentors with filters
        See get_help_requests for rationale: UI sends "All" and we want
        to treat that as no filter. Comparison is case‑insensitive.
        """
        mentors = self.data["mentors"][::-1]
        
        if subject and subject.lower() != "all":
            mentors = [m for m in mentors if m.get("subject") == subject]
        if exam and exam.lower() != "all":
            mentors = [m for m in mentors if m.get("exam") == exam]
        
        return mentors

    # ==================== CHAT OPERATIONS ====================
    def _find_chat(self, users: List[str]) -> Dict:
        """Return an existing chat that contains exactly the given users.
        The list order is ignored (chats between the same pair are unique).
        """
        user_set = set(users)
        for c in self.data.get("chats", []):
            if set(c.get("users", [])) == user_set:
                return c
        return {}

    def create_chat(self, user1: str, user2: str) -> int:
        """Create a chat between two users, or return existing chat id."""
        if user1 == user2:
            raise ValueError("cannot create chat with self")
        existing = self._find_chat([user1, user2])
        if existing:
            return existing["id"]

        # ensure the two users are marked as connected
        self.add_connection(user1, user2)

        chat = {
            "id": len(self.data.get("chats", [])) + 1,
            "users": [user1, user2],
            "messages": []
        }
        self.data.setdefault("chats", []).append(chat)
        self.save_data()
        return chat["id"]

    def get_chats_for_user(self, username: str) -> List[Dict]:
        """Return a list of chat objects that include `username`."""
        return [c for c in self.data.get("chats", []) if username in c.get("users", [])]

    def send_message(self, chat_id: int, username: str, text: str):
        """Add a message to a chat. Creates chat if necessary (should already exist)."""
        for c in self.data.get("chats", []):
            if c.get("id") == chat_id:
                c.setdefault("messages", []).append({
                    "user": username,
                    "text": text,
                    "time": str(datetime.now())
                })
                self.save_data()
                return
        # if we reach here the chat was missing; ignore or raise
        raise KeyError(f"Chat with id {chat_id} not found")
    
    # ==================== STATISTICS ====================
    def get_stats(self) -> Dict:
        """Get platform statistics"""
        return {
            "total_users": len(self.data["users"]),
            "total_posts": len(self.data["posts"]),
            "total_helps": len(self.data["helps"]),
            "total_mentors": len(self.data["mentors"]),
            "countries": len(set(u.get("country", "") for u in self.data["users"].values())),
            "exams": len(set(u.get("exam", "") for u in self.data["users"].values()))
        }