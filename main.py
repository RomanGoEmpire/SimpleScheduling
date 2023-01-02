from Parser.task_parser import TaskParser

if __name__ == "__main__":
    t = TaskParser("Examples/scheduling_problem.txt")
    list = t.get_task_list()
    for task in list:
        print(task)
