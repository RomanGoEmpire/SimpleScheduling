from Parser.task_parser import TaskParser
from scheduling_z3 import solve


def schedule(path):
    task_parser = TaskParser(path)
    task_list = task_parser.get_task_list()
    for task in task_list:
        print(task)
    if task_list:
        answer = solve(task_list)
        print(answer)


if __name__ == "__main__":

    # change the content of this file
    #schedule("Examples/scheduling_problem.txt")

    # simplest example
    # schedule("Examples/simplest.txt")

    # vicious example
    # schedule("Examples/vicious.txt")

    # standard example
    schedule("Examples/standard.txt")
