from z3 import *


def get_start_times(tasks):
    return [Int(f'start_{task[0]}') for task in tasks]


def get_end_times(tasks):
    return [Int(f'end_{task[0]}') for task in tasks]


def get_durations(tasks):
    return [Int(f'duration_{task[0]}') for task in tasks]


def get_task_indices(tasks):
    return {task[0]: i for i, task in enumerate(tasks)}


def get_start_time_constraints(start_times):
    return [start_time >= 0 for start_time in start_times]


def get_end_time_constraints(start_times, end_times, durations):
    return [end_time == start_time + duration
            for start_time, end_time, duration in zip(start_times, end_times, durations)]


def get_dependency_constraints(tasks, start_times, end_times, task_indices):
    dependency_constraints = []
    for task, start_time in zip(tasks, start_times):
        if task[2] is None:
            continue
        else:
            dependencies = task[2].split()
            if 'and' in dependencies:
                dependencies.remove('and')
            dependencies_completed = [end_times[task_indices[dependency]] <= start_time
                                      for dependency in dependencies if dependency in task_indices]
            dependency_constraints.append(And(dependencies_completed))
    return dependency_constraints

def get_overlap_constraints(tasks, start_times, end_times):
    overlap_constraints = []
    for i in range(len(tasks)):
        for j in range(i + 1, len(tasks)):
            overlap_constraints.append(Or(end_times[i] <= start_times[j], end_times[j] <= start_times[i]))
    return overlap_constraints


def get_duration_constraints(tasks, durations):
    return [duration == task[1] for task, duration in zip(tasks, durations)]


def schedule_tasks(tasks):
    start_times = get_start_times(tasks)
    end_times = get_end_times(tasks)
    durations = get_durations(tasks)
    task_indices = get_task_indices(tasks)
    start_time_constraints = get_start_time_constraints(start_times)
    end_time_constraints = get_end_time_constraints(start_times, end_times, durations)
    dependency_constraints = get_dependency_constraints(tasks, start_times, end_times, task_indices)
    overlap_constraints = get_overlap_constraints(tasks, start_times, end_times)
    duration_constraints = get_duration_constraints(tasks, durations)

    solver = Optimize()
    constrains = (start_time_constraints + end_time_constraints + duration_constraints +
                  dependency_constraints + overlap_constraints)
    solver.add(constrains)
    solver.minimize(Sum(durations))

    if solver.check() == sat:
        model = solver.model()
        output = []
        for task, start_time, end_time in zip(tasks, start_times, end_times):
            output.append((task[0], model[start_time].as_long(), model[end_time].as_long()))
        return output
    else:
        return "Wrong"


# tasks = [('Task1', 3, None), ('Task2', 2, 'Task1'), ('Task3', 4, 'Task1 and Task2'), ('Task4', 1, 'Task3')]
# tasks = [('Task1', 3, None), ('Task2', 2, 'Task1'), ('Task3', 4, 'Task1 and Task2'), ('Task4', 1, 'Task3'),
#          ('Task5', 5, 'Task4'), ('Task6', 2, 'Task5'), ('Task7', 3, 'Task5'), ('Task8', 1, 'Task6 and Task7'),
#          ('Task9', 2, 'Task8'), ('Task10', 4, 'Task9')]
# tasks = [('Task1', 5, None), ('Task2', 4, 'Task1'), ('Task3', 6, 'Task1 and Task2'), ('Task4', 3, 'Task3'),
#          ('Task5', 7, 'Task4'), ('Task6', 5, 'Task5 and Task3'), ('Task7', 6, 'Task5'), ('Task8', 4, 'Task6 and Task7'),
#          ('Task9', 3, 'Task8'), ('Task10', 5, 'Task9 and Task5 and Task1')]
# tasks = [('Task1', 5, 'Task4 and Task7'),
#          ('Task2', 4, 'Task5 and Task8'),
#          ('Task3', 6, 'Task6 and Task9'),
#          ('Task4', 3, 'Task10'),
#          ('Task5', 7, 'Task10'),
#          ('Task6', 5, 'Task10'),
#          ('Task7', 6, 'Task10'),
#          ('Task8', 4, 'Task10'),
#          ('Task9', 3, 'Task10'),
#          ('Task10', 5, None)]
tasks = [('Task1', 3, None), ('Task2', 2, 'Task1'), ('Task3', 4, 'Task1 and Task2'), ('Task4', 1, 'Task3')]



result = schedule_tasks(tasks)
print(result)
