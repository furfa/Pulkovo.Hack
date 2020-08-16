from entity_classes import *
from entity_getters import *
from datetime import datetime
import pandas as pd


class Schedule_item:
    
    def __init__(self, time:Time, task:Task, teacher:Teacher, audience:Audience):
        self.time = time
        self.task = task
        self.teacher = teacher
        self.audience = audience

    def __str__(self):
        s  = "{}({}) проводит занятие {} {}({}) c {} по {} в {} аудитории"
        return s.format(
            self.teacher.name, 
            self.teacher.id, 
            self.task.discipline, 
            self.task.programm, 
            self.task.id, 
            self.time.start, 
            self.time.end, 
            self.audience.id
        )


class Schedule:

    data = list()

    def __init__(self, *args, **kwargs):
        pass


    def append(self, *args ,**kwargs):
        self.data.append( Schedule_item(*args, **kwargs) )

    def print(self):
        self.sort()
        print(self.to_dataframe())

    def sort(self):
        self.data.sort(key=lambda x:x.time.start)

    def to_dataframe(self):
        to_df = list()
        columns = [
            "teacher.name", 
            "teacher.id", 
            "task.discipline", 
            "task.programm", 
            "task.id", 
            "time.start", 
            "time.end", 
            "audience.id"
        ]
        for row in self.data:
            to_df.append([
                row.teacher.name, 
                row.teacher.id, 
                row.task.discipline, 
                row.task.programm, 
                row.task.id, 
                row.time.start, 
                row.time.end, 
                row.audience.id
            ])
        return pd.DataFrame(to_df, columns=columns)

        

if __name__ == "__main__":
    s = Schedule()

    TIME = get_times()[0]
    TASK = get_tasks()[0]
    TEACHER = get_teachers()[0]
    AUDIENCE = get_audiences()[0]

    s.append(TIME, TASK, TEACHER, AUDIENCE)

    s.print()
    