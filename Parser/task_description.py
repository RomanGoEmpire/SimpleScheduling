class Task:
    def __init__(self,name,duration,dependencies):
        self.name = name
        self.duration = duration
        self.dependencies = dependencies

    def get_name(self):
        return self.name

    def get_duration(self):
        return self.duration

    def get_dependencies(self):
        return self.dependencies

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Duration: {self.duration}\n" \
               f"Dependencies: {self.dependencies}\n"

