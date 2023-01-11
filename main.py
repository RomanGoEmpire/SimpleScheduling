import doctest

from Parser.task_parser import TaskParser
from scheduling_z3 import solve


def schedule(path):
    """
    >>> schedule("Examples/simplest")
    Task: begin 0 end 1
    [('Task', 0, 1)]

    >>> schedule("Examples/standard")
    Task1: begin 3 end 5
    Task2: begin 0 end 1
    Task3: begin 1 end 4
    Task4: begin 0 end 3
    Task5: begin 0 end 3
    [('Task1', 3, 5), ('Task2', 0, 1), ('Task3', 1, 4), ('Task4', 0, 3), ('Task5', 0, 3)]

    >>> schedule("Examples/vicious")
    Unsolvable!

    >>> schedule("Examples/parse_fail_name")
    Parsing failed, because of:
     Expected TokenType.TAKES
    Got TokenType.NUMBER
    """

    # initialize the Parser
    task_parser = TaskParser(path)
    task_list = None
    # get the Tasklist
    try:
        task_list = task_parser.get_task_list()
    except Exception as e:
        print("Parsing failed, because of:\n " + str(e))
    # if parsing was successful execute z3
    if task_list:
        answer = solve(task_list)
        # if solving was successful
        if answer:
            for task in answer:
                print(f"{task[0]}: begin {task[1]} end {task[2]}")
            print(answer)
        else:
            print("Unsolvable!")


if __name__ == "__main__":
    doctest.testmod()

    # TODO: EDIT THIS FILE TO GET YOUR SCHEDULING
    # schedule("Examples/scheduling_problem")

    # simplest example
    # schedule("Examples/simplest")

    # vicious example
    # schedule("Examples/vicious")

    # standard example
    schedule("Examples/standard")
