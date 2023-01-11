from z3 import *

from Parser.Objects.node import TaskNode


def solve(tasks):
    # Create integer variables to represent the start, the end times of each task and a list of the end times
    starts = {task.name: Int(f"{task.name}_start") for task in tasks}
    ends = {task.name: Int(f"{task.name}_end") for task in tasks}
    duration = [Int(f"{task.name}_end") for task in tasks]

    # Create a solver instance
    solver = Optimize()

    # Constraints:
    # 1- Start should be greater than zero
    # 2- If a task takes n steps and starts at step s, then it must finish at step s + n.
    for task in tasks:
        solver.add(starts[task.name] >= 0)
        solver.add(ends[task.name] == starts[task.name] + task.duration)

    # recursive function to get the dependencies of a task
    def convert_tree_to_z3_expression(node, name):
        if type(node) is TaskNode:
            if node.name == "none":
                return
            return starts[name] >= ends[node.name]
        if node.operator == "And":
            return And(convert_tree_to_z3_expression(node.left, name), convert_tree_to_z3_expression(node.right, name))
        if node.operator == "Or":
            return Or(convert_tree_to_z3_expression(node.left, name), convert_tree_to_z3_expression(node.right, name))

    # 3 - If a task depends on another task it can not start before the other task ends
    for task in tasks:
        dep = convert_tree_to_z3_expression(task.dependencies, task.name)
        if dep is None:
            continue
        solver.add(dep)

    # minimize the sum of the end times of all tasks
    solver.minimize(sum(duration))

    triple = []
    if solver.check() == sat:
        model = solver.model()
        for task in tasks:
            triple.append((task.name, model[Int(f'{task.name}_start')], model[Int(f'{task.name}_end')]))
        return triple
    else:
        return None
