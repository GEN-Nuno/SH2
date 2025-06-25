class MainController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)

    def run(self):
        self.view.show()

    def add_task(self, task_name, status, estimated_time):
        task = self.model.add_task(task_name, status, estimated_time)
        self.view.update_task_list(self.model.get_tasks())

    def edit_task(self, task_id, new_name, new_status, new_estimated_time):
        self.model.edit_task(task_id, new_name, new_status, new_estimated_time)
        self.view.update_task_list(self.model.get_tasks())

    def delete_task(self, task_id):
        self.model.delete_task(task_id)
        self.view.update_task_list(self.model.get_tasks())

    def calculate_work_time(self):
        work_time = self.model.calculate_work_time()
        self.view.show_work_time(work_time)