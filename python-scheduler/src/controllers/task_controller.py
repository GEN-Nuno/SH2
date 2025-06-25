from models.task import Task
from models.scheduler_model import SchedulerModel

class TaskController:
    def __init__(self):
        self.scheduler_model = SchedulerModel()

    def add_task(self, name, status, estimated_time):
        task = Task(name=name, status=status, estimated_time=estimated_time)
        self.scheduler_model.add_task(task)

    def remove_task(self, task_id):
        self.scheduler_model.remove_task(task_id)

    def update_task(self, task_id, name=None, status=None, estimated_time=None):
        task = self.scheduler_model.get_task(task_id)
        if task:
            if name is not None:
                task.name = name
            if status is not None:
                task.status = status
            if estimated_time is not None:
                task.estimated_time = estimated_time

    def get_all_tasks(self):
        return self.scheduler_model.get_all_tasks()

    def get_task(self, task_id):
        return self.scheduler_model.get_task(task_id)