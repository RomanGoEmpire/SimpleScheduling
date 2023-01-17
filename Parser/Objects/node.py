class Node:
    def __str__(self):
        pass


# A TaskNode is a node which contains the name of the task.
class TaskNode(Node):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


# An OperatorNode contains the operation and a left and right child which can be other OperatorNodes or TaskNodes.
class OperatorNode(Node):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def get_operator(self):
        return self.operator

    def set_left(self, left):
        self.left = left

    def get_left(self):
        return self.left

    def set_right(self, right):
        self.right = right

    def get_right(self):
        return self.right

    def __str__(self):
        return f"{self.operator}({self.left},{self.right})"
