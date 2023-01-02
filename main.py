from Parser.task_description import TaskDescription

if __name__ == "__main__":
    t = TaskDescription("../Examples/scheduling_problem.txt")
    list = t.get_task_list()
    for task in list:
        print(task)
