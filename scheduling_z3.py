from z3 import *

from Parser.node import TaskNode

def solve(tasks):


    # Create integer variables to represent the start, the end times of each task and how much it takes
    starts = {task.name: Int(f"{task.name}_start") for task in tasks}
    ends = {task.name: Int(f"{task.name}_end") for task in tasks}
    takes = {task.name: Int(f"{task.name}_takes") for task in tasks}
    # Create a solver instance
    solver = Solver()

    # Constraints:
    # 1- Every task must be given a duration: the number of steps it needs to complete.
    # 2- A duration is specified by the keyword takes followed by a natural number (which should be greater than zero).
    # 3- If a task takes n steps and starts at step s, then it must finish at step s + n.
    for task in tasks:
        solver.add(takes[task.name] == task.duration)
        solver.add(starts[task.name] >= 0)
        solver.add(ends[task.name] == starts[task.name] + task.duration)

    # dependencies
    def c_dep(node,name):
        if type(node) is TaskNode:
            if node.name == "none":
                return
            return starts[name] >= ends[node.name]
        if node.operator == "And":
            return And(c_dep(node.left,name),c_dep(node.right,name))
        if node.operator == "Or":
            return Or(c_dep(node.left,name),c_dep(node.right,name))


    for task in tasks:
        dep = c_dep(task.dependencies,task.name)
        if dep is None:
            continue
        solver.add(dep)


    triple = []
    if solver.check() == sat:
        print(solver)
        model = solver.model()
        for task in tasks:
            triple.append((task.name, model[Int(f'{task.name}_start')], model[Int(f'{task.name}_end')]))
        return triple

    return "Unsolvable!"
