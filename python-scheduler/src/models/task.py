class Task:
    def __init__(self, name, status='planned', estimated_time=0):
        self.name = name
        self.status = status
        self.estimated_time = estimated_time

    def update_status(self, new_status):
        self.status = new_status

    def set_estimated_time(self, time):
        self.estimated_time = time

    def __repr__(self):
        return f"Task(name={self.name}, status={self.status}, estimated_time={self.estimated_time})"