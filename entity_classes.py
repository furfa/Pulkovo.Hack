from datetime import datetime



class Task:
    def __init__(self, id, discipline, programm, is_practice, prev_id=None):
        """
        Все таски идут 1 академический час,
        если одна больше часа, то раздить на несколько
        И указать приоритет выполнения.
        """
        self.id = id
        self.prev_id = prev_id # id предыдущего урока
        self.discipline = discipline
        self.programm = programm
        self.is_practice = is_practice

class Teacher:
    def __init__(self, id, allowed_tasks, allowed_times,name):
        self.id = id
        self.allowed_tasks = set(allowed_tasks) # Set из (task_id:int, приоритет:int ) 
        self.allowed_times = set(allowed_times)
        # self.grapic = [] # График работы
        self.name = name

    def check_task(self, task):
        for i in self.allowed_tasks:
            if i[0] == task:
                return i[1]
        return None

class Time:
    def __init__(self, id, 
                    start = datetime(2020, 9, 1, 8, 0, 0),
                    end   = datetime(2020, 9, 1, 9, 30, 0) ):
        self.id = id
        self.start = start
        self.end = end


class Audience:
    def __init__(self, id, tasks_allowed):
        self.id = id
        self.tasks_allowed = set(tasks_allowed)