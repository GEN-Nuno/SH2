from patterns.command import Command
from patterns.strategy import TaskFilterStrategy, TodayTasksFilter
from models.task_model import Task
from patterns.state import StateContext
from PyQt5.QtWidgets import QMessageBox

class TaskController:
    """Controller for task-related operations"""
    
    def __init__(self, model):
        self.model = model
        self.current_filter_strategy = TodayTasksFilter()
    
    def set_filter_strategy(self, strategy):
        """Set the strategy for filtering tasks"""
        if not isinstance(strategy, TaskFilterStrategy):
            raise TypeError("Strategy must be a TaskFilterStrategy")
        
        self.current_filter_strategy = strategy
    
    def get_filtered_tasks(self):
        """Get tasks filtered by the current strategy"""
        return self.current_filter_strategy.filter(self.model.tasks)
    
    def add_task(self, task):
        """Add a new task to the model"""
        self.model.add_task(task)
    
    def delete_task(self, task):
        """Remove a task from the model"""
        self.model.delete_task(task)
    
    def delete_closed_tasks(self):
        """Delete all closed tasks from the model"""
        self.model.delete_closed_tasks()
    
    def update_task(self, task, attributes):
        """Update task attributes"""
        for key, value in attributes.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        # Handle state transitions if status changes
        if 'status' in attributes:
            # Update display properties based on new state
            state = StateContext.get_state_for_status(task.status)
            properties = state.get_display_properties()
            # The properties could be used to update UI elements
        
        self.model.notify()
        return True
    
    def save_tasks(self):
        """Save all tasks to configuration file"""
        self.model.save_tasks()
        return True
    
    def add_tag(self, tag):
        """Add a new tag"""
        self.model.add_tag(tag)
        self.model.save_tags()
    
    def delete_tag(self, tag):
        """Delete a tag"""
        self.model.delete_tag(tag)
        self.model.save_tags()
    
    def create_new_task(self, name="", status="planned", days=None, details="", tags=None):
        """Create a new task with the given attributes"""
        return Task(name=name, status=status, days=days if days else ["Free"], 
                    details=details, tags=tags if tags else [])
    
    def show_task_detail_view(self, task, parent=None):
        """Show a detail view for the given task"""
        from views.task_detail_view import TaskDetailView
        from views.builders.theme_factory import LightThemeFactory
        
        theme_factory = LightThemeFactory()
        detail_view = TaskDetailView(theme_factory, task, self)
        result = detail_view.exec_()
        
        # If the dialog was accepted, notify model observers
        if result == detail_view.Accepted:
            self.model.notify()
        
        return True

    def get_today_tasks(self, include_free=False):
        """Get tasks for today, with option to include Free tasks"""
        return self.model.get_today_tasks(include_free=include_free)
    
    def save_today_tasks(self, tasks):
        """Save today's tasks to configuration file"""
        result = self.model.save_today_tasks(tasks)
        if result:
            # Also save to regular tasks file for consistency
            self.save_tasks()
        return result
    
    def get_all_tasks(self):
        """Get all tasks from the model"""
        return self.model.tasks.copy()
    
    def get_all_tags(self):
        """Get all tags from the model"""
        return self.model.tags.copy()
    
    def refresh_all_schedule_view(self, view):
        """Refresh the all schedule view with current model data"""
        if view:
            view.refresh_view(self.get_all_tasks(), self.get_all_tags())
    
    def refresh_today_task_view(self, view):
        """Refresh the today task view with current model data"""
        if view:
            # Only get tasks for today
            today_tasks = self.model.get_today_tasks(include_free=False)
            view.set_tasks(today_tasks)
            view.set_tags(self.get_all_tags())
