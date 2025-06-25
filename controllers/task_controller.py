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
        detail_view.exec_()
        return True
