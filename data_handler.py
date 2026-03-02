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
            return {
                "users": {},
                "posts": [],
                "helps": [],
                "mentors": [],
                "connections": [],
                "study_rooms": []
            }
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {
                "users": {},
                "posts": [],
                "helps": [],
                "mentors": [],
                "connections": [],
                "study_rooms": []
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
            "comments": []
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
                self.save_data()
                break
    
    def comment_post(self, post_id: int, username: str, comment: str):
        """Comment on a post"""
        for post in self.data["posts"]:
            if post["id"] == post_id:
                post["comments"].append({
                    "user": username,
                    "comment": comment,
                    "time": str(datetime.now())
                })
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
                    "upvotes": []
                })
                # Award points for helping
                if username in self.data["users"]:
                    self.data["users"][username]["points"] += 3
                self.save_data()
                break
    
    def get_help_requests(self, subject: str = "all", exam: str = "all") -> List[Dict]:
        """Get help requests with filters"""
        helps = self.data["helps"][::-1]
        
        if subject != "all":
            helps = [h for h in helps if h.get("subject") == subject]
        if exam != "all":
            helps = [h for h in helps if h.get("exam") == exam]
        
        return helps
    
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
        """Get mentors with filters"""
        mentors = self.data["mentors"][::-1]
        
        if subject != "all":
            mentors = [m for m in mentors if m.get("subject") == subject]
        if exam != "all":
            mentors = [m for m in mentors if m.get("exam") == exam]
        
        return mentors
    
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