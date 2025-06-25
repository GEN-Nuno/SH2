class ScheduleController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)

    def load_schedules(self):
        schedules = self.model.get_schedules()
        self.view.display_schedules(schedules)

    def add_schedule(self, schedule_data):
        self.model.add_schedule(schedule_data)
        self.load_schedules()

    def update_schedule(self, schedule_id, updated_data):
        self.model.update_schedule(schedule_id, updated_data)
        self.load_schedules()

    def delete_schedule(self, schedule_id):
        self.model.delete_schedule(schedule_id)
        self.load_schedules()