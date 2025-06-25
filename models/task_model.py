import json
from datetime import datetime

class Task:
    """Model representing a task in the scheduler"""
    
    STATUS_OPTIONS = ["working", "planned", "closed"]
    DAYS_OPTIONS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Free"]
    
    def __init__(self, name="", status="planned", days=None, details="", tags=None, 
                 completed_today=False, perceived_effort=0):
        self.name = name
        self.status = status if status in self.STATUS_OPTIONS else "planned"
        self.days = days if days else ["Free"]
        self.details = details
        self.tags = tags if tags else []
        self.completed_today = completed_today
        self.perceived_effort = perceived_effort
        self.calculated_work_time = 0
    
    def is_for_today(self, include_free=True):
        """Check if task is scheduled for today"""
        today = datetime.now().strftime("%A")
        if today in self.days:
            return True
        return include_free and "Free" in self.days
    
    def to_dict(self):
        """Convert task to dictionary for serialization"""
        return {
            "name": self.name,
            "status": self.status,
            "days": self.days,
            "details": self.details,
            "tags": self.tags,
            "completed_today": self.completed_today,
            "perceived_effort": self.perceived_effort
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create task from dictionary"""
        return cls(
            name=data.get("name", ""),
            status=data.get("status", "planned"),
            days=data.get("days", ["Free"]),
            details=data.get("details", ""),
            tags=data.get("tags", []),
            completed_today=data.get("completed_today", False),
            perceived_effort=data.get("perceived_effort", 0)
        )
