from ortools.sat.python import cp_model
import collections

from datetime import datetime
from pprint import pprint
import json

from entity_classes import *
from entity_getters import *

from schedule_class import Schedule


"""
 TODO: Одна таска может иметь несколько подрядидущих времен, если она не входит в одно

"""

class PulkovoPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._solution_count = 0
        self._solutions = sols


    def on_solution_callback(self):
        if self._solution_count in self._solutions:

            print('Solution %i' % self._solution_count)
            
        self._solution_count += 1

    def solution_count(self):
        return self._solution_count

def main():
    
    Tasks = get_tasks()         # :list()
    Teachers = get_teachers()   # :list()
    Audiences = get_audiences() # :list()
    Times = get_times()         # :list()

    # Create the model.
    model = cp_model.CpModel()
    
    schedule = {}
    
    for time_id, time in enumerate(Times):
        for audience_id, audience in enumerate(Audiences):
            for task_id, task in enumerate(Tasks):
                for teacher_id, teacher in enumerate(Teachers):
                    suffix = f'{time_id=}{audience_id=}{task_id=}{teacher_id=}'
                    schedule[time_id, audience_id, task_id, teacher_id] = model.NewBoolVar(suffix)
    
    for task_id, task in enumerate(Tasks):
        tasks_presence = []
        for time_id, time in enumerate(Times):
            for audience_id, audience in enumerate(Audiences): 
                for teacher_id, teacher in enumerate(Teachers):
                    tasks_presence.append(schedule[time_id, audience_id, task_id, teacher_id])
        model.Add(sum(tasks_presence) == 1) # Каждый урок должен идти ровно 1 раз
    
    
        
    for time_id, time in enumerate(Times):
        for audience_id, audience in enumerate(Audiences):
            for task_id, task in enumerate(Tasks):
                teacher_presence = []
                for teacher_id, teacher in enumerate(Teachers):
                    teacher_presence.append(schedule[time_id, audience_id, task_id, teacher_id])
                model.Add(sum(tasks_presence) <= 1) # В каждый момент времени, в каждом кабинете находится не более одного учителя

    for time_id, time in enumerate(Times):
        for audience_id, audience in enumerate(Audiences):
            teacher_presence = []
            for task_id, task in enumerate(Tasks):
                for teacher_id, teacher in enumerate(Teachers):
                    teacher_presence.append(schedule[time_id, audience_id, task_id, teacher_id])
            model.Add(sum(teacher_presence) <= 1) # Каждый учитель в любой момент времени в любой аудитории ведёт только 1 урок

    for teacher_id, teacher in enumerate(Teachers):
        for time_id, time in enumerate(Times):
            teacher_presence = []
            for audience_id, audience in enumerate(Audiences):
                for task_id, task in enumerate(Tasks):
                    teacher_presence.append(schedule[time_id, audience_id, task_id, teacher_id])
            model.Add(sum(teacher_presence) <= 1) # Каждый учитель в каждый момент времени ведёт в одной аудитории (или не ведёт вообще)
    
    for time_id, time in enumerate(Times):
        for audience_id, audience in enumerate(Audiences):
            for task_id, task in enumerate(Tasks):
                for teacher_id, teacher in enumerate(Teachers):
                    if teacher.check_task(task_id) == None:
                        model.Add(schedule[time_id, audience_id, task_id, teacher_id] == 0) # Учитель ведёт только свой урок
    
    for time_id, time in enumerate(Times):
        for audience_id, audience in enumerate(Audiences):
            for teacher_id, teacher in enumerate(Teachers):
                for task_id, task in enumerate(Tasks):
                    if Tasks[task_id] 
                

    priorities = []
    for time_id, time in enumerate(Times):
        for audience_id, audience in enumerate(Audiences):
            for task_id, task in enumerate(Tasks):
                for teacher_id, teacher in enumerate(Teachers):
                    priority = Teachers[teacher_id].check_task(task_id)
                    if priority == None:
                        continue
                    # если в time_id, audience_id есть урок task_id и его ведёт teacher_id
                    # тогда schedule[time_id, audience_id, task_id, teacher_id] = 1
                    # в таком случае приоритет такого занятия равен приоритету teacher_id к task_id
                    # в тех случаях когда schedule[time_id, audience_id, task_id, teacher_id] = 0
                    # приоритет будет равен 0
                    # таким образом на некоторый task_id будет выбран teacher_id с наивысшим приоритетом
                    priorities.append(schedule[time_id, audience_id, task_id, teacher_id] * priority)
    model.Maximize(sum(priorities))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        table_obj = Schedule()
        
        for time_id, time in enumerate(Times):
            for audience_id, audience in enumerate(Audiences):
                for task_id, task in enumerate(Tasks):
                    for teacher_id, teacher in enumerate(Teachers):
                        if solver.Value( schedule[time_id, audience_id, task_id, teacher_id] ):
                            table_obj.append( Times[time_id], Tasks[task_id], Teachers[teacher_id], Audiences[audience_id] )
        table_obj.print()


    else:
        print("Нет решения")


    print()
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())

        
if __name__ == '__main__':
    main()