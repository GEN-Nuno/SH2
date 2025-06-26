import os
import json
import datetime
from .task_model import Task
from patterns.observer import Subject

class ScheduleModel(Subject):
    """Model representing the schedule containing tasks"""
    
    def __init__(self):
        Subject.__init__(self)
        self.tasks = []
        self.tags = ["Work", "Personal", "Meeting", "Development", "Documentation"]
        self.load_tasks()
        self.load_tags()
    
    def add_task(self, task):
        """Add a new task to the schedule"""
        self.tasks.append(task)
        self.notify()
    
    def delete_task(self, task):
        """Remove a task from the schedule"""
        if task in self.tasks:
            self.tasks.remove(task)
            self.notify()
    
    def delete_closed_tasks(self):
        """Delete all tasks with 'closed' status"""
        self.tasks = [task for task in self.tasks if task.status != "closed"]
        self.notify()
    
    def get_today_tasks(self, include_exceptions=False):
        """Get tasks for today"""
        today = datetime.datetime.now().strftime("%A")
        if include_exceptions:
            return self.tasks
        else:
            return [task for task in self.tasks if today in task.days or "Free" in task.days]
    
    def add_tag(self, tag):
        """Add a new tag"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.save_tags()
            self.notify()
    
    def delete_tag(self, tag):
        """Remove a tag"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.save_tags()
            self.notify()
    
    def save_tasks(self):
        """Save tasks to configuration file"""
        data = [task.to_dict() for task in self.tasks]
        os.makedirs(os.path.dirname("c:\\SH\\task_Lists.conf"), exist_ok=True)
        with open("c:\\SH\\task_Lists.conf", "w") as file:
            json.dump(data, file, indent=4)
        return True
    
    def load_tasks(self):
        """Load tasks from configuration file"""
        try:
            if os.path.exists("c:\\SH\\task_Lists.conf"):
                with open("c:\\SH\\task_Lists.conf", "r") as file:
                    data = json.load(file)
                    self.tasks = [Task.from_dict(task_dict) for task_dict in data]
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []
    
    def save_tags(self):
        """Save tags to configuration file"""
        os.makedirs(os.path.dirname("c:\\SH\\tags.conf"), exist_ok=True)
        with open("c:\\SH\\tags.conf", "w") as file:
            json.dump(self.tags, file, indent=4)
        return True
    
    def load_tags(self):
        """Load tags from configuration file"""
        try:
            if os.path.exists("c:\\SH\\tags.conf"):
                with open("c:\\SH\\tags.conf", "r") as file:
                    self.tags = json.load(file)
        except Exception as e:
            print(f"Error loading tags: {e}")
            # デフォルトタグを使用
    
    def save_work_time(self, calculated_tasks):
        """Save calculated work time to configuration file"""
        # Use full ISO format to include date and time
        today_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "date": today_date,
            "tasks": [
                {
                    "name": task.name,
                    "tags": task.tags,
                    "work_time": task.calculated_work_time,
                    "perceived_effort": task.perceived_effort
                }
                for task in calculated_tasks
            ]
        }
        
        # Load existing data if file exists
        all_data = []
        if os.path.exists("c:\\SH\\work_time.conf"):
            try:
                with open("c:\\SH\\work_time.conf", "r") as file:
                    all_data = json.load(file)
            except:
                all_data = []
        
        # Append new data
        if not isinstance(all_data, list):
            all_data = []
        all_data.append(data)
        
        # Save back to file
        os.makedirs(os.path.dirname("c:\\SH\\work_time.conf"), exist_ok=True)
        with open("c:\\SH\\work_time.conf", "w") as file:
            json.dump(all_data, file, indent=4)
        
        return True
