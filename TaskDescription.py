class TaskDescription:
    def __init__(self, name: str, duration: int, dependencies: str):
        self.name = name
        self.duration = duration
        self.dependencies = dependencies

    def __str__(self) -> str:
        return f'{self.name} takes {self.duration} needs {self.dependencies}'


task = TaskDescription("Task1", 5, "none")
print(task)
