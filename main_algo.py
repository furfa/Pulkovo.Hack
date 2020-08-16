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
    
    max_time = len(Tasks)

    all_tasks = {}
    teachers_task_intervals = collections.defaultdict(list)
    all_tim_aud = collections.defaultdict(list)

    for time_id, time in enumerate(Times):
        for audience_id, audience in enumerate(Audiences):
            tasks_presence = []
            for task_id, task in enumerate(Tasks):

                suffix = f'0_{time_id=}_{audience_id=}'
                task_used = model.NewBoolVar('used'+suffix)
                tasks_presence.append(task_used)

            all_tim_aud[time_id, audience_id] = tasks_presence
            model.Add(sum(tasks_presence) <= 1)

    for task_id, task in enumerate(Tasks):
        task_in_total = []
        for time_id, time in enumerate(Times):
            for audience_id, audience in enumerate(Audiences):
                task_in_total.append(all_tim_aud[time_id, audience_id][task_id])
        model.Add(sum(task_in_total) == 1)

    for time_id, time in enumerate(Times):
        for task_id, task in enumerate(Tasks):
            task_in_total = []
        
            for audience_id, audience in enumerate(Audiences):
                task_in_total.append(all_tim_aud[time_id, audience_id][task_id])
            model.Add( sum(task_in_total) <= 1)
    
    for task_id, task in enumerate(Tasks):
        teachers_presence = []
        for teacher_id, teacher in enumerate(Teachers):
            if teacher.check_task(task_id) == None:
                continue
            
            suffix = f'_{task_id=}'
            teacher_suffix = f'_{task_id=}_{teacher_id=}'
            duration = 1

            teacher_used = model.NewBoolVar('used'+suffix)
            teachers_presence.append(teacher_used)

            start_var = model.NewIntVar(0, max_time, 'start' + suffix)
            end_var = model.NewIntVar(0, max_time, 'end' + suffix)
            interval_var_optional = model.NewOptionalIntervalVar(start_var, duration, end_var, teacher_used,
                                                'interval' + teacher_suffix)

            teachers_task_intervals[teacher_id].append(interval_var_optional)

            all_tasks[task_id, teacher_id] = {
                "teacher": teacher_id,
                "task": task_id,
                "start"    : start_var,
                "end"      : end_var,
                "interval" : interval_var_optional,
                "teacher_work": teacher_used
            }
        model.Add(sum(teachers_presence) == 1)

        for teacher_id, teacher in enumerate(Teachers):
            model.AddNoOverlap(teachers_task_intervals[teacher_id])

    #in some TIME somewhere works TEACHER
    # teacher_in_time = collections.defaultdict(list)
    # for time_id, time in enumerate(Times):
    #     teachers_presence = []
    #     for teacher_id, teacher in enumerate(Teachers):
    #         suffix = f'3_{time_id=}'
    #             teacher_used = model.NewBoolVar('used'+suffix)
    #             teachers_presence.append(task_used)
    #         teacher_in_time[time_id] = tasks_presence

    
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    tasks_in_tim_aud = {}
    if status == cp_model.OPTIMAL:
        table_obj = Schedule()

        for time_id, time in enumerate(Times):
            for audience_id, audience in enumerate(Audiences):
                tasks = [solver.Value(i) for i in all_tim_aud[time_id, audience_id]]
                for i in range(len(tasks)):
                    if tasks[i]:
                        tasks_in_tim_aud[i] = (time_id, audience_id)

        
        for (task_id, teacher_id),data in all_tasks.items():
            if not solver.Value(data["teacher_work"]):
                continue

            (task_time_id, task_audience_id) = tasks_in_tim_aud[task_id]

            table_obj.append( Times[task_time_id], Tasks[task_id], Teachers[teacher_id], Audiences[task_audience_id] )

        table_obj.print()

            
    else:
        print("Нет решения")

    # import pdb; pdb.set_trace()
    # solution_printer = PulkovoPartialSolutionPrinter(
    #     tasks = Tasks,
    #     teachers = Teachers,
    #     all_tasks = all_tasks,
    #     sols = range(5)
    # )

    # solver.SearchForAllSolutions(model, solution_printer)


    print()
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())

        

if __name__ == '__main__':
    main()