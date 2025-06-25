class SchedulerModel:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def get_tasks(self):
        return self.tasks

    def get_task_by_status(self, status):
        return [task for task in self.tasks if task.status == status]

    def update_task(self, task, new_name=None, new_status=None, new_estimated_time=None):
        if new_name is not None:
            task.name = new_name
        if new_status is not None:
            task.status = new_status
        if new_estimated_time is not None:
            task.estimated_time = new_estimated_time