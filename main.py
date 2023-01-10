from Parser.task_parser import TaskParser
from scheduling_z3 import solve

def schedule(path):
    task_parser = TaskParser(path)
    task_list = task_parser.get_task_list()
    answer = solve(task_list)
    print(answer)


if __name__ == "__main__":
    schedule("Examples/scheduling_problem.txt")
    #simple example



