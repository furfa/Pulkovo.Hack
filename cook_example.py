import random

def main():

    orders = []
    # create 10 orders
    for i in range(1,10):
        # pick a random number of meals for this order between 1-8
        # max customers per order is 8
        number_of_meals = random.randint(1,8)
        meals = []
        for j in range(number_of_meals):
            # pick a random meal id between 1 and 10
            meal_id = random.randint(1,10)
            meal = Meal(meal_id)
            meals.append(meal)

        order = Order(meals)
        orders.append(order)


    # create the model
    model = cp_model.CpModel()

    kitchen_capacity = 5  # a kitchen can only cook 5 meals at a time
    driver_capacity = 20 # a driver can carry only 20 meals at a time

    horizon = 40  # the max time a meal can be cooked at .. we say at the 40th minute mark

    kitchen_one_intervals = []
    kitchen_two_intervals = []

    kitchen_one_demands = []
    kitchen_two_demands = []

    end_drives = []
    driver_intervals = collections.defaultdict(list)

    number_of_drivers = 2
    driver_presences = collections.defaultdict(list)

    driver_demands = collections.defaultdict(list)

    job_master_drive_start = {}
    job_master_drive_end = {}

    job_driver_starts = collections.defaultdict(list)
    job_driver_ends = collections.defaultdict(list)
    job_to_driver_intervals = collections.defaultdict(list)

    kitchen_master_intervals =  []


    for o in orders:
        print (o)


    for o in range(len(orders)):
         order = orders[o]

         # create meal cooking constraints
         for m in range(len(order.get_meals())):
             job_id = "job_%i_%i" % (o,m)
             kitchen_one_presence = model.NewBoolVar(job_id + "_cook_presence_k1")
             kitchen_two_presence = model.NewBoolVar(job_id + "_cook_presence_k2")


             start_master_cook = model.NewIntVar(0, horizon, "master_start_meal_" + job_id)
             end_master_cook = model.NewIntVar(0, horizon, "master_end_meal_" + job_id)

             start_cook_time_k1 = model.NewIntVar(0, horizon, "k1_start_meal_" + job_id)
             end_cook_time_k1 = model.NewIntVar(0, horizon, "k1_end_meal_" + job_id)

             start_cook_time_k2 = model.NewIntVar(0, horizon, "k2_start_meal_" + job_id)
             end_cook_time_k2 = model.NewIntVar(0, horizon, "k2_end_meal_" + job_id)

             # the meal gets cooked in either kitchen
             # let's say it takes 5 minutes to cook every meal in every kitchen
             kitchen_one_optional = model.NewOptionalIntervalVar(start_cook_time_k1, 5, end_cook_time_k1, kitchen_one_presence
                                                                 , "kitchen_one_" + job_id)

             kitchen_two_optional = model.NewOptionalIntervalVar(start_cook_time_k2, 5, end_cook_time_k2, kitchen_two_presence
                                                             , "kitchen_two_" + job_id)


             # TODO: add m9 and m10 constraints ...

             kitchen_one_intervals.append(kitchen_one_optional)
             kitchen_two_intervals.append(kitchen_two_optional)

             # takes up demand "1" when a meal is cooked in a kitchen
             kitchen_one_demands.append(1)
             kitchen_two_demands.append(1)


             # master kitchen interval
             model.Add(sum([kitchen_one_presence, kitchen_two_presence]) == 1)
             cook_duration = model.NewIntVar(5, 5, "master_cook_duration_" + job_id)
             master_kitchen_interval = model.NewIntervalVar(start_master_cook, cook_duration, end_master_cook, "kitchen_master_interval_" + job_id)


             model.Add(start_cook_time_k1 == start_master_cook).OnlyEnforceIf(kitchen_one_presence)
             model.Add(end_cook_time_k1 == end_master_cook).OnlyEnforceIf(kitchen_one_presence)
             model.Add(start_cook_time_k2 == start_master_cook).OnlyEnforceIf(kitchen_two_presence)
             model.Add(end_cook_time_k2 == end_master_cook).OnlyEnforceIf(kitchen_two_presence)


             # master drive interval
             start_master_drive = model.NewIntVar(0, horizon, "start_drive_" + job_id)
             end_master_drive = model.NewIntVar(0, horizon, "end_drive_" + job_id)
             master_drive_interval = model.NewIntervalVar(start_master_drive, 10 , end_master_drive,
                                                          "drive_master_interval_" + job_id)

             job_master_drive_start[job_id] = start_master_drive
             job_master_drive_end[job_id] = end_master_drive

             kitchen_master_intervals.append(end_master_drive)


             # create delivery constraints
             for d in range(number_of_drivers):


                 # vars to represent start/end drives
                 start_drive = model.NewIntVar(0, horizon, "start_meal_drive_" + job_id + "_" + str(d))
                 end_drive = model.NewIntVar(0, horizon, "end_meal_drive_" + job_id + " _" + str(d))
                 job_driver_presence = model.NewBoolVar(job_id + "_driver_presence" + "_" + str(d))

                 job_driver_starts[job_id].append(start_drive)
                 job_driver_ends[job_id].append(end_drive)

                 end_drives.append(end_master_drive)


                 # option to drive this meal by driver d
                 # let's assume for simplicity that every driver d takes 10 mins to drive the meal to
                 # any restaurant .. in the real world application this would be different
                 # depending on the time taken to drive to the restaurant where the order came from
                 driver_interval = model.NewOptionalIntervalVar(start_drive, 10, end_drive, job_driver_presence,
                                                                "driver_" + str(d) + "_" + job_id)

                 driver_intervals[d].append(driver_interval)
                 job_to_driver_intervals[job_id].append(driver_interval)
                 driver_presences[job_id].append(job_driver_presence)

                 # 1 meal delivery -> 1 demand from the driver
                 driver_demands[d].append(1)


             # one meal gets assigned to one driver
             # so the sum of all "driver presences" for this delivery must be 1
             for job_id, job_driver_presences in driver_presences.items():
                 model.Add(sum(job_driver_presences) == 1)


             for d in range(number_of_drivers):
                 start_master = job_master_drive_start[job_id]
                 end_master = job_master_drive_end[job_id]
                 p = driver_presences[job_id][d]
                 model.Add(start_master == job_driver_starts[job_id][d]).OnlyEnforceIf(p)
                 model.Add(end_master == job_driver_ends[job_id][d]).OnlyEnforceIf(p)


             # all meals belonging to a single order must be delivered by the same driver
             # unsure on how to model this constraint ... but going to leave it for now

             # precedences
             # a meal must not wait > 20 mins waiting to be picked up
             model.Add(end_master_cook < start_master_drive)
             model.Add(start_master_drive < end_master_cook + 20)
             model.Add(end_master_drive < 40)

    # add capacities and demands
    for d, intervals in driver_intervals.items():
        model.AddCumulative(intervals, driver_demands[d], driver_capacity)


    model.AddCumulative(kitchen_one_intervals, kitchen_one_demands, kitchen_capacity)
    model.AddCumulative(kitchen_two_intervals, kitchen_two_demands, kitchen_capacity)

    for end_drive in end_drives:
        model.Minimize(end_drive)

    print("validation: " +  model.ModelStats())

    solver = cp_model.CpSolver()

    solution_printer = cp_model.ObjectiveSolutionPrinter()
    solver.SolveWithSolutionCallback(model, solution_printer)
    print(solver.ResponseStats())

    for inter in kitchen_master_intervals:
        print ("value: " +  str(solver.Value(inter)))

main()