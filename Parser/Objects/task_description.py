# A Task description has a name and a duration and the root node of the Tree
import string

from Parser.Objects.node import Node


class Task:
    def __init__(self, name: string, duration: int, dependencies: Node):
        self.name = name
        self.duration = duration
        self.dependencies = dependencies

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Duration: {self.duration}\n" \
               f"Dependencies: {self.dependencies}\n"
