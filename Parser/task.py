class Task:
    def __init__(self,name,duration,dependencies):
        self.name = name
        self.duration = duration
        self.dependencies = dependencies

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Duration: {self.duration}\n" \
               f"Dependencies: {self.dependencies}\n"

