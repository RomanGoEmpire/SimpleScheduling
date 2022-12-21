import Parser

parsed_tasks = []

# List of inputs to test the parser
inputs = [
    "Task1 takes 1 needs none",
    "Task2 takes 2 needs Task1 and Task3 or Task4",
    "Task3 takes 3 needs Task2",
    "Task4 takes 2 needs Task2 or Task1",
]

for input_str in inputs:
    task = Parser.ParseTask().parse(input_str)
    if task is not None:
        parsed_tasks.append(task)
    else:
        print(f"Unable to parse input: {input_str}")

for task in parsed_tasks:
    print(task)
